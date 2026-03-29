# 🎓 YouTube Learning Assistant

AI-powered YouTube Learning Assistant that converts videos into structured notes, topics, and MCQs with multi-language support.

## ✨ Features
- 🎥 Supports long YouTube videos (3+ hours)
- 🌍 Multi-language transcript handling
- 📘 Topic-wise structured notes
- ❓ MCQ generation for practice
- ⚡ Chunk-based processing to avoid token limits

## 🧠 How it Works

1. Extract transcript from YouTube
2. Detect language automatically
3. Split into chunks
4. Process each chunk with OpenAI
5. Generate structured notes + MCQs
   
## 🛠 Tech Stack

- Python
- Streamlit
- OpenAI API
- YouTube Transcript API

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
