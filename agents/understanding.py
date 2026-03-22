import ollama
import json
import re

def extract_tasks(meeting_text):
    prompt = f"""
    Extract tasks from the meeting.

    IMPORTANT:
    - Preserve urgency/priority words like 'urgent', 'high priority'
    - Do NOT remove context words
    - If owner is missing, leave it empty

    Return ONLY JSON array.

    Format:
    [
      {{"task": "", "owner": "", "deadline": ""}}
    ]

    Meeting:
    {meeting_text}
    """

    response = ollama.chat(
        model='llama3',
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['message']['content']

    # Extract JSON safely
    match = re.search(r"\[.*\]", content, re.DOTALL)

    if match:
        json_text = match.group(0)
        try:
            return json.loads(json_text)
        except:
            print("JSON parsing failed:", json_text)
            return []
    else:
        print("No JSON found:", content)
        return []