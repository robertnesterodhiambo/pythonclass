import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")  # Replace with your actual API key

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # Change to "gpt-3.5-turbo" if needed
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    user_input = input("Ask ChatGPT: ")
    answer = ask_gpt(user_input)
    print("ChatGPT:", answer)
