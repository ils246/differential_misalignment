import json
import os
import sys
import ast

def save_answers_json(filename, answers_dict):
    """Save generated answers as a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(answers_dict, file, indent=4, ensure_ascii=False)

# ** Step 1: Load Paraphrased Prompts from JSON **
def load_paraphrases(filename="./data/paraphrases.json"):
    """Load paraphrases from a JSON file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

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

    COUNTRIES = ast.literal_eval(sys.argv[1])  # Convert string to list
    SHEET_NAME = sys.argv[2]
    MODEL_NAME = sys.argv[3]
    QUESTION_TYPE = sys.argv[4]


    for country in COUNTRIES:

        # Input and output
        input_path = f'data/output_{country.replace(" ", "_")}_CENSORSHIP_MC.jsonl'
        out_path = f'data/export_{QUESTION_TYPE}/{country}'  
        os.makedirs(out_path, exist_ok=True)  # Ensure output directory exists
        
        # Read the file
        with open(input_path, "r", encoding="utf-8") as file:
            data = [json.loads(line) for line in file]
        
        input_path = f"data/prompt_{country.replace(" ", "_")}_CENSORSHIP_MC.json"
        all_prompts = load_paraphrases(input_path)  # Load paraphrased prompts
        all_prompts = filter_keys(all_prompts, selected_keys = ['id', 'orginal'])

        # Dizionario con domanda e rispsota
        ans_dict = {}
        rate_limit_count = 0

        for d in data:
            try:
                ans_dict[d[0]['messages'][1]['content']] = d[1]['choices'][0]['message']['content']
            except Exception:
                ans_dict[d[0]['messages'][1]['content']] = 'rate limits'
                rate_limit_count += 1
        print(f"Rate limits encountered: {rate_limit_count}")
        
        # Ricostruisco struttura originale
        final = []
        for prompt in all_prompts:
            new_dict = {
                'id': prompt['id'],
                'orginal': ans_dict[prompt['orginal']],
            }
            final.append(new_dict)

        # Export
        for i in final:
            save_path = os.path.join(out_path, f"{i['id']}.json")
            save_answers_json(save_path, i)