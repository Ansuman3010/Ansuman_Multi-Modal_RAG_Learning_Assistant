import yt_dlp
import uuid
import os

def download_youtube_audio(url: str) -> str:
    """
    Downloads the audio from a YouTube URL using yt-dlp.
    Returns the path to the downloaded audio file.
    """
    temp_filename = f"temp_audio_{uuid.uuid4().hex}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{temp_filename}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        
        # 'cookiesfrombrowser': ('chrome', ), 
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            final_filename = ydl.prepare_filename(info_dict)
            
            if not os.path.exists(final_filename):
                 raise FileNotFoundError(f"Audio file was not created successfully.")
                 
            return final_filename
            
    except yt_dlp.utils.DownloadError as e:
        raise Exception(f"Failed to download audio from YouTube. The video might be private, deleted, or the URL is invalid. Details: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred during audio download: {str(e)}")
