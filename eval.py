import os
import json
from openai import OpenAI, OpenAIError
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from difflib import SequenceMatcher

try:
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
except LookupError as e:
    print(f"Error: {e}. Please download required NLTK resources.")
    exit()

openai_api_key = "EMPTY"  # Replace with your actual API key
openai_api_base = "http://localhost:2242/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

stop_words = set(stopwords.words('english'))

def is_grammatically_correct(text):
    """Rudimentary grammatical correctness check (using simple sentence length)."""
    sentences = text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    # A very basic heuristic: shorter sentences are considered more grammatically correct (this is a simplification!)
    return max(0, 1 - (avg_sentence_length - 15) / 30)  # Scale to 0-1

def is_relevant(text, prompt):
    """Rudimentary relevance check (using word overlap)."""
    prompt_words = set(word_tokenize(prompt.lower())) - stop_words
    text_words = set(word_tokenize(text.lower())) - stop_words
    overlap = len(prompt_words.intersection(text_words))
    return overlap / max(len(prompt_words), len(text_words)) if max(len(prompt_words), len(text_words)) > 0 else 0

def is_creative_and_engaging(text):
    """Rudimentary creativity and engagement check (using sentence length variation)."""
    sentences = text.split('.')
    sentence_lengths = [len(s.split()) for s in sentences]
    if not sentence_lengths:
        return 0
    std_dev = (sum([(x - sum(sentence_lengths) / len(sentence_lengths))**2 for x in sentence_lengths]) / len(sentence_lengths))**0.5
    # A very basic heuristic: more variation in sentence length is considered more engaging (this is a simplification!)
    return min(1, std_dev / 5)

def is_free_of_errors(text):
    """Rudimentary error check (currently returns 1, needs improvement)."""
    # Placeholder:  This needs a proper spell checker and grammar checker integration.
    return 1

def is_consistent_in_style(text, prompt):
    """Rudimentary style consistency check (using similarity score)."""
    return SequenceMatcher(None, prompt.lower(), text.lower()).ratio()

def calculate_overall_score(scores):
    """Calculates an overall score based on individual evaluation scores."""
    if all(s is not None for s in scores):
        return sum(scores) / len(scores)
    else:
        return None

try:
    for i in range(5):
        completion = client.completions.create(
            model="ccore/opt-125-nh",
            prompt="Once upon a time",
            temperature=1.1,
            max_tokens=50,
            extra_body={"min_p": 0.1}
        )

        print(f"Completion result {i+1}:", completion)

        generated_text = completion.choices[0].text.strip()
        completion_tokens = completion.usage.completion_tokens
        prompt_tokens = completion.usage.prompt_tokens
        total_tokens = completion.usage.total_tokens

        print(f"Completion tokens {i+1}:", completion_tokens)
        print(f"Prompt tokens {i+1}:", prompt_tokens)
        print(f"Total tokens {i+1}:", total_tokens)

        temperature = 1.1
        min_p = 0.1

        print(f"Temperature {i+1}:", temperature)
        print(f"min_p {i+1}:", min_p)

        print(f"Generated text {i+1}:", generated_text)

        sentences = generated_text.split('.')
        if len(sentences) > 1:
            coherence_score = 1
            for j in range(len(sentences) - 1):
                words1 = set(sentences[j].lower().split())
                words2 = set(sentences[j+1].lower().split())
                if len(words1.intersection(words2)) == 0:
                    coherence_score -= 0.2
            print(f"Basic Coherence Score (0-1) {i+1}:", coherence_score)
        else:
            print(f"Too few sentences for coherence check {i+1}.")

        # Perform evaluations
        grammatical_score = is_grammatically_correct(generated_text)
        relevance_score = is_relevant(generated_text, "Once upon a time")
        creativity_score = is_creative_and_engaging(generated_text)
        error_score = is_free_of_errors(generated_text)
        style_score = is_consistent_in_style(generated_text, "Once upon a time")

        overall_score = calculate_overall_score([grammatical_score, relevance_score, creativity_score, error_score, style_score])

        print(f"Grammatical Correctness {i+1}:", grammatical_score)
        print(f"Relevance {i+1}:", relevance_score)
        print(f"Creativity & Engagement {i+1}:", creativity_score)
        print(f"Errors & Typos {i+1}:", error_score)
        print(f"Style & Tone Consistency {i+1}:", style_score)
        print(f"Overall Score {i+1}:", overall_score)

except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
except IndexError as e:
    print(f"Error accessing completion  {e}. Check API response format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
