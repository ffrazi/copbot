import requests
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# ---- CONFIGURATION ----
OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama server URL
USE_LOCAL_LLAMA = False  # Set to True if you want to use LLaMA 2 instead of Ollama

# ---- LOAD LLaMA 2 MODEL (Only if using local mode) ----
if USE_LOCAL_LLAMA:
    print("Loading LLaMA 2 model... (This may take time)")
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

# ---- FUNCTION TO GET RESPONSE FROM MISTRAL (OLLAMA) ----
def get_ollama_response(prompt):
    """
    Sends a prompt to the Mistral model running on Ollama and returns a response.
    """
    payload = {
        "model": "mistral",  # Ensure "mistral" is downloaded in Ollama
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(OLLAMA_URL, json=payload, headers=headers)
        response_data = response.json()
        return response_data.get("response", "Sorry, I couldn't generate a response.")
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

# ---- FUNCTION TO GET RESPONSE FROM LLaMA 2 ----
def get_llama_response(prompt):
    """
    Generates a response using a locally running LLaMA 2 model.
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ---- CHAT LOOP ----
if __name__ == "__main__":
    print("🤖 Start chatting! Type 'exit' to end the conversation.")
    conversation_history = ""

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("👋 Ending conversation.")
            break

        # Maintain conversation history
        conversation_history += f"User: {user_input}\n"

        # Choose model dynamically
        if USE_LOCAL_LLAMA:
            response = get_llama_response(conversation_history)
        else:
            response = get_ollama_response(conversation_history)

        conversation_history += f"Chatbot: {response}\n"
        print(f"Chatbot: {response}")
