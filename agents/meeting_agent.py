import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_tasks(meeting_text):
    prompt = f"""
You are an AI assistant. Extract actionable tasks from the meeting notes.

For each task, return:
- task_name
- assigned_to (if not mentioned, put "Unassigned")
- deadline (if not mentioned, put "Not specified")

Return output in JSON format.

Meeting Notes:
{meeting_text}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash-8b",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    sample_meeting = """
Team meeting:
- Sai will complete UI by Friday
- Ravi handles backend by Saturday
- Testing should be done by Sunday
"""

    result = extract_tasks(sample_meeting)
    print(result)