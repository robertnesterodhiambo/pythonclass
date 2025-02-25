from llama_cpp import Llama

# Path to your downloaded GGUF model
MODEL_PATH = "/home/dragon/Downloads/llama-2-7b.Q2_K.gguf"

# Load the model
llm = Llama(model_path=MODEL_PATH)

# Generate response
response = llm("Q: What is the capital of France?\nA:")

# Print response
print(response["choices"][0]["text"].strip())  # Strip to remove extra spaces/newlines
