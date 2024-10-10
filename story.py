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
coherence_threshold = 0.8
max_attempts = 5
max_sentences = 5

def generate_story(prompt):
    story = ""
    coherence_score = 0
    attempts = 0

    while coherence_score < coherence_threshold and attempts < max_attempts:
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

        if coherence_score < coherence_threshold:
            print("Story coherence is low, trying again with a revised prompt...")
            prompt = generated_text  # Use previous output as prompt for the next iteration
        else:
            story += generated_text

        attempts += 1

    return story

def check_coherence(story):
    if len(story) > 1:
        coherence_score = 1
        for j in range(len(story) - 1):
            words1 = set(story[j].lower().split())
            words2 = set(story[j+1].lower().split())
            if len(words1.intersection(words2)) == 0:
                coherence_score -= 0.2
        return coherence_score
    else:
        return 0.5  # Assign a default coherence score for single-sentence stories

def generate_and_check_stories(prompt, max_attempts=3):
    for i in range(max_attempts):
        try:
            story = generate_story(prompt)
            print(f"Story {i+1}:")
            print(story)

            # Check coherence and adjust prompt if needed (you can add more sophisticated logic here)
            coherence = check_coherence(story.split('.'))
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

def research_topic(topic):
    research_topics = []
    attempts = 0

    while len(research_topics) < 5 and attempts < max_attempts:
        try:
            completion = client.completions.create(
                model="ccore/opt-125-nh",
                prompt=topic,
                temperature=temperature,
                max_tokens=max_tokens,
                extra_body=extra_body
            )

            generated_text = completion.choices[0].text.strip()
            sentences = generated_text.split('.')
            coherence_score = check_coherence(sentences)

            if coherence_score < coherence_threshold:
                print("Research topic coherence is low, trying again with a revised prompt...")
                topic = generated_text  # Use previous output as prompt for the next iteration
            else:
                research_topics.append(generated_text)

            attempts += 1

        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
        except IndexError as e:
            print(f"Error accessing completion  {e}. Check API response format.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return research_topics

generate_and_check_stories(prompt)
