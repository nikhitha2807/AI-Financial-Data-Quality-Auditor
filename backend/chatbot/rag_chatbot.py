import os
from groq import Groq
from backend.database.vector_store import VectorStore
from dotenv import load_dotenv

load_dotenv()

class RAGChatbot:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    async def get_response(self, dataset_id: str, question: str):
        if not self.client:
            return "Groq API Key not configured. Chatbot unavailable."

        # Retrieve context from VectorStore
        context_chunks = self.vector_store.query_context(dataset_id, question)
        context = "\n".join(context_chunks)

        prompt = f"""
        You are a Data Guardian AI Assistant. Use the provided dataset context to answer the user's question.
        If the answer is not in the context, use your general data science knowledge to provide a helpful response, 
        but clarify what is based on the specific dataset and what is general advice.

        ### Dataset Context:
        {context}

        ### User Question:
        {question}
        
        Answer professionally and concisely.
        """
        
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful data quality assistant."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error in chatbot: {str(e)}"
