import sys 
import ast
from functions import load_answers, save_answers_json
import pandas as pd
import re
import os

def extract_lone_specific_capitals(text):
    # Match only the specific capital letters A, B, C, D, or E when they stand alone
    matches = re.findall(r'\b[A-E]\b', text)
    return matches

def get_correct_mapping(question):
    """
    Questa funzione mi serve per il mapping delle shuffled answers
    """
    choices = list(question.values())[2:-1]
    ans_keys = [f"ans{i+1}" for i, choice in enumerate(choices)]
    if len(choices) != 5:
        print('There is an error with the amount of possible answers.')
    choices = [(c,ans) for c,ans in zip(choices,ans_keys) if pd.notna(c)]

    mapping = {}
    for i, choice in enumerate(choices):
        key_value = f"{chr(65 + i)}"
        mapping[key_value] = choice[1]
    return mapping

def process_answers(answers, questions):
    """
    Questa funzione mi serve per processare le risposte.
    """ 
    i = 0
    for ans in answers:

        and_id = ans['id']

        for quest in questions:
            mapping = get_correct_mapping(quest)

            if quest['id'] == and_id: # Se matchano
                    
                mapped_ans_orginal = extract_lone_specific_capitals(ans['orginal'])
                if mapped_ans_orginal == []:
                    mapped_ans_orginal = ['Non response']
                    i+=1

                try:
                    ans['orginal_mapped'] = mapping[mapped_ans_orginal[0]] # Storing
                except:
                    ans['orginal_mapped'] = "Non Reponse" # Storing

    print(i)

if __name__ == '__main__':

    COUNTRIES = ast.literal_eval(sys.argv[1])  # Convert string to list
    SHEET_NAME = sys.argv[2]
    MODEL_NAME = sys.argv[3]
    MODEL = sys.argv[4]

    questions = pd.read_excel("not_touch/mapping_CENSORSHIP.xlsx", sheet_name = SHEET_NAME)
    questions = questions.to_dict(orient="records")

    # Iterate over all combinations
    for country in COUNTRIES:
        
        answers = load_answers(f'data/export_{MODEL}/{country}/')

        process_answers(answers = answers, questions = questions)
        print(country)

        os.makedirs('data/results/', exist_ok=True)
        save_answers_json(filename = f'data/results/{country}_CENSORSHIP.json', answers_dict = answers)
