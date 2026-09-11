import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Create a chat completion request using a current production model ID
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models in 2 sentences.",
        }
    ],
    model="openai/gpt-oss-20b", 
)

print(chat_completion.choices[0].message.content)