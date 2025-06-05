import requests



try:
    response = requests.get("http://localhost:11434/api/tags")
    print("Ollama connection: SUCCESS")
    print(response.json())
except:
    print("Ollama connection: FAILED")