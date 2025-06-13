import pandas as pd
import json
from functions import transform_dict_values
import sys
import ast

def format_question_with_choices(question: str, choices: list) -> str:
    """
    Generates a formatted prompt with a question and multiple-choice answers.
    
    Parameters:
    question (str): The question text.
    choices (list): A list of answer choices.
    
    Returns:
    str: A formatted string with the question and answer choices.
    """
    choices_str = "\n".join([f"{chr(65 + i)} - {choice}" for i, choice in enumerate(choices)])
    prompt = f"""Question: {question}

Choices:
{choices_str}

Answer: 
"""
    return prompt

if __name__ == '__main__':

    COUNTRIES = ast.literal_eval(sys.argv[1])  
    SHEET_NAME = sys.argv[2]
    MODEL_NAME = sys.argv[3]
    MODEL = sys.argv[4]

    mapping = pd.read_excel(f'not_touch/mapping_CENSORSHIP.xlsx', sheet_name = SHEET_NAME) # Mapping
    mapping['all_answers'] = mapping[['ans1', 'ans2', 'ans3', 'ans4', 'ans5']].apply(
        lambda x: [str(ans).strip().replace('\n', '') for ans in x if pd.notna(ans) and str(ans).strip()], axis=1
    )

    for country in COUNTRIES:
        # DATA IMPORT
        with open(f'not_touch/CENSORSHIP.json', "r", encoding="utf-8") as file:
            data = json.load(file)
        
        data_ = [transform_dict_values(d, country=country) for d in data]

        all_mapped_ids = mapping.id.tolist() 
        final = []
        for d in data_: 

            temp_dict = {} 
            if d['id'] in all_mapped_ids:
                
                answers = mapping[mapping.id == d['id']].all_answers.iloc[0] 
                temp_dict['id'] = d['id'] 
                temp_dict['orginal'] = format_question_with_choices(d['orginal'], answers) # generot tutti i prompt
                final.append(temp_dict)

            output_file =  f"data/prompt_{country.replace(" ", "_")}_CENSORSHIP_MC.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(final, f, indent=4, ensure_ascii=False)

