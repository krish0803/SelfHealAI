import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

def index_codebase():
    # Load codebase
    loader = DirectoryLoader('codebase', glob="**/*.py", loader_cls=TextLoader)
    documents = loader.load()

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Initialize Pinecone
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    
    pc = Pinecone(api_key=api_key)
    
    # Create vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore.from_documents(
        docs, 
        embeddings, 
        index_name=index_name
    )
    print(f"Successfully indexed {len(docs)} chunks from codebase into Pinecone index: {index_name}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("PINECONE_API_KEY"):
        print("Error: Missing API keys in environment.")
    else:
        index_codebase()
