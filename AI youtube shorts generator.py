import streamlit as st
from moviepy.editor import *
from gtts import gTTS
import google.generativeai as genai

st.title("AI YouTube Shorts Generator")

topic = st.text_input("Video Topic", "3 Productivity Hacks for Students")

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_script(topic):
    prompt = f"""Write a 50-word YouTube Shorts script about {topic}. 
    Hook in first 3 seconds. Fast pace. End with CTA. Format: Hook | Tip1 | Tip2 | Tip3 | CTA"""
    return model.generate_content(prompt).text

def create_video(script):
    # Text to speech
    tts = gTTS(script)
    tts.save("voice.mp3")
    audio = AudioFileClip("voice.mp3")
    
    # Simple video: colored background + text
    txt = TextClip(script, fontsize=50, color='white', size=(720,1280), method='caption')
    txt = txt.set_duration(audio.duration)
    
    video = ColorClip(size=(720,1280), color=(0,0,0), duration=audio.duration)
    final = CompositeVideoClip([video, txt]).set_audio(audio)
    final.write_videofile("short.mp4", fps=24)
    return "short.mp4"

if st.button("Generate Short"):
    script = generate_script(topic)
    st.write("**Script:**", script)
    video_path = create_video(script)
    st.video(video_path)
    st.download_button("Download Short", video_path)