import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

def extract_video_id(video_url):
    """Extracts YouTube video ID from various URL formats."""
    patterns = [
        r"v=([a-zA-Z0-9_-]+)",        
        r"youtu\.be/([a-zA-Z0-9_-]+)", 
        r"embed/([a-zA-Z0-9_-]+)",     
        r"\/v\/([a-zA-Z0-9_-]+)"       
    ]
    
    for pattern in patterns:
        match = re.search(pattern, video_url)
        if match:
            return match.group(1)
    
    return None

def get_video_transcript(video_id):
    """Fetches the transcript of a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    except Exception as e:
        return f"Error fetching transcript: {e}"

def summarize_transcript(transcript_text):
    """Summarizes the transcript using OpenAI's GPT model."""
    try:
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)
        messages = [
            SystemMessage(content="You are an AI assistant that summarizes YouTube video transcripts."),
            HumanMessage(content=f"Summarize the following transcript:\n{transcript_text}")
        ]
        
        response = llm(messages)
        return response.content if response else "Error: No response from AI."
    
    except Exception as e:
        return f"Error generating summary: {e}"

def main():
    video_url = input("Enter YouTube Video URL: ").strip()
    
    print("\nExtracting Video ID...")
    video_id = extract_video_id(video_url)
    
    if not video_id:
        print("Invalid YouTube URL. Please check and try again.")
        return
    
    print("\nFetching transcript...")
    transcript_text = get_video_transcript(video_id)

    if "Error" in transcript_text:
        print(transcript_text)
        return
    
    print("\nGenerating summary...")
    summary = summarize_transcript(transcript_text)

    print("\nVideo Summary:")
    print(summary)

if __name__ == "__main__":
    main()
