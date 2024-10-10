import os
import json
from openai import OpenAI, OpenAIError

openai_api_key = "EMPTY"  # Replace with your actual API key
openai_api_base = "http://localhost:2242/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

try:
    completion = client.completions.create(
        model="ccore/opt-125-nh",
        prompt="Once upon a time",
        temperature=1.1,
        max_tokens=50,
        extra_body={"min_p": 0.1}
    )

    print("Completion result:", completion)

    # Analyze the completion result
    generated_text = completion.choices[0].text.strip()
    #Use the correct token counting method provided by the API response.
    completion_tokens = completion.usage.completion_tokens
    prompt_tokens = completion.usage.prompt_tokens
    total_tokens = completion.usage.total_tokens

    print("Completion tokens:", completion_tokens)
    print("Prompt tokens:", prompt_tokens)
    print("Total tokens:", total_tokens)

    # Access temperature from the request parameters, not the response.
    temperature = 1.1 #This should match the value set in the request.  Could be retrieved from a variable if set dynamically.
    min_p = completion.extra_body["min_p"]

    print("Temperature:", temperature)
    print("min_p:", min_p)

    print("Generated text:", generated_text)

    # Basic coherence check (can be significantly improved)
    sentences = generated_text.split('.')
    if len(sentences) > 1:
        coherence_score = 1  # Assume coherent initially
        for i in range(len(sentences) - 1):
            # Simple check:  Do sentences share any words?
            words1 = set(sentences[i].lower().split())
            words2 = set(sentences[i+1].lower().split())
            if len(words1.intersection(words2)) == 0:
                coherence_score -= 0.2  # Reduce score if no word overlap
        print("Basic Coherence Score (0-1):", coherence_score)
    else:
        print("Too few sentences for coherence check.")


except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
except IndexError as e:
    print(f"Error accessing completion  {e}. Check API response format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

