from pydantic import BaseModel, Field
from typing import List, Optional
from agents.llm_config import get_llm

class ExtractedTask(BaseModel):
    task: str = Field(description="The description of the action item or task")
    owner: str = Field(description="The assigned owner of the task. Leave empty string if no clear owner is mentioned.")
    deadline: str = Field(description="The deadline or timeframe for the task. Leave empty string if none.")
    priority: str = Field(description="Priority: 'high', 'medium', or 'low' based on urgency words.")

class TaskExtractionOutput(BaseModel):
    tasks: List[ExtractedTask] = Field(description="List of tasks extracted from the text")

def extract_tasks(text: str) -> list:
    llm = get_llm()
    structured_llm = llm.with_structured_output(TaskExtractionOutput)
    
    prompt = f"""
    You are an AI specialized in understanding meeting transcripts and enterprise communication.
    Extract all action items from the following text.
    If a task has no explicitly mentioned owner, leave the owner field as "".
    
    Text:
    {text}
    """
    
    try:
        result = structured_llm.invoke(prompt)
        # Convert pydantic models to dicts for our workflow integration
        tasks = []
        for t in result.tasks:
            tasks.append({
                "task": t.task,
                "owner": t.owner,
                "deadline": t.deadline,
                "priority": t.priority,
            })
        return tasks
    except Exception as e:
        print(f"Error extracting tasks: {e}")
        return []