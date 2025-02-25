import os
from llama_cpp import Llama
import PyPDF2

# Path to your local LLaMA model (GGUF format)
MODEL_PATH = "/home/dragon/Downloads/llama-2-7b.Q2_K.gguf"

# Folder containing PDFs
PDF_FOLDER = "/home/dragon/Bob/pythonclass/chatbot/pdfs"

# Load LLaMA model
llm = Llama(model_path=MODEL_PATH)

def extract_text_from_pdfs(pdf_folder):
    """Extracts text from all PDFs in a folder and combines them into one document."""
    text = ""
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            with open(os.path.join(pdf_folder, file), "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
    return text.strip()

# Extract text from PDFs
pdf_text = extract_text_from_pdfs(PDF_FOLDER)

def find_relevant_text(question, text, chunk_size=400):
    """Finds the most relevant part of the text using a sliding window approach."""
    sentences = text.split(". ")  # Split text into sentences
    best_chunk = ""
    best_score = 0

    for i in range(0, len(sentences), 5):  # Move in steps of 5 sentences
        chunk = ". ".join(sentences[i:i+chunk_size])
        score = sum(1 for word in question.split() if word.lower() in chunk.lower())

        if score > best_score:
            best_score = score
            best_chunk = chunk

    return best_chunk[:chunk_size]  # Ensure the final chunk is within the token limit

def ask_question(question):
    """Finds the most relevant chunk and asks a question based on it."""
    relevant_text = find_relevant_text(question, pdf_text, chunk_size=400)

    if not relevant_text:
        return "I couldn't find relevant information in the document."

    prompt = f"Using the following information from a document, answer the question:\n\n{relevant_text}\n\nQuestion: {question}\nAnswer:"
    response = llm(prompt, max_tokens=100)  # Keep max_tokens low to stay within limits
    return response["choices"][0]["text"].strip()

# Interactive Q&A
while True:
    user_question = input("\nAsk a question (or type 'exit' to quit): ")
    if user_question.lower() == "exit":
        break
    answer = ask_question(user_question)
    print("\nAnswer:", answer)
