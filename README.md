# MedikBot - AI Medical Assistant Chatbot

## Overview
MedikBot is an advanced AI-powered medical assistant chatbot designed to provide accurate and helpful information about medical conditions, symptoms, and general health inquiries. Built using state-of-the-art natural language processing and retrieval-augmented generation techniques, MedikBot offers a user-friendly interface for accessing medical knowledge.

## Features
- **Intelligent Medical Responses**: Leverages Google's Gemini 2.0 Flash model to generate accurate, concise medical information
- **Knowledge-Based Answers**: Uses a Pinecone vector database to retrieve relevant medical information from trusted sources
- **Responsive UI**: Beautiful, animated interface that works across desktop and mobile devices
- **Real-time Interaction**: Immediate responses with visual feedback during processing
- **Containerized**: Packaged with Docker for consistent deployment across environments
- **Continuous Deployment**: Automatic deployment via GitHub Actions to Fly.io

## Live Demo
Visit the live application at [https://gen-ai-medical-chatbot.fly.dev](https://gen-ai-medical-chatbot.fly.dev)

## Technology Stack
- **Frontend**: HTML, CSS, JavaScript with modern animations and responsive design
- **Backend**: Flask (Python web framework)
- **AI/ML**:
  - LangChain for orchestrating the retrieval-augmented generation pipeline
  - Google Gemini 2.0 Flash for natural language generation
  - Sentence Transformers for text embeddings
  - Pinecone for vector storage and similarity search
- **Data Processing**: PyPDF for extracting information from medical documents
- **Containerization**: Docker for consistent environment and deployment
- **Deployment**: Fly.io for hosting, GitHub Actions for CI/CD

## Installation

### Prerequisites
- Python 3.8+
- Pinecone API key
- Google AI API key
- Docker (optional, for containerized deployment)

### Local Setup
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gen-ai-medical-chatbot.git
   cd gen-ai-medical-chatbot
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your API keys:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```
5. Prepare your medical data:
   - Place PDF documents in the `data/` directory
   - Run the indexing script to process and store embeddings:
     ```
     python store_index.py
     ```
6. Start the application:
   ```
   python app.py
   ```
7. Access the chatbot at `http://localhost:5000`

### Docker Setup
1. Build the Docker image:
   ```
   docker build -t medikbot .
   ```
2. Run the container:
   ```
   docker run -p 8080:8080 \
     -e PINECONE_API_KEY=your_pinecone_api_key \
     -e GOOGLE_API_KEY=your_google_api_key \
     medikbot
   ```
3. Access the chatbot at `http://localhost:8080`

## Deployment

### Deploying to Fly.io
1. Install the Fly CLI:
   ```
   curl -L https://fly.io/install.sh | sh
   ```
2. Login to Fly:
   ```
   fly auth login
   ```
3. Launch your app:
   ```
   fly launch
   ```
4. Set your secrets:
   ```
   fly secrets set PINECONE_API_KEY=your_pinecone_api_key
   fly secrets set GOOGLE_API_KEY=your_google_api_key
   ```
5. Deploy your app:
   ```
   fly deploy
   ```

### Continuous Deployment
This project uses GitHub Actions for continuous deployment to Fly.io. When you push to the main branch, your changes are automatically deployed.

To set up continuous deployment:
1. Create a Fly.io deploy token:
   ```
   fly tokens create deploy -x 999999h
   ```
2. Add the token to your GitHub repository secrets as `FLY_API_TOKEN`
3. The workflow in `.github/workflows/fly-deploy.yml` will handle the rest

## Usage
1. Type your medical question in the input field
2. Press Enter or click the send button
3. Receive a concise, informative response based on medical knowledge

## Project Structure
```
gen-ai-medical-chatbot/
├── app.py                  # Main Flask application
├── Dockerfile              # Docker configuration for containerization
├── .dockerignore           # Files to exclude from Docker context
├── data/                   # Directory for medical PDF documents
├── requirements.txt        # Python dependencies
├── setup.py                # Package setup file
├── src/
│   ├── __init__.py
│   ├── helper.py           # Utility functions for document processing
│   └── prompt.py           # System prompts for the LLM
├── static/
│   ├── css/
│   │   └── style.css       # Styling for the chatbot interface
│   └── js/
│       └── chat.js         # Frontend JavaScript for the chat functionality
├── templates/
│   └── index.html          # Main HTML template
├── store_index.py          # Script to process documents and create vector index
└── .github/
    └── workflows/
        ├── fly-deploy.yml  # GitHub Actions workflow for deployment
        └── deploy.yml      # Alternative deployment workflow
```

## Development

### Adding New Medical Data
1. Add PDF files to the `data/` directory
2. Run `python store_index.py` to update the vector database
3. Restart the application to use the new knowledge base

### Customizing the Model
You can adjust the model parameters in `app.py`:
```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.6,  # Adjust for creativity vs. accuracy
    max_output_tokens=500  # Adjust for response length
)
```

### Docker Development
For development with Docker:
1. Build the development image:
   ```
   docker build -t medikbot:dev .
   ```
2. Run with volume mounting for live code changes:
   ```
   docker run -p 8080:8080 \
     -v $(pwd):/app \
     -e FLASK_DEBUG=1 \
     -e PINECONE_API_KEY=your_pinecone_api_key \
     -e GOOGLE_API_KEY=your_google_api_key \
     medikbot:dev
   ```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Medical information sourced from publicly available medical literature
