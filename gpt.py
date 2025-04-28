from openai import OpenAI
from constants import OPENAI_API_KEY
from utility import update_status

client = OpenAI(api_key=OPENAI_API_KEY)

system = """
You are an assistant that reads a user's message and determines if it is about hiring, recruiting, or looking for a developer, programmer, or software engineer.

Reply "yes" only if:
- The content is hiring or recruiting for a developer, programmer, or software engineer
AND
- There are no requirements related to nationality, ethnicity, native language ability (such as "native English speaker", "European only", or similar).

Reply "no" if:
- The message mentions any nationality, ethnicity, or native language restrictions
OR
- The message is unrelated to hiring a developer, programmer, or software engineer.

You must reply with only "yes" or "no" and nothing else.
Always answer strictly in lowercase: "yes" or "no".
"""

chatLog = "Chat Bot: Hi, I'm a Chat Bot. What can I help you with today?\n"


def check_job_post(text) -> bool:
    global chatLog
    messages = [
        {"role": "system", "content": system},
        {"role": "assistant", "content": chatLog},
        {"role": "user", "content": text}
    ]
    try:
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
        )
        # Access the message content correctly based on the response structure
        message_content = response.choices[0].message.content

        return "yes" in message_content.lower()
    except Exception as error:
        print("\n\n\nError:", error)
        return False
