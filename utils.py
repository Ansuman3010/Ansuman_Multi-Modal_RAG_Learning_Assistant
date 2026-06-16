import os
from urllib.parse import urlparse, parse_qs
from pypdf import PdfReader
from youtube_audio import download_youtube_audio
from transcriber import transcribe_audio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def get_pdf_text(pdf_files) -> list[Document]:
    """Extracts text from uploaded PDF files and returns a list of Langchain Documents."""
    documents = []
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        filename = pdf_file.name
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:
                doc = Document(
                    page_content=text,
                    metadata={"source": filename, "page": i + 1}
                )
                documents.append(doc)
    return documents

def extract_youtube_video_id(url: str) -> str:
    """Extracts the video ID from a YouTube URL."""
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p.get('v', [None])[0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def get_youtube_transcript(url: str) -> list[Document]:
    """Fetches the transcript for a YouTube video and returns it as Langchain Documents."""
    video_id = extract_youtube_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL provided.")
    
    audio_file = None
    try:
        # Download audio via yt-dlp
        audio_file = download_youtube_audio(url)
        
        # Transcribe using Whisper
        transcript_text = transcribe_audio(audio_file, model_name="base")
        
        # Create LangChain Document
        doc = Document(
            page_content=transcript_text,
            metadata={"source": url}
        )
        return [doc]

    except Exception as e:
        raise Exception(f"Could not extract transcript via Whisper. Error: {str(e)}")
    finally:
        # Automatically delete temporary audio files after transcription
        if audio_file and os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except:
                pass

def get_text_chunks(documents: list[Document]) -> list[Document]:
    """Splits documents into smaller chunks for vectorization."""
    if not documents:
        return []
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    return chunks
