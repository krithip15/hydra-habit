from ollama import chat

response = chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": "Explain hydration in one simple sentence.",
        }
    ],
)

print(response.message.content)
