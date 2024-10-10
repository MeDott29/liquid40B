from openai import OpenAI
from os import getenv

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "https://www.thoughtflux.io",  # Optional, for including your app on openrouter.ai rankings.
    "X-Title": "ThoughtFluxAI",  # Optional. Shows in rankings on openrouter.ai.
  },
  model="liquid/lfm-40b",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)
