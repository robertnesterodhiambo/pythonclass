from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)

# Store chat history in a list
chat_history = []

def ask_gpt(prompt):
    """Function to get a response from OpenAI's GPT model, with error handling."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content, None  # Return response and no error
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
        response, error = ask_gpt(user_input)

        if response:
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "chatgpt", "content": response})

    return render_template("index.html", messages=chat_history, error=error)

if __name__ == "__main__":
    app.run(debug=True)
