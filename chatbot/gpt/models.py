import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")  # Replace with your actual API key)

models = client.models.list()
for model in models.data:
    print(model.id)