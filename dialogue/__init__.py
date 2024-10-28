"""
This script configures and initializes a generative AI model using the Google Generative AI library.

It loads environment variables from a .env file and sets up the API key required for authentication
with the Google Generative AI service. The script then creates an instance of a generative model with
specific parameters for generating dialogues and stories for non-player characters (NPCs) in video games.

Modules:
- os: Provides functions for interacting with the operating system, including accessing environment variables.
- google.generativeai: A library for working with Google's generative AI models.
- dotenv: A library to load environment variables from a .env file.

Usage:
1. Ensure that the `GEMINI_API_KEY` is set in your environment variables or in a `.env` file.
2. Run this script to configure the model and prepare it for use.

Example:
    To generate text, call methods on the `model` instance after initialization.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the Google Generative AI with the API key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the generative model with specific instructions for NPC dialogue generation
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a human writer. You can write dialogues and story for all kinds of NPCs in a video game.",
)
