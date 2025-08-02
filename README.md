# DocuMind AI - RAG Document Chat Application

A Streamlit-based Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and have intelligent conversations with their content using local LLMs via Ollama.

## 🚀 Features

- **PDF Document Upload**: Easy drag-and-drop PDF file upload interface
- **Intelligent Document Processing**: Automatic text extraction and chunking
- **Vector Search**: Semantic similarity search for relevant document sections
- **Chat Interface**: Interactive chat experience with document context
- **Local LLM Integration**: Uses Ollama for privacy-focused, local AI processing
- **Persistent Chat History**: Maintains conversation context during session
- **Expert Responses**: AI assistant trained to explain concepts from basic to advanced levels

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **LLM Framework**: LangChain
- **Embeddings**: Nomic Embed Text (via Ollama)
- **Language Model**: Llama 3.2:3b (via Ollama)
- **Document Processing**: PDFPlumber
- **Vector Store**: In-Memory Vector Store
- **Text Splitting**: Recursive Character Text Splitter

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
3. Required Ollama models downloaded:


2. **Access the application** in your browser (typically `http://localhost:8501`)

3. **Upload a PDF document** using the file uploader

4. **Wait for processing** - the application will:
- Extract text from the PDF
- Split it into manageable chunks
- Create vector embeddings
- Index the content

5. **Start chatting** with your document using the chat input field

## 💡 How It Works

1. **Document Upload**: Users upload PDF files which are saved locally in a `document_store` directory
2. **Text Extraction**: PDFPlumber extracts text content from the uploaded PDF
3. **Chunking**: Documents are split into 1000-character chunks with 200-character overlap
4. **Vectorization**: Text chunks are converted to embeddings using Nomic Embed Text model
5. **Indexing**: Embeddings are stored in an in-memory vector store
6. **Query Processing**: User queries are matched against document chunks using similarity search
7. **Response Generation**: Relevant chunks are provided as context to Llama 3.2 for generating responses

## ⚙️ Configuration

The application uses the following default settings:

- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Temperature**: 0.6 (for response generation)
- **Response Length**: Limited to 4-5 lines for conciseness

You can modify these parameters in the code:



## 🔍 Key Functions

- `saved_uploaded_doc()`: Saves uploaded PDF files locally
- `load_document()`: Loads and extracts text from PDF files
- `chunk_documents()`: Splits documents into manageable chunks
- `index_documents()`: Creates and stores vector embeddings
- `find_related_docs()`: Performs similarity search for relevant content
- `generate_answer()`: Generates AI responses using retrieved context

## 🛡️ Privacy & Security

- **Local Processing**: All document processing and AI inference happens locally
- **No Data Transmission**: Documents and conversations are not sent to external services
- **Temporary Storage**: Uploaded files are stored locally during the session

## 🔧 Troubleshooting

**Common Issues:**

1. **Ollama not running**: Ensure Ollama service is started
2. **Models not found**: Download required models using `ollama pull`
3. **Memory issues**: Large PDFs may require more system memory
4. **Slow processing**: Consider reducing chunk size or using smaller models

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation


**Note**: This application requires Ollama to be installed and running on your local machine with the specified models available.
