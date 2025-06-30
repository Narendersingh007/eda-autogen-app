
import openai
from openai import OpenAI

client = OpenAI(api_key="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")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)

print(response.choices[0].message.content)