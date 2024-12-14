import json
import os
import requests

# ClinicalTrials API Base URL
CLINICAL_TRIALS_API_URL = "https://clinicaltrials.gov/api/v2/studies"

# Function to call the ClinicalTrials API and fetch all results
def fetch_clinical_trials(api_params):
    all_results = []  # List to store all the results
    next_page_token = None  # Token for pagination

    # Convert fields list to a comma-separated string
    if 'fields' in api_params and isinstance(api_params['fields'], list):
        api_params['fields'] = ','.join(api_params['fields'])

    # while True:
    # Prepare API request parameters
    params = {
        **api_params,
        'pageToken': next_page_token  # Set the token for the next page
    }
    # Make the API call
    #response = requests.get(CLINICAL_TRIALS_API_URL, params=params)
    # match this url: https://clinicaltrials.gov/api/v2/studies?query.cond=friedreich%27s+ataxia&filter.overallStatus=AVAILABLE%7CRECRUITING" \
    print("api_params['query.cond']:", api_params['query.cond'])
    query_cond_formatted = api_params['query.cond'].replace(" ", "+").replace("'", "%27")
    new_url = f"{CLINICAL_TRIALS_API_URL}?query.cond={query_cond_formatted}&filter.overallStatus=AVAILABLE%7CRECRUITING"
    response = requests.get(new_url)

    # Check for errors in the response
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    # Parse the JSON response
    response_data = response.json()
    studies = response_data.get("studies", [])
    all_results.extend(studies)

        # Check if there's a next page token
        # next_page_token = response_data.get("nextPageToken")
        # if not next_page_token:
        #     break

    return all_results

if __name__ == "__main__":
    with open(os.path.join("data", "demo/input.json"), "r") as file:
        patient_input = json.load(file)
    
    api_params = {key: value for key, value in patient_input.items() if value is not None}
    api_params["filter.overallStatus"] = ["RECRUITING", "AVAILABLE"]
    api_params["postFilter.overallStatus"] = ["RECRUITING", "AVAILABLE"]


    results = fetch_clinical_trials(api_params)
    
    with open(os.path.join("data", "clinical_trials_results.json"), "w") as outfile:
        json.dump(results, outfile, indent=2)
    
    with open(os.path.join("data", "api_params.json"), "w") as file:
        json.dump(api_params, file, indent=2)