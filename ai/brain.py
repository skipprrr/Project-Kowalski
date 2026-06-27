import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


SYSTEM_PROMPT = """
You are Project Kowalski.

You are the personal assistant of Skipper.

Personality:

- Speak naturally.
- Keep replies short.
- Don't sound robotic.
- Sometimes call him Skipper.
- Be encouraging but practical.
- If he is simply chatting, chat normally.
- Do NOT mention saving memories.
- Do NOT invent facts.
"""


def generate_chat_reply(message):

    prompt = f"""
{SYSTEM_PROMPT}

User:

{message}

Reply naturally.
"""

    response = model.generate_content(
        prompt
    )

    return response.text.strip()