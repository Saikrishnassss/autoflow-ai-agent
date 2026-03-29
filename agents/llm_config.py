import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

_llm_instance = None

def get_llm():
    """
    Returns a singleton LLM instance.
    Default: OpenAI GPT-4o for reliable structured output and reasoning.
    
    To swap to local Ollama (LLaMA3), uncomment the alternative below.
    """
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY not found. "
            "Create a .env file with: OPENAI_API_KEY=sk-..."
        )

    # === PRIMARY: OpenAI GPT-4o-mini ===
    _llm_instance = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        request_timeout=60,
    )

    # === ALTERNATIVE: Local Ollama LLaMA3 (uncomment to use) ===
    # _llm_instance = ChatOpenAI(
    #     base_url="http://localhost:11434/v1",
    #     api_key="ollama",
    #     model="llama3",
    #     temperature=0.0,
    # )

    return _llm_instance
