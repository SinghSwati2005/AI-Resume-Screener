import os
import importlib
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    try:
        st = importlib.import_module("streamlit")
        API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=API_KEY)
MODEL = "openai/gpt-oss-120b"