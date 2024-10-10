def generate_and_check_stories(prompt, max_attempts=15):
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

def generate_story(prompt):
    story = ""
    coherence_score = 0
    attempts = 0

    while coherence_score < 1.1 and attempts < max_attempts:
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

        if coherence_score < 1.1:
            print("Story coherence is low, trying again with a revised prompt...")
            prompt = generated_text  # Use previous output as prompt for the next iteration
        else:
            story += generated_text

        attempts += 1

    return story
