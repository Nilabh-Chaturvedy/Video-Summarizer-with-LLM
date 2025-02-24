import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv() #Load the environment variables

import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a Youtube video summarizer.You will be taking the transcript text and summarize
the entire video and provide important summary in points within 200-250 words. The Transcript text
is appended here"""

def generate_gemini_content(transcript,subject,):
    
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript)
    return response.text
#Getting the transcript from the youtube videos
def fetch_transcript(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript=YouTubeTranscriptApi.get_transcript(video_id,languages=['en'])
        transcript_text=" ".join([x['text'] for x in transcript])
        return transcript_text
    except Exception as e:
        raise e
#Main function
if __name__=="__main__":
    st.title("Youtube Video Summarizer")
    st.subheader("Enter the youtube video URL")
    youtube_video_url=st.text_input("Enter the youtube video URL")  
    
    if youtube_video_url:
        video_id=youtube_video_url.split("=")[1]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

        if st.button("Get Detailed Summary"):
                transcript_text=fetch_transcript(youtube_video_url)

                if transcript_text:
                    summary=generate_gemini_content(transcript_text,"Youtube Video")
                    st.markdown("#Detailed Notes")
                    st.write(summary)


        
