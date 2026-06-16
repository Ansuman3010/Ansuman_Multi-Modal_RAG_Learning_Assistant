import os
from dotenv import load_dotenv
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain_community.vectorstores import FAISS

from langchain_core.documents import Document
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings



load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class RAGManager:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_api_key_here":
            raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
            
        self.embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, google_api_key=api_key)
        self.vector_store_path = "faiss_index"
        
    def create_vector_store(self, chunks: list[Document]):
        """Creates a new vector store from chunks and saves it."""
        if not chunks:
            return
        vector_store = FAISS.from_documents(chunks, embedding=self.embeddings)
        vector_store.save_local(self.vector_store_path)
        
    def add_to_vector_store(self, chunks: list[Document]):
        """Adds chunks to an existing vector store, or creates one if it doesn't exist."""
        if not chunks:
            return
            
        if os.path.exists(self.vector_store_path):
            vector_store = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
            new_vector_store = FAISS.from_documents(chunks, embedding=self.embeddings)
            vector_store.merge_from(new_vector_store)
            vector_store.save_local(self.vector_store_path)
        else:
            self.create_vector_store(chunks)

    def ask_question(self, question: str):
        """Queries the RAG system and returns the answer with sources."""
        try:
            if not os.path.exists(self.vector_store_path):
                raise ValueError("Vector store not found. Please process some documents first.")
                
            vector_store = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
            docs = vector_store.similarity_search(question, k=5)
            context_text = "\n\n".join([doc.page_content for doc in docs])
            
            prompt_template = f"""
            Answer the question as detailed as possible from the provided context. If the answer is not in
            the provided context, just say "The answer is not available in the context." Don't provide the wrong answer.
            
            Context:
            {context_text}
            
            Question: 
            {question}
            
            Answer:
            """
            
            response = self.llm.invoke(prompt_template)
            answer = response.content
            
            sources = []
            for doc in docs:
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "")
                citation = f"{source} (Page {page})" if page else source
                if citation not in sources:
                    sources.append(citation)
                    
            return answer, sources
        except Exception as e:
            return f"An error occurred: {str(e)}", []

    def generate_content(self, task_type: str) -> str:
        """Generates summary, notes, or MCQs based on the vector store content."""
        if not os.path.exists(self.vector_store_path):
             return "No documents processed yet."
             
        vector_store = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
        
        if task_type == "summary":
            query = "Summarize the main topics discussed in these documents."
            system_prompt = "Write a concise and comprehensive summary of the following extracted text."
        elif task_type == "notes":
            query = "Provide key concepts, definitions, and important points for study notes."
            system_prompt = "Create structured study notes from the following text. Use bullet points, bold text for key terms, and clear headings."
        elif task_type == "mcq":
            query = "Generate multiple choice questions based on the key facts in the text."
            system_prompt = "Based on the provided context, generate exactly 10 Multiple Choice Questions (MCQs). Format each question clearly with 4 options (A, B, C, D) and specify the correct answer at the end of each question."
        else:
            return "Invalid task type."
            
        docs = vector_store.similarity_search(query, k=15)
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        prompt = f"{system_prompt}\n\nContext:\n{context_text}"
        
        response = self.llm.invoke(prompt)
        return response.content
