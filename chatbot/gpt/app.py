from flask import Flask, render_template, request
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")  # Replace with your actual API key

app = Flask(__name__)

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        answer = ask_gpt(user_input)
    
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
