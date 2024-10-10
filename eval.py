import os
import json
from openai import OpenAI, OpenAIError

openai_api_key = "EMPTY"  # Replace with your actual API key
openai_api_base = "http://localhost:2242/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def is_grammatically_correct(text):
    """Checks grammatical correctness (placeholder)."""
    # Implement grammatical correctness check here using a library like spaCy or NLTK
    return None  # Replace with a score or boolean value

def is_relevant(text, prompt):
    """Checks relevance to the prompt (placeholder)."""
    # Implement relevance check here using techniques like cosine similarity
    return None  # Replace with a score or boolean value

def is_creative_and_engaging(text):
    """Checks creativity and engagement (placeholder)."""
    # Implement creativity and engagement check here (challenging task)
    return None  # Replace with a score or boolean value

def is_free_of_errors(text):
    """Checks for errors and typos (placeholder)."""
    # Implement error and typo check here (e.g., using spell checking libraries)
    return None  # Replace with a score or boolean value

def is_consistent_in_style(text, prompt):
    """Checks consistency with the prompt's style and tone (placeholder)."""
    # Implement style and tone consistency check here (challenging task)
    return None  # Replace with a score or boolean value

def calculate_overall_score(scores):
    """Calculates an overall score based on individual evaluation scores."""
    # Implement a scoring mechanism (e.g., average, weighted average)
    if all(s is not None for s in scores):
        return sum(scores) / len(scores)
    else:
        return None


try:
    completion = client.completions.create(
        model="ccore/opt-125-nh",
        prompt="Once upon a time",
        temperature=1.1,
        max_tokens=50,
        extra_body={"min_p": 0.1}
    )

    print("Completion result:", completion)

    generated_text = completion.choices[0].text.strip()
    completion_tokens = completion.usage.completion_tokens
    prompt_tokens = completion.usage.prompt_tokens
    total_tokens = completion.usage.total_tokens

    print("Completion tokens:", completion_tokens)
    print("Prompt tokens:", prompt_tokens)
    print("Total tokens:", total_tokens)

    temperature = 1.1
    min_p = 0.1

    print("Temperature:", temperature)
    print("min_p:", min_p)

    print("Generated text:", generated_text)

    sentences = generated_text.split('.')
    if len(sentences) > 1:
        coherence_score = 1
        for i in range(len(sentences) - 1):
            words1 = set(sentences[i].lower().split())
            words2 = set(sentences[i+1].lower().split())
            if len(words1.intersection(words2)) == 0:
                coherence_score -= 0.2
        print("Basic Coherence Score (0-1):", coherence_score)
    else:
        print("Too few sentences for coherence check.")

    # Perform evaluations
    grammatical_score = is_grammatically_correct(generated_text)
    relevance_score = is_relevant(generated_text, "Once upon a time")
    creativity_score = is_creative_and_engaging(generated_text)
    error_score = is_free_of_errors(generated_text)
    style_score = is_consistent_in_style(generated_text, "Once upon a time")

    overall_score = calculate_overall_score([grammatical_score, relevance_score, creativity_score, error_score, style_score])

    print("Grammatical Correctness:", grammatical_score)
    print("Relevance:", relevance_score)
    print("Creativity & Engagement:", creativity_score)
    print("Errors & Typos:", error_score)
    print("Style & Tone Consistency:", style_score)
    print("Overall Score:", overall_score)


except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
except IndexError as e:
    print(f"Error accessing completion  {e}. Check API response format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

