# The Differential Misalignment of Large Language Models in Evaluating Press Freedom

This is the reproducibility package for the paper 'The Differential Misalignment of Large Language Models in Evaluating Press Freedom'

# src/
Contians the code to repdocue the analysis in the paper
plots_for_paper_final.ipynb - code for reproducing the plots in the paper

# data/ 
Contains the data to repdocue the analysis in the paper

Here’s an improved version of your README section that is clearer, more structured, and more professional. I’ve made the language more concise, corrected grammar, and formatted key parameters for readability:

---

## `full_pipeline/`

This folder contains all the code needed to run the full pipeline that calls language models (LLMs) and generates country-specific scores based on a survey.

To generate the final DataFrame with LLM-based scores for each country, simply run the `main.py` script located in this folder.

### Required Parameters

Before running the script, configure the following parameters:

```python
COUNTRIES = {'Bahrain'}  # Set of countries to process
SHEET_NAME = 'mapping_r1'  # Options: 'mapping', 'mapping_r1', or 'mapping_r2'
MODEL_NAME = 'deepseek-chat'  # Name of the LLM (e.g., 'gpt-4', 'claude-3-opus', 'deepseek-chat', etc.)
MODEL = 'DEEPSEEK'  # Model ID used internally
API_KEY = 'your_api_key'  # API key for the chosen model
END_POINT = 'https://api.deepseek.com/v1/chat/completions'  # Endpoint URL for the LLM API
```

### Parameter Descriptions

* **`COUNTRIES`**: A set of country names for which you want to compute survey scores.
* **`SHEET_NAME`**: Specifies the ordering of survey answers. Use:

  * `'mapping'` for the original order,
  * `'mapping_r1'` or `'mapping_r2'` for two different randomized orders.
* **`MODEL_NAME`**: The name of the language model. Refer to the documentation of the respective API to choose the correct identifier.
* **`MODEL`**: An internal string identifier used for tracking the model (can be anything descriptive).
* **`API_KEY`**: Your API key for accessing the LLM service.
* **`END_POINT`**: The specific endpoint URL to send requests to. This may vary depending on the selected model/API.

### Running the Pipeline

Once the parameters are set, execute the pipeline by running:

```bash
python main.py
```

The output will be a DataFrame with survey scores computed for each selected country using the specified LLM.
