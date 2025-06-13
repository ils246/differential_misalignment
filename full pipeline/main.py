import subprocess
import os
import os
import shutil

# Define directory
dir_path = "data/"

if __name__ == '__main__':
    COUNTRIES = {'Bahrain',} # countries of interest
    SHEET_NAME = 'mapping_r1' # mapping, mapping_r1, mapping_r2, 
    MODEL_NAME = 'deepseek-chat' # Name of the model
    MODEL = "DEEPSEEK" # ID of the model
    API_KEY = 'api key' # api key
    END_POINT = 'https://api.deepseek.com/v1/chat/completions' #endpoint

    max_requests_per_minute = 1500
    max_tokens_per_minute = 100000

    # CREO LA CARTELLA DATA
    if os.path.exists('data/'):
        shutil.rmtree('data/')  # Delete the entire folder and its contents
    os.makedirs('data/', exist_ok=True)
    
    scripts_to_iterate = ['0_prompt_creation.py', '1_prompt_input.py']

    for script in scripts_to_iterate:
        command = ['python', script, str(COUNTRIES), SHEET_NAME, MODEL_NAME, MODEL] 
        subprocess.run(command)

    # ASNWERS GENERATION
    base_command = (
        "set OPENAI_API_KEY= {api_key} && "
        "python 2_multi_call_API.py "
        "--requests_filepath data/input_{country}_CENSORSHIP_MC.jsonl "
        "--save_filepath data/output_{country}_CENSORSHIP_MC.jsonl "
        "--request_url {end_point} "
        "--max_requests_per_minute {max_requests_per_minute}  "
        "--max_tokens_per_minute {max_tokens_per_minute}  "
        "--token_encoding_name cl100k_base "
        "--max_attempts 5 "
        "--logging_level 20"
    )

    for country in COUNTRIES:
        command = base_command.format(country=country.replace(" ", "_"), api_key = API_KEY, end_point = END_POINT, max_requests_per_minute = max_requests_per_minute, max_tokens_per_minute = max_tokens_per_minute)
        subprocess.run(command, shell=True, check=True) 

    # ORGANIZE ANSWERS
    command = ['python', '3_organize_answers.py', str(COUNTRIES), SHEET_NAME, MODEL_NAME, MODEL]
    subprocess.run(command)

    # MAPPING SCORES
    command = ['python', '4_mapping.py', str(COUNTRIES), SHEET_NAME, MODEL_NAME, MODEL]
    subprocess.run(command)
        
    # STATA
    command = ['python', '5_get_stata.py', str(COUNTRIES), SHEET_NAME, MODEL_NAME, MODEL]
    subprocess.run(command)