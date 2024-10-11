# DSPy Task Guidance Script

"""
This script will guide you through the 8 steps of using DSPy effectively.
It will interactively ask you for inputs at each step and help you define your task,
pipeline, data, metric, and optimization strategy.

Let's get started!
"""

def step1_define_task():
    print("Step 1: Define your task.")
    print("You cannot use DSPy well if you haven't defined the problem you're trying to solve.")
    print("\nExpected Input/Output Behavior:")
    print("Are you trying to build a chatbot over your data? A code assistant? A system for extracting information from papers? Or perhaps a translation system? Or a system for highlighting snippets from search results? Or a system to summarize information on a topic, with citations?")
    task_description = input("\nPlease describe your task: ")
    print("\nIt's often useful to come up with just 3-4 examples of the inputs and outputs of your program (e.g., questions and their answers, or topics and their summaries).")
    examples = []
    for i in range(1, 4):
        print(f"\nExample {i}:")
        input_example = input("Input: ")
        output_example = input("Expected Output: ")
        examples.append({'input': input_example, 'output': output_example})
    print("\nQuality and Cost Specs:")
    print("Your final system can't be too expensive to run, and it should probably respond to users quickly enough.")
    lm_choice = input("\nGuess what kind of language model you'd like to use (e.g., GPT-3.5, Mistral-7B, Llama2-13B-chat): ")
    return {
        'task_description': task_description,
        'examples': examples,
        'lm_choice': lm_choice
    }

def step2_define_pipeline():
    print("\nStep 2: Define your pipeline.")
    print("What should your DSPy program do?")
    print("Can it just be a simple chain-of-thought step?")
    print("Or do you need the LM to use retrieval?")
    print("Or maybe other tools, like a calculator or a calendar API?")
    pipeline_description = input("\nPlease describe your initial pipeline: ")
    print("\nThink about this space but always start simple.")
    print("Almost every task should probably start with just a single dspy.ChainofThought module, and then add complexity incrementally as you go.")
    return pipeline_description

def step3_explore_examples(task_info, pipeline_description):
    print("\nStep 3: Explore a few examples.")
    print("Run your examples through your pipeline.")
    print("Consider using a large and powerful LM at this point, or a couple of different LMs, just to understand what's possible.")
    print("At this point, you're still using your pipeline zero-shot, so it will be far from perfect.")
    print("Record the interesting (both easy and hard) examples you try: even if you don't have labels, simply tracking the inputs you tried will be useful for DSPy optimizers below.")
    print("\nLet's simulate running your examples through the pipeline.")
    for example in task_info['examples']:
        print(f"\nInput: {example['input']}")
        output = input("Output from pipeline (simulated): ")
        example['pipeline_output'] = output
    return task_info['examples']

def step4_define_data():
    print("\nStep 4: Define your data.")
    print("Now it's time to more formally declare your training and validation data for DSPy evaluation and optimization.")
    print("You can use DSPy optimizers usefully with as few as 10 examples, but having 50-100 examples (or even better, 300-500 examples) goes a long way.")
    print("\nDo you have a dataset prepared? (yes/no)")
    has_dataset = input()
    if has_dataset.lower() == 'yes':
        dataset_description = input("Please describe your dataset: ")
    else:
        print("You may need to collect or prepare a dataset.")
        dataset_description = "Dataset not available yet."
    return dataset_description

def step5_define_metric():
    print("\nStep 5: Define your metric.")
    print("What makes outputs from your system good or bad?")
    print("Invest in defining metrics and improving them over time incrementally.")
    print("It's really hard to consistently improve what you aren't able to define.")
    print("\nFor simple tasks, this could be just 'accuracy' or 'exact match' or 'F1 score'.")
    print("However, for most applications, your system will output long-form outputs.")
    print("There, your metric should probably be a smaller DSPy program that checks multiple properties of the output (quite possibly using AI feedback from LMs).")
    metric_description = input("\nPlease describe your metric: ")
    return metric_description

def step6_collect_evaluations():
    print("\nStep 6: Collect preliminary 'zero-shot' evaluations.")
    print("Now that you have some data and a metric, run evaluation on your pipeline before any optimizer runs.")
    print("Look at the outputs and the metric scores.")
    print("This will probably allow you to spot any major issues, and it will define a baseline for your next step.")
    print("\nSimulating evaluation...")
    print("Assuming you have collected preliminary evaluations.")
    return "Preliminary evaluations collected."

def step7_compile_with_optimizer():
    print("\nStep 7: Compile with a DSPy optimizer.")
    print("Given some data and a metric, we can now optimize the program you built.")
    print("\nDSPy includes many optimizers that do different things.")
    print("Here's the general guidance on getting started:")
    print("\n- If you have very little data, e.g. 10 examples of your task, use BootstrapFewShot")
    print("- If you have slightly more data, e.g. 50 examples of your task, use BootstrapFewShotWithRandomSearch.")
    print("- If you have more data than that, e.g. 300 examples or more, use MIPRO.")
    print("- If you have been able to use one of these with a large LM and need a very efficient program, compile that down to a small LM with BootstrapFinetune.")
    optimizer_choice = input("\nBased on your data size, which optimizer would you like to use? ")
    return optimizer_choice

def step8_iterate():
    print("\nStep 8: Iterate.")
    print("At this point, you are either very happy with everything or, more likely, you've made a lot of progress but you don't like something about the final program or the metric.")
    print("Go back to step 1 and revisit the major questions.")
    print("Iterative development is key.")
    print("\nWould you like to iterate on any of the steps? (yes/no)")
    iterate = input()
    return iterate.lower() == 'yes'

def main():
    print("Welcome to the DSPy Task Guidance Script.")
    task_info = step1_define_task()
    pipeline_description = step2_define_pipeline()
    examples_with_outputs = step3_explore_examples(task_info, pipeline_description)
    dataset_description = step4_define_data()
    metric_description = step5_define_metric()
    evaluations = step6_collect_evaluations()
    optimizer_choice = step7_compile_with_optimizer()
    need_iteration = step8_iterate()
    if need_iteration:
        print("\nPlease consider iterating on the previous steps as needed.")
    else:
        print("\nCongratulations! You have completed the initial 8 steps of using DSPy.")
    print("\nSummary of your inputs:")
    print(f"\nTask Description: {task_info['task_description']}")
    print(f"\nExamples:")
    for ex in examples_with_outputs:
        print(f"Input: {ex['input']}")
        print(f"Expected Output: {ex['output']}")
        print(f"Pipeline Output: {ex.get('pipeline_output', 'Not provided')}\n")
    print(f"Language Model Choice: {task_info['lm_choice']}")
    print(f"\nPipeline Description: {pipeline_description}")
    print(f"\nDataset Description: {dataset_description}")
    print(f"\nMetric Description: {metric_description}")
    print(f"\nOptimizer Choice: {optimizer_choice}")
    print("\nThank you for using the DSPy Task Guidance Script.")

if __name__ == "__main__":
    main()
