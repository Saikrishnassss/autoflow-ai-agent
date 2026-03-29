import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

_llm_instance = None

def get_llm():
    """
    Returns a singleton LLM instance.
    Switched to Google Gemini 1.5 Pro to bypass OpenAI billing limits.
    """
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY not found. "
            "Please add it to the Render Environment Variables."
        )

    # === ACTIVE: Google Gemini ===
    _llm_instance = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.0,
        request_timeout=60,
    )

    return _llm_instance

    # === ALTERNATIVE: Local Ollama LLaMA3 (uncomment to use) ===
    # _llm_instance = ChatOpenAI(
    #     base_url="http://localhost:11434/v1",
    #     api_key="ollama",
    #     model="llama3",
    #     temperature=0.0,
    # )

    return _llm_instance
