from flask import Flask, render_template, jsonify, request
from langchain_google_genai import ChatGoogleGenerativeAI
from src.helper import load_pdf_file, text_split, download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os   
from src.prompt import *

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embeddings = download_embeddings()

index_name = "medikbot-index"

# Load existing Index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,      
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.6,
    max_output_tokens=500,
    google_api_key=GOOGLE_API_KEY
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "Question: {input}"),  # Changed {question} to {input}
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    input = user_message
    response = retrieval_chain.invoke({"input": input})
    return jsonify({'response': response['answer']})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
