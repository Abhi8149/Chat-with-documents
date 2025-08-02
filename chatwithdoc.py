from langchain_ollama import OllamaEmbeddings,ChatOllama
import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

Prompt="""You are a expert research assistant which can explain any concept from basic to advance using first principle rule. If you are not sure of answering the query then say that I don't know. Use the provided context to answer the query and be concise and factual and the answer should not be more than 4-5 lines.
Query-{query}
Context-{document_context}
Answer:
 """

load_dotenv()

PDF_STORAGE_PATH='document_store'
os.makedirs(PDF_STORAGE_PATH, exist_ok=True)
EMBEDDINGS_MODEL=OllamaEmbeddings(model='nomic-embed-text')
VECTOR_STORE=InMemoryVectorStore(EMBEDDINGS_MODEL)
LANGUAGE_MODEL=ChatOllama(model='llama3.2:3b', temperature=0.6)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False

def saved_uploaded_doc(uploaded_doc):
    file_path=os.path.join(PDF_STORAGE_PATH, uploaded_doc.name)
    with open(file_path, 'wb') as file:
        file.write(uploaded_doc.getbuffer())
    
    return file_path

def load_document(file_path):
    document_loader=PDFPlumberLoader(file_path)
    return document_loader.load()

def chunk_documents(raw_document):
    text_chunker=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    return text_chunker.split_documents(raw_document)

def index_documents(chunked_documents):
    VECTOR_STORE.add_documents(chunked_documents)

def find_related_docs(query):
    return VECTOR_STORE.similarity_search(query)

def generate_answer(user_query, context_docs):
    context_text="\n\n".join([docs.page_content for docs in context_docs])
    conversation_prompt=ChatPromptTemplate.from_template(Prompt)
    conversation_chain=conversation_prompt | LANGUAGE_MODEL

    return conversation_chain.invoke({'query':user_query, 'document_context':context_text})

def clear_chat_history():
    st.session_state.messages = []
    st.rerun()

st.title("📘 DocuMind AI")
st.markdown('Your Intelligent AI research assistant')
st.markdown('---')

uploaded_pdf=st.file_uploader(
    "Upload Research document (PDF)",
    type="pdf",
    help='Select document for analysis',
    accept_multiple_files=False
)

if uploaded_pdf:
    # Process document only if not already processed
    if not st.session_state.document_processed:
        with st.spinner("🔄 Processing document..."):
            saved_path=saved_uploaded_doc(uploaded_pdf)
            raw_docs=load_document(saved_path)
            processed_chunks=chunk_documents(raw_docs)
            index_documents(processed_chunks)
            st.session_state.document_processed = True

    st.success("✅ Document processed successfully! Ask your questions below.")

    # Add clear chat button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🗑️ Clear Chat"):
            clear_chat_history()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    user_input = st.chat_input("Enter your questions about the document...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Generate and display assistant response
        with st.spinner("Analyzing document..."):
            relevant_docs = find_related_docs(user_input)
            response = generate_answer(user_input, relevant_docs)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant message
        with st.chat_message("assistant", avatar="🤖"):
            st.write(response.content)

# Reset document processing when new file is uploaded
if uploaded_pdf is None:
    st.session_state.document_processed = False
    st.session_state.messages = []