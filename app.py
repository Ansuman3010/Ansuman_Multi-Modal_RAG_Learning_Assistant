import streamlit as st
import os
from utils import get_pdf_text, get_youtube_transcript, get_text_chunks
from rag import RAGManager

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_manager" not in st.session_state:
        try:
            st.session_state.rag_manager = RAGManager()
        except ValueError as e:
            st.error(f"Configuration Error: {str(e)}")
            st.stop()

def main():
    st.set_page_config(page_title="Multi-Modal RAG Assistant", page_icon="📚", layout="wide")
    init_session_state()
    
    st.title("📚 Multi-Modal RAG Learning Assistant")
    st.markdown("Upload PDFs or enter YouTube URLs to chat, summarize, and generate study materials!")

    # Sidebar
    with st.sidebar:
        st.header("1. Upload Content")
        
        pdf_docs = st.file_uploader("Upload your PDFs", accept_multiple_files=True, type=["pdf"])
        youtube_url = st.text_input("Or enter a YouTube Video URL")
        
        if st.button("Process Content"):
            with st.spinner("Processing..."):
                documents = []
                try:
                    if pdf_docs:
                        pdf_docs_content = get_pdf_text(pdf_docs)
                        documents.extend(pdf_docs_content)
                        st.success(f"Extracted text from {len(pdf_docs)} PDF(s).")
                        
                    if youtube_url:
                        yt_docs_content = get_youtube_transcript(youtube_url)
                        documents.extend(yt_docs_content)
                        st.success("Extracted text from YouTube video.")
                        
                    if documents:
                        chunks = get_text_chunks(documents)
                        st.session_state.rag_manager.add_to_vector_store(chunks)
                        st.success("Content processed and added to the knowledge base successfully!")
                    else:
                        st.warning("Please upload a PDF or enter a YouTube URL.")
                except Exception as e:
                    st.error(f"Error processing content: {str(e)}")
                    
        st.divider()
        st.header("2. Additional Features")
        if st.button("📝 Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = st.session_state.rag_manager.generate_content("summary")
                st.session_state.messages.append({"role": "assistant", "content": f"**Summary:**\n\n{summary}"})
                st.rerun()
                
        if st.button("📖 Generate Study Notes"):
            with st.spinner("Generating study notes..."):
                notes = st.session_state.rag_manager.generate_content("notes")
                st.session_state.messages.append({"role": "assistant", "content": f"**Study Notes:**\n\n{notes}"})
                st.rerun()
                
        if st.button("❓ Generate 10 MCQs"):
            with st.spinner("Generating MCQs..."):
                mcqs = st.session_state.rag_manager.generate_content("mcq")
                st.session_state.messages.append({"role": "assistant", "content": f"**MCQs:**\n\n{mcqs}"})
                st.rerun()

        st.divider()
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # Main Chat Interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, sources = st.session_state.rag_manager.ask_question(prompt)
                
                response_content = answer
                if sources:
                    response_content += "\n\n**Sources:**\n"
                    for source in sources:
                        response_content += f"- {source}\n"
                        
                st.markdown(response_content)
                st.session_state.messages.append({"role": "assistant", "content": response_content})

if __name__ == "__main__":
    main()
