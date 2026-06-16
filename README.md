# Multi-Modal RAG Learning Assistant

An AI-powered learning assistant built with Streamlit, LangChain, FAISS, Whisper, and Gemini.

This application allows users to upload PDF documents and YouTube videos, then interact with the content through a Retrieval-Augmented Generation (RAG) chatbot. Users can ask questions, generate summaries, create study notes, and produce multiple-choice questions from the uploaded learning materials.

---

## Features

### PDF Processing

* Upload one or multiple PDF files
* Extract and process document text
* Preserve document metadata and page references

### YouTube Video Processing

* Paste a YouTube video URL
* Download audio using yt-dlp
* Transcribe speech using OpenAI Whisper
* Works even when YouTube captions are unavailable

### AI-Powered RAG Chatbot

* Ask questions about uploaded content
* Semantic retrieval using FAISS
* Context-aware responses using Gemini
* Source citations for transparency

### Learning Tools

* Generate concise summaries
* Create structured study notes
* Generate 10 MCQs automatically
* Useful for courses, lectures, tutorials, and exam preparation

---

## Architecture

### PDF Pipeline

PDF Upload
↓
Text Extraction
↓
Document Chunking
↓
FAISS Vector Store
↓
Retriever
↓
Gemini
↓
Answer Generation

### YouTube Pipeline

YouTube URL
↓
yt-dlp Audio Download
↓
Whisper Transcription
↓
LangChain Documents
↓
Document Chunking
↓
FAISS Vector Store
↓
Retriever
↓
Gemini
↓
Answer Generation

---

## Project Structure

```text
Multi-Modal-RAG-Learning-Assistant/
│
├── app.py
├── rag.py
├── utils.py
├── youtube_audio.py
├── transcriber.py
├── requirements.txt
├── README.md
```

---

## Tech Stack

### Frontend

* Streamlit

### LLM & RAG

* LangChain
* Google Gemini
* FAISS

### Speech Processing

* OpenAI Whisper

### Video Processing

* yt-dlp

### Document Processing

* PyPDF

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/Multi-Modal-RAG-Learning-Assistant.git

cd Multi-Modal-RAG-Learning-Assistant
```

### Create Virtual Environment

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/Mac:

```bash
python -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install FFmpeg

Whisper requires FFmpeg.

Verify installation:

```bash
ffmpeg -version
```

If FFmpeg is not installed, download and install it and add it to your system PATH.

---

## Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Get your API key from Google AI Studio.

---

## Run Locally

Activate virtual environment:

```bash
venv\Scripts\activate
```

Run Streamlit:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Usage

### Upload PDFs

1. Upload one or more PDF files
2. Click Process Content
3. Ask questions about the uploaded documents

### Process YouTube Videos

1. Paste a YouTube URL
2. Click Process Content
3. Audio is downloaded and transcribed using Whisper
4. Ask questions about the video content

### Generate Learning Material

* Summary
* Study Notes
* MCQs

---

## Example Questions

* Summarize this lecture.
* What are the key concepts discussed?
* Generate study notes from this content.
* Create MCQs for revision.
* Explain the main topic in simple terms.

---

## Future Improvements

* Chat history memory
* Multi-video support
* MP4 file uploads
* OCR for scanned PDFs
* Export notes to PDF
* Quiz mode
* User authentication

---

## Author

Built as an AI/ML internship project demonstrating:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Semantic Search
* Speech-to-Text Processing
* Large Language Models
* Streamlit Deployment
