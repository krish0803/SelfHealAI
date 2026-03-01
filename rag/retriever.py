import os
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

class PineconeRetriever:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.vectorstore = PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embeddings
        )

    def query(self, text: str) -> str:
        try:
            results = self.vectorstore.similarity_search(text, k=3)
            return "\n---\n".join([doc.page_content for doc in results])
        except Exception as e:
            return f"Error querying Pinecone: {str(e)}"

# Singleton for the agent to use
retriever = None
if os.getenv("PINECONE_API_KEY") and os.getenv("OPENAI_API_KEY"):
    retriever = PineconeRetriever()
else:
    class MockRetriever:
        def query(self, text): return "Retriever not initialized (missing API keys)."
    retriever = MockRetriever()
