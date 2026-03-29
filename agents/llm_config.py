import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

_llm_instance = None

def get_llm():
    """
    Returns a singleton LLM instance.
    Switched to Groq (Llama-3.3-70b) for absolutely free, unthrottled, region-independent API access.
    """
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. "
            "Please add it to the Render Environment Variables."
        )

    # === ACTIVE: Groq Llama 3 ===
    _llm_instance = ChatGroq(
        model="llama-3.3-70b-versatile",
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
