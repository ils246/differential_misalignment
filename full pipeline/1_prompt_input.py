import json
import os
import ast
import sys


# ** Step 1: Load Paraphrased Prompts from JSON **
def load_paraphrases(filename="./data/paraphrases.json"):
    """Load paraphrases from a JSON file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


# ** Step 2: Flatten all th inputs
def flatten_dict(input_dict):
    """Flattens a dictionary into a list of strings while maintaining an index map."""
    flattened_list = []
    index_map = {}  # To store positions for reconstructing
    
    for key, value in input_dict.items():
        if isinstance(value, list):  # If value is a list of strings
            index_map[key] = (len(flattened_list), len(flattened_list) + len(value))
            flattened_list.extend(value)
        elif isinstance(value, str):  # If value is a single string
            index_map[key] = (len(flattened_list), len(flattened_list) + 1)
            flattened_list.append(value)
        else:  # Keep non-string values (like 'id') unchanged
            index_map[key] = value
    
    return flattened_list, index_map


# Step 4: Reshape output
def reshape_output(flattened_list, index_map):
    """Reshapes a flattened list back into the original dictionary structure using the index map."""
    output_dict = {}
    
    for key, value in index_map.items():
        if isinstance(value, tuple):  # If it's a range, it's a list or string
            start, end = value
            if end - start == 1:
                output_dict[key] = flattened_list[start]  # Single string
            else:
                output_dict[key] = flattened_list[start:end]  # List of strings
        else:  # Directly copy unchanged values
            output_dict[key] = value
    
    return output_dict


def generate_jsonl(prompts, output_filepath="data/input.jsonl",
                    model_name="gpt-4", temperature=0.8, max_tokens=500):
    """
    Generates a JSONL file for OpenAI's Chat Completions API from a list of prompts.

    Parameters:
    - prompts (list): List of text prompts.
    - output_filepath (str): Path where the JSONL file will be saved.
    - model_name (str): Model to use for the API (default: "gpt-4").
    - temperature (float): Sampling temperature for randomness (default: 0.8).
    - max_tokens (int): Maximum number of tokens in response (default: 500).
    """
    system_message = "You are a concise assistant. Always answer with only the letter corresponding to the correct answer choice, without any explanations or additional text."
    max_tokens = 2

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    with open(output_filepath, "w", encoding="utf-8") as f:
        for prompt in prompts:
            request_data = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            json.dump(request_data, f)
            f.write("\n")  # Ensure newline separation for JSONL format

    print(f"JSONL file successfully created at: {output_filepath}")


def filter_keys(all_prompts, selected_keys):
    """
    Filters a list of dictionaries, retaining only the specified keys in each dictionary.
    
    Parameters:
    - all_prompts (list of dict): The list of dictionaries to filter.
    - selected_keys (list of str): The keys to retain in each dictionary.
    
    Returns:
    - list of dict: A new list of dictionaries with only the selected keys.
    """
    return [{k: d[k] for k in selected_keys if k in d} for d in all_prompts]


if __name__ == '__main__':
    
    COUNTRIES = ast.literal_eval(sys.argv[1])  
    SHEET_NAME = sys.argv[2]
    MODEL_NAME = sys.argv[3]
    MODEL = sys.argv[4]


    for country in COUNTRIES:
        input_path = f"data/prompt_{country.replace(" ", "_")}_CENSORSHIP_MC.json"
        all_prompts = load_paraphrases(input_path)  
        all_prompts = filter_keys(all_prompts, selected_keys = ['id',  'orginal'])
        initial_list = []
        for p in all_prompts:
            flatten_input, structure = flatten_dict(p)
            initial_list.extend(flatten_input)
        generate_jsonl(initial_list, output_filepath=f"data/input_{country.replace(" ", "_")}_CENSORSHIP_MC.jsonl", model_name = MODEL_NAME)