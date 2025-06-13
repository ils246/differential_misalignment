import pandas as pd
import os
from functions import load_answer
import ast
import sys


results_path = 'data/results/'


if __name__ == '__main__':

    COUNTRIES = ast.literal_eval(sys.argv[1])  # Convert string to list
    SHEET_NAME = sys.argv[2]
    MODEL_NAME = sys.argv[3]
    MODEL = sys.argv[4]
    
    if SHEET_NAME == 'mapping':
        sheet_name = 'scoring'
    elif SHEET_NAME == 'mapping_r1':
        sheet_name = 'scoring_r1'
    else:
        sheet_name = 'scoring_r2'
    # Scoring
    scores = pd.read_excel("not_touch/mapping_CENSORSHIP.xlsx", sheet_name = sheet_name)


    # IMPORTING ALL THE DATA
    all_dicts = []
    for file in os.listdir(results_path):
        
        country = file.split('_')[0]

        data_CENSORSHIP_MC = load_answer(os.path.join(results_path, file))

        temp_dict = { 
            'model' : MODEL,
            'country' : country,
            'ids' : [],
            'scores' : [],
            'categories' : [],
        }

        for d in data_CENSORSHIP_MC:

            id = d['id']
            ans = d['orginal_mapped']

            try: 
                score = scores[scores.id == id][ans].iloc[0] 
            except:
                score = -1 # NON RESPONSE

            category = scores[scores.id == id]['category'].iloc[0] 
            temp_dict['ids'].append(id)
            temp_dict['scores'].append(score)
            temp_dict['categories'].append(category)
        
        all_dicts.append(temp_dict)

    df_full = pd.concat([pd.DataFrame(data) for data in all_dicts])
    df_full.to_csv(f'data/final_{MODEL}_{SHEET_NAME}.csv')

