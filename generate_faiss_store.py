from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# Load local text knowledge base
loader = TextLoader("farming_knowledge_base.txt")
documents = loader.load()

# Split into smaller chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# Use HuggingFace embeddings (no API key required)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS index
vectorstore = FAISS.from_documents(chunks, embeddings)

# Save the vectorstore locally
vectorstore.save_local("rag_vector_store")

print("✅ FAISS vector store generated and saved locally!")
