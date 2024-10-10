import os
import json
from openai import OpenAI, OpenAIError

openai_api_key = "YOUR_API_KEY"  # Replace with your actual API key
openai_api_base = "http://localhost:2242/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

prompt = "Once upon a time"
temperature = 1.1
max_tokens = 50
extra_body = {"min_p": 0.1}

for i in range(3):
    try:
        completion = client.completions.create(
            model="ccore/opt-125-nh",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            extra_body=extra_body
        )

        generated_text = completion.choices[0].text.strip()

        print(f"Story {i+1}:")
        print(generated_text)

        if i == 1:
            prompt = generated_text  # Use previous output as prompt for the middle
        elif i == 2:
            prompt = generated_text  # Use previous output as prompt for the end

    except OpenAIError as e:
        print(f"OpenAI API Error: {e}")
    except IndexError as e:
        print(f"Error accessing completion  {e}. Check API response format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
