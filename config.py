import os 
from dotenv import load_dotenv


load_dotenv()

class Config:
    OLLAMA_BASE_URL = "http://localhost:11434"
    DEFAULT_MODEL = "llama3.2:3b"
    TEMPERATURE = 0.5
    MAX_TOKENS = 4000