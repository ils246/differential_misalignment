
from flashtext import KeywordProcessor
import json 
import os

def load_answer(filename):
    """Load answers from a JSON file and return the data as a dictionary."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

def load_answers(path):

    data = []
    for file in os.listdir(path):
        d = load_answer(filename = os.path.join(path,file))
        d['id'] = int(file.split('.')[0])
        data.append(d)
    return data

# Processing all the dict
def transform_dict_values(data, country = 'China'):
    """
    Applies remove_number_prefix and replace_country_phrases to all strings in a dict.
    If a value is a list of strings, it applies the functions to each string in that list.
    Any other data types remain unchanged.

    Args:
        data (dict): A dictionary with string or list-of-string values.

    Returns:
        dict: A new dictionary with transformed values.
    """
    keyword_processor_0 = KeywordProcessor(case_sensitive=False)
    keyword_dict_0 = {
        country: ["your nation","your country","your state","your homeland","your territory","your jurisdiction","your borders","your area"],
        }

    keyword_processor_1 = KeywordProcessor(case_sensitive=False)
    keyword_dict_1 = {
        country: ["nation","country","homeland","territory","jurisdiction","borders","area"], 
        }
    keyword_processor_0.add_keywords_from_dict(keyword_dict_0)
    keyword_processor_1.add_keywords_from_dict(keyword_dict_1)


    transformed = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Apply transformations to a single string
            original_value = value
            final_value = keyword_processor_1.replace_keywords(keyword_processor_0.replace_keywords(original_value))
            # Check if any change occurred
            if final_value == original_value:
                final_value = f"In {country}, {final_value.lower()}"
            transformed[key] = final_value
            
        elif isinstance(value, list):
            # Apply transformations to each element if it's a string
            new_list = []
            for item in value:
                if isinstance(item, str):
                    original_value = item
                    final_value = keyword_processor_1.replace_keywords(keyword_processor_0.replace_keywords(original_value))
                    if final_value == original_value:
                        final_value = f"In {country}, {final_value.lower()}"
                    new_list.append(final_value)
                else:
                    # If it's not a string, leave it unchanged
                    new_list.append(item)
            transformed[key] = new_list
        else:
            # Leave other data types unchanged
            transformed[key] = value

    return transformed


# ** Step 3: Save answers in JSON format **
def save_answers_json(filename, answers_dict):
    """Save generated answers as a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(answers_dict, file, indent=4, ensure_ascii=False)