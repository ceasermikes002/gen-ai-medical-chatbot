from flask import Flask, render_template, jsonify, request
from langchain_google_genai import ChatGoogleGenerativeAI
from src.helper import load_pdf_file, text_split, download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import re
from src.prompt import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("medikbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Set up caching
cache_config = {
    "CACHE_TYPE": "SimpleCache",  # Use Redis in production
    "CACHE_DEFAULT_TIMEOUT": 300
}
cache = Cache(app, config=cache_config)

# Set up rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Load environment variables
load_dotenv()

# Get API keys with fallbacks
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Log API key status (without revealing the actual keys)
if PINECONE_API_KEY:
    logger.info("PINECONE_API_KEY is set")
else:
    logger.error("PINECONE_API_KEY is missing")

if GOOGLE_API_KEY:
    logger.info("GOOGLE_API_KEY is set")
else:
    logger.error("GOOGLE_API_KEY is missing")

# Only set environment variables if they exist
if PINECONE_API_KEY:
    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# API usage tracking
class APIUsageTracker:
    def __init__(self):
        self.daily_count = 0
        self.reset_time = datetime.now()
        
    def track(self):
        current_time = datetime.now()
        if current_time.date() > self.reset_time.date():
            self.daily_count = 0
            self.reset_time = current_time
        
        self.daily_count += 1
        logger.info(f"API call count: {self.daily_count}")
        
        # Alert if approaching limits
        if self.daily_count > 9000:  # Assuming 10k daily limit
            logger.warning(f"Approaching API limit: {self.daily_count}/10000")

api_tracker = APIUsageTracker()

# Get the latest index name
def get_latest_index_name():
    try:
        with open("current_index_version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "medikbot-index"  # Default fallback

# Initialize embeddings and vector store
embeddings = download_embeddings()
index_name = get_latest_index_name()
logger.info(f"Using index: {index_name}")

# Default retriever in case of failure
retriever = None

# Load existing Index
if PINECONE_API_KEY:
    try:
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,      
            embedding=embeddings
        )
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        logger.info("Successfully connected to Pinecone")
    except Exception as e:
        logger.error(f"Error connecting to Pinecone: {str(e)}")
        # Fallback mechanism could be implemented here
else:
    logger.error("Cannot connect to Pinecone: API key is missing")

# Initialize LLM
if GOOGLE_API_KEY:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.6,
            max_output_tokens=500,
            google_api_key=GOOGLE_API_KEY,
            timeout=40  # Increased timeout to prevent worker hanging
        )
        logger.info("Successfully initialized Google Generative AI")
    except Exception as e:
        logger.error(f"Error initializing Google Generative AI: {str(e)}")
        llm = None
else:
    logger.error("Cannot initialize Google Generative AI: API key is missing")
    llm = None

# Set up prompt templates for A/B testing
prompt_templates = {
    "A": ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Question: {input}"),
    ]),
    "B": ChatPromptTemplate.from_messages([
        ("system", system_prompt + "\nPlease provide a very concise answer."),
        ("user", "Question: {input}"),
    ])
}

# Helper functions
def anonymize_phi(text):
    """Remove potentially identifiable information"""
    # Remove names
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME]', text)
    # Remove dates
    text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', '[DATE]', text)
    # Remove phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    return text

def determine_complexity(query):
    """Determine query complexity for tiered response strategy"""
    complexity_score = len(query.split())
    medical_terms = ["diagnosis", "treatment", "symptoms", "prognosis", "etiology"]
    for term in medical_terms:
        if term in query.lower():
            complexity_score += 5
    return "high" if complexity_score > 15 else "low"

def store_feedback(feedback_data):
    """Store user feedback"""
    with open("feedback.log", "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp},{feedback_data['messageId']},{feedback_data['feedback']}\n")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # Track API usage
    api_tracker.track()
    
    # Get and process user message
    user_message = request.json['message']
    request_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    # Log the request
    logger.info(f"Request {request_id}: {user_message}")
    
    # Check if retriever is available
    if retriever is None:
        logger.error(f"Cannot process request {request_id}: Retriever is not available")
        return jsonify({
            'response': "I'm sorry, the service is currently experiencing technical difficulties. Please try again later.",
            'error': "Retriever not available"
        }), 503
    
    # Anonymize input
    anonymized_input = anonymize_phi(user_message)
    
    # Check complexity for tiered response
    complexity = determine_complexity(anonymized_input)
    
    # Try cache for simple queries
    if complexity == "low":
        cached_response = cache.get(anonymized_input)
        if cached_response:
            logger.info(f"Cache hit for request {request_id}")
            return jsonify({'response': cached_response, 'source': 'cache'})
    
    # A/B testing - randomly select prompt variant
    import random
    variant = "A" if random.random() < 0.5 else "B"
    prompt = prompt_templates[variant]
    
    # Create chain with selected prompt
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    try:
        # Get response from LLM
        response = retrieval_chain.invoke({"input": anonymized_input})
        answer = response['answer']
        
        # Log the response
        logger.info(f"Response {request_id} (variant {variant}): {answer[:100]}...")
        
        # Cache the response for simple queries
        if complexity == "low":
            cache.set(anonymized_input, answer)
        
        return jsonify({
            'response': answer,
            'variant': variant,
            'requestId': request_id
        })
    except Exception as e:
        logger.error(f"Error processing request {request_id}: {str(e)}")
        return jsonify({
            'response': "I'm sorry, I encountered an error processing your request. Please try again later.",
            'error': str(e)
        }), 500

@app.route('/api/feedback', methods=['POST'])
def feedback():
    feedback_data = request.json
    
    # Log feedback
    logger.info(f"Feedback for message {feedback_data['messageId']}: {feedback_data['feedback']}")
    
    # Store in database for analysis
    store_feedback(feedback_data)
    
    return jsonify({'status': 'success'})

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Get port from environment variable (Fly.io sets PORT=8080)
    # or use 5000 as default for local development
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
