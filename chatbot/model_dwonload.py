from huggingface_hub import hf_hub_download

# Download Llama 2 model
model_path = hf_hub_download(
    repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
    filename="llama-2-7b-chat.Q4_K_M.gguf",  # Change this based on the quantization you want
    local_dir="./models",  # Save the model in the 'models' directory
)

print(f"Model downloaded to: {model_path}")
