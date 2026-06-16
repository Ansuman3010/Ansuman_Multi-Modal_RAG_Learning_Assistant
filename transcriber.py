import whisper

def transcribe_audio(audio_path: str, model_name: str = "base") -> str:
    """
    Transcribes an audio file using OpenAI's Whisper model.
    """
    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        raise Exception(f"Failed to transcribe audio. Ensure ffmpeg is installed on your system. Details: {str(e)}")
