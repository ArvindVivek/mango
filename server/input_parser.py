import json
import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
)

# Define the custom function for extracting clinical trial parameters
clinical_trial_functions = [
    {
        'name': 'extract_clinical_trial_params',
        'description': 'Extract all relevant parameters for the clinical trial API call from user input. The field name in the JSON object should match the API parameter name. \n Do not have a field named "patient" in the JSON object, this should be called query.patient \n For filter.geo, if given a general location name, convert the value to this format: distance(latitude,longitude,radius). Examples: distance(39.0035707,-77.1013313,50mi)',
        'parameters': {
            'type': 'object',
            'properties': {
                'query.cond': {
                    'type': 'string',
                    'description': 'Condition or disease the user is looking for.'
                },
                'query.term': {
                    'type': 'string',
                    'description': 'Other terms for additional filtering or keywords.'
                },
                'query.locn': {
                    'type': 'string',
                    'description': 'Location terms for finding nearby trials.'
                },
                'query.titles': {
                    'type': 'string',
                    'description': 'Search by study titles or acronyms.'
                },
                'query.intr': {
                    'type': 'string',
                    'description': 'Search for intervention or treatment details.'
                },
                'query.outc': {
                    'type': 'string',
                    'description': 'Search for outcome measures.'
                },
                'query.spons': {
                    'type': 'string',
                    'description': 'Search by sponsor or collaborator.'
                },
                'query.lead': {
                    'type': 'string',
                    'description': 'Search by lead sponsor name.'
                },
                'query.id': {
                    'type': 'string',
                    'description': 'Search by specific study IDs.'
                },
                'query.patient': {
                    'type': 'string',
                    'description': 'Patient-specific filters for clinical trials.'
                },
                'filter.overallStatus': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Recruitment statuses to filter by (e.g., RECRUITING, COMPLETED).'
                },
                'filter.geo': {
                    'type': 'string',
                    'description': 'Geographical filter (e.g., distance(latitude,longitude,radius)). Filter by geo-function. Currently only distance function is supported. Format: distance(latitude,longitude,distance)Examples: distance(39.0035707,-77.1013313,50mi)'
                },
                'filter.ids': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Filter by specific study IDs.'
                },
                'filter.advanced': {
                    'type': 'string',
                    'description': 'Advanced filters using Essie expression syntax.'
                },
                'filter.synonyms': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Filters based on area:synonym_id pairs.'
                },
                'postFilter.overallStatus': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Post-filters by recruitment status.'
                },
                'postFilter.geo': {
                    'type': 'string',
                    'description': 'Post-filters by geographical location.'
                },
                'postFilter.ids': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Post-filters by specific study IDs.'
                },
                'postFilter.advanced': {
                    'type': 'string',
                    'description': 'Post-filters using Essie expression syntax.'
                },
                'postFilter.synonyms': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Post-filters based on area:synonym_id pairs.'
                },
                'aggFilters': {
                    'type': 'string',
                    'description': 'Apply aggregation filters.'
                },
                'geoDecay': {
                    'type': 'string',
                    'description': 'Proximity factor for geographical filters.'
                },
                'fields': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Fields to return in the API response.'
                },
                'sort': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Sorting options for studies.'
                },
                'countTotal': {
                    'type': 'boolean',
                    'description': 'Whether to include the total count of studies in the response.'
                },
                'pageSize': {
                    'type': 'integer',
                    'description': 'Number of studies to return per page.'
                },
                'pageToken': {
                    'type': 'string',
                    'description': 'Token for fetching the next page of results.'
                }
            },
            'required': ['query.cond']
        }
    }
]

# Function to simulate an API parameter generation workflow
def generate_clinical_trial_params(patient_input):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': patient_input}],
        functions=clinical_trial_functions,
        function_call='auto'
    )
    # Parse and return the JSON response
    return json.loads(response.choices[0].message.function_call.arguments)

if __name__ == "__main__":

    # Sample user inputs describing patients and their needs
    patient_inputs = [
        "I am a 45-year-old male diagnosed with lung cancer. I am looking for recruiting clinical trials.",
        "I am a 30-year-old female with breast cancer. I'm interested in active trials anywhere in the United States."
    ]

    # Process each patient input
    for patient_input in patient_inputs:
        try:
            api_params = generate_clinical_trial_params(patient_input)
            print(json.dumps(api_params, indent=4))
        except Exception as e:
            print(f"Error processing input: {patient_input}\n{e}")