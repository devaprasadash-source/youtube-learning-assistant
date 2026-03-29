import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

# Load env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🎓 YouTube Learning Assistant (Robust Version)")

video_url = st.text_input("Enter YouTube Video URL:")


# ✅ Extract video ID
def get_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    if parsed_url.path == "/watch":
        return parse_qs(parsed_url.query).get("v", [None])[0]

    if parsed_url.path.startswith("/live/"):
        return parsed_url.path.split("/")[2]

    if parsed_url.path.startswith("/shorts/"):
        return parsed_url.path.split("/")[2]

    return None


# ✅ ROBUST transcript fetch (AUTO language detection)
def get_transcript_text(video_id):
    ytt_api = YouTubeTranscriptApi()

    try:
        transcript_list = ytt_api.list(video_id)

        # Priority: manually created → generated
        try:
            transcript = transcript_list.find_manually_created_transcript(
                [t.language_code for t in transcript_list]
            )
        except:
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )

        data = transcript.fetch()

        return " ".join([t.text for t in data])

    except Exception as e:
        raise Exception("No transcript available for this video.")


# ✅ Chunking
def chunk_text(text, chunk_size=2000):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])


# ✅ Educational processing
def process_chunk(chunk):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an educational assistant.

From this transcript section:
1. Extract key topics
2. Write detailed notes
3. Create 2-3 MCQs with answers

Always respond in English.
"""
            },
            {"role": "user", "content": chunk}
        ]
    )

    return response.choices[0].message.content


# MAIN
if st.button("Generate Study Notes"):
    if not video_url:
        st.warning("Please enter a URL.")
    else:
        video_id = get_video_id(video_url)

        if not video_id:
            st.error("Invalid URL")
        else:
            try:
                st.info("Fetching transcript...")

                full_text = get_transcript_text(video_id)

                st.info("Processing video... ⏳")

                for i, chunk in enumerate(chunk_text(full_text)):
                    with st.expander(f"📘 Section {i+1}"):
                        result = process_chunk(chunk)
                        st.write(result)

                st.success("✅ Study Notes Ready!")

            except Exception as e:
                st.error(f"Error: {str(e)}")