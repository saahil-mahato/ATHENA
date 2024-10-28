import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a human writer. You can write dialogues and story for all kinds of NPCs in a video game.",
)
