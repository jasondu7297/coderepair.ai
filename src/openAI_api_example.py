from openai import OpenAI

client = OpenAI(api_key='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')




PROMPT = "You are a helpful assistant"

messages = [
    {"role": "system", "content": PROMPT},
    {"role": "user", "content": "What is the Boston Redsox's record in 2022"}
]

# Start a conversation
response = client.chat.completions.create(model="gpt-4-turbo-preview",  # Use the correct model identifier
messages=messages
)

print(response.choices[0].message.content)
messages.append({"role": "user", "content": "What were they ranked in their conference"})
# Continue the conversation
response = client.chat.completions.create(model="gpt-4-turbo-preview",
messages=messages
)

print(response.choices[0].message.content)