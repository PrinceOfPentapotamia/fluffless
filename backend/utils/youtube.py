import re

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
    Fetches the transcript for a given video ID using RapidAPI to bypass cloud IP bans.
    """
    try:
        import requests
        import urllib3
        import os
        import html
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        rapidapi_key = os.environ.get("RAPIDAPI_KEY")
        if not rapidapi_key:
            raise Exception("RAPIDAPI_KEY environment variable is not set. Please add it to your Render dashboard.")

        url = "https://youtube-transcript3.p.rapidapi.com/api/transcript"
        querystring = {"videoId": video_id}
        headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "youtube-transcript3.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring, verify=False)
        data = response.json()
        
        if not data.get("success"):
            error_msg = data.get("error", "Unknown API error")
            raise Exception(f"RapidAPI Error: {error_msg}")
            
        transcript_list = data.get("transcript", [])
        text_parts = [html.unescape(part.get("text", "")) for part in transcript_list]
        full_text = " ".join(text_parts).replace('\n', ' ')
        
        return full_text
        
    except Exception as e:
        raise Exception(f"An error occurred while fetching the transcript: {str(e)}")
