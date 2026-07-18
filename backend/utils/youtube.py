import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    """
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def get_video_title(url: str) -> str:
    """
    Fetches the video title from a YouTube URL.
    """
    try:
        import requests
        r = requests.get(url, verify=False)
        match = re.search(r'<title>(.*?)</title>', r.text)
        if match:
            title = match.group(1)
            # Clean up suffix
            if title.endswith(" - YouTube"):
                title = title[:-10]
            return title
        return "Unknown Video Title"
    except Exception:
        return "Unknown Video Title"

def get_transcript(video_id: str) -> str:
    """
    Fetches the transcript for a given video ID and returns it as a single string.
    """
    try:
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        session = requests.Session()
        session.verify = False
        
        transcript_list = YouTubeTranscriptApi(http_client=session).fetch(video_id)
        # transcript_list is a list of FetchedTranscriptSnippet objects
        text_parts = [part.text for part in transcript_list]
        full_text = " ".join(text_parts)
        # Clean up some common issues in auto-generated text
        full_text = full_text.replace('\n', ' ')
        return full_text
    except TranscriptsDisabled:
        raise Exception("The creator has disabled transcripts for this video.")
    except NoTranscriptFound:
        raise Exception("YouTube could not auto-generate a transcript for this video.")
    except Exception as e:
        raise Exception(f"An error occurred while fetching the transcript: {str(e)}")
