from flask import Flask, render_template, request
import openai

# Initialize OpenAI client
api_key = "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"  # Replace with your actual API key
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)

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
    answer = None
    error = None

    if request.method == "POST":
        user_input = request.form["user_input"]
        answer, error = ask_gpt(user_input)  # Get answer & error message

    return render_template("index.html", answer=answer, error=error)

if __name__ == "__main__":
    app.run(debug=True)
