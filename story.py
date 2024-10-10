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

def generate_story(prompt):
    coherence_score = 0
    while coherence_score < 0.8:
        completion = client.completions.create(
            model="ccore/opt-125-nh",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            extra_body=extra_body
        )

        generated_text = completion.choices[0].text.strip()
        sentences = generated_text.split('.')
        coherence_score = check_coherence(sentences)

        if coherence_score < 0.8:
            print("Story coherence is low, trying again with a revised prompt...")
            prompt = generated_text  # Use previous output as prompt for the next iteration

    return generated_text

def check_coherence(story):
    sentences = story.split('.')
    if len(sentences) > 1:
        coherence_score = 1
        for j in range(len(sentences) - 1):
            words1 = set(sentences[j].lower().split())
            words2 = set(sentences[j+1].lower().split())
            if len(words1.intersection(words2)) == 0:
                coherence_score -= 0.2
        return coherence_score
    else:
        return 0

def generate_and_check_stories(prompt, max_attempts=3):
    for i in range(max_attempts):
        try:
            story = generate_story(prompt)
            print(f"Story {i+1}:")
            print(story)

            # Check coherence and adjust prompt if needed (you can add more sophisticated logic here)
            coherence = check_coherence(story)
            print(f"Coherence Score: {coherence}")
            if i == 1:
                prompt = story  # Use previous output as prompt for the middle
            elif i == 2:
                prompt = story  # Use previous output as prompt for the end

        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
        except IndexError as e:
            print(f"Error accessing completion  {e}. Check API response format.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

generate_and_check_stories(prompt)
