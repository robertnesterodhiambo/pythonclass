from flask import Flask, render_template, request
import openai
import os
import fitz  # PyMuPDF for PDF text extraction
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)

# Path to the PDF folder
PDF_FOLDER = "/home/dragon/GIT/pythonclass/chatbot/gpt/pdfs"

# Store chat history
chat_history = []

def extract_text_from_pdfs():
    """Extract text from all PDFs in the specified folder."""
    text_content = ""
    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, filename)
            with fitz.open(pdf_path) as pdf:
                for page in pdf:
                    text_content += page.get_text("text") + "\n"
    return text_content

# Load all PDF text at startup
pdf_text = extract_text_from_pdfs()

def ask_gpt(prompt, pdf_context=""):
    """Function to get a response from OpenAI's GPT model, using PDF context if provided."""
    try:
        # Combine user query with PDF text
        full_prompt = f"Using the following document information:\n{pdf_context[:2000]}\n\nAnswer this: {prompt}"  # Limit to 2000 chars for efficiency
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-instruct-0914",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content, None
    except openai.APIError as e:
        return None, f"API Error: {str(e)}"
    except openai.OpenAIError as e:
        return None, f"OpenAI Error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history
    error = None

    if request.method == "POST":
        user_input = request.form["user_input"]
        response, error = ask_gpt(user_input, pdf_text)

        if response:
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "chatgpt", "content": response})

    return render_template("index.html", messages=chat_history, error=error)

if __name__ == "__main__":
    app.run(debug=True)
