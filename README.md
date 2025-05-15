# MedikBot - AI Medical Assistant Chatbot
## OverviewMedikBot is an advanced AI-powered medical assistant chatbot designed to provide accurate and helpful information about medical conditions, symptoms, and general health inquiries. Built using state-of-the-art natural language processing and retrieval-augmented generation techniques, MedikBot offers a user-friendly interface for accessing medical knowledge.
## Features
- **Intelligent Medical Responses**: Leverages Google's Gemini 2.0 Flash model to generate accurate, concise medical information- **Knowledge-Based Answers**: Uses a Pinecone vector database to retrieve relevant medical information from trusted sources
- **Responsive UI**: Beautiful, animated interface that works across desktop and mobile devices- **Real-time Interaction**: Immediate responses with visual feedback during processing
## Technology Stack
- **Frontend**: HTML, CSS, JavaScript with modern animations and responsive design- **Backend**: Flask (Python web framework)
- **AI/ML**:  - LangChain for orchestrating the retrieval-augmented generation pipeline
  - Google Gemini 2.0 Flash for natural language generation  - Sentence Transformers for text embeddings
  - Pinecone for vector storage and similarity search- **Data Processing**: PyPDF for extracting information from medical documents
## Installation
### Prerequisites
- Python 3.8+- Pinecone API key
- Google AI API key
### Setup1. Clone the repository:
   ```   git clone https://github.com/yourusername/gen-ai-medical-chatbot.git
   cd gen-ai-medical-chatbot   ```
2. Create and activate a virtual environment:
   ```   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate   ```
3. Install dependencies:
   ```   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your API keys:   ```
   PINECONE_API_KEY=your_pinecone_api_key   GOOGLE_API_KEY=your_google_api_key
   ```
5. Prepare your medical data:   - Place PDF documents in the `data/` directory
   - Run the indexing script to process and store embeddings:     ```
     python store_index.py     ```
6. Start the application:
   ```   python app.py
   ```
7. Access the chatbot at `http://localhost:5000`
## Usage1. Type your medical question in the input field
2. Press Enter or click the send button3. Receive a concise, informative response based on medical knowledge
## Project Structure
```gen-ai-medical-chatbot/
├── app.py                  # Main Flask application├── data/                   # Directory for medical PDF documents
├── requirements.txt        # Python dependencies├── setup.py                # Package setup file
├── src/│   ├── __init__.py
│   ├── helper.py           # Utility functions for document processing│   └── prompt.py           # System prompts for the LLM
├── static/│   ├── css/
│   │   └── style.css       # Styling for the chatbot interface│   └── js/
│       └── chat.js         # Frontend JavaScript for the chat functionality├── templates/
│   └── index.html          # Main HTML template└── store_index.py          # Script to process documents and create vector index
```
## Development
### Adding New Medical Data1. Add PDF files to the `data/` directory
2. Run `python store_index.py` to update the vector database3. Restart the application to use the new knowledge base
### Customizing the Model
You can adjust the model parameters in `app.py`:```python
llm = ChatGoogleGenerativeAI(    model="gemini-2.0-flash",
    temperature=0.6,  # Adjust for creativity vs. accuracy    max_output_tokens=500  # Adjust for response length
)```
## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Acknowledgments
- Medical information sourced from publicly available medical literature
























































# gen-ai-medical-chatbot
