import requests

# Function to fetch studies from the API
def fetch_studies(
    base_url,
    condition,
    overall_status,
    fields,
    sort_by,
    page_size,
    markup_format="markdown",
    response_format="json"
):
    """
    Fetch studies from the ClinicalTrials API based on input parameters.
    
    Args:
        base_url (str): Base URL for the API.
        condition (str): Condition or disease to search for.
        overall_status (str): Recruitment status to filter studies.
        fields (str): Comma-separated list of fields to return.
        sort_by (str): Sorting criteria for the studies.
        page_size (int): Number of studies per page.
        markup_format (str): Format of markup fields, default is markdown.
        response_format (str): Response format, default is json.

    Returns:
        dict: Parsed response from the API.
    """
    # Parameters for the API request
    params = {
        "format": response_format,
        "markupFormat": markup_format,
        "query.cond": condition,
        "filter.overallStatus": overall_status,
        "fields": fields,
        "sort": sort_by,
        "pageSize": page_size,
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return parsed JSON response
    else:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

# Variables for input parameters
base_url = "https://clinicaltrials.gov/api/v2/studies"
condition = "lung cancer"  # Search condition
overall_status = "RECRUITING"  # Filter by recruiting status
fields = "NCTId,BriefTitle,OverallStatus,EnrollmentCount"  # Fields to include
sort_by = "EnrollmentCount:desc"  # Sort by enrollment count, descending
page_size = 10  # Number of studies per page

# Function call
try:
    result = fetch_studies(
        base_url=base_url,
        condition=condition,
        overall_status=overall_status,
        fields=fields,
        sort_by=sort_by,
        page_size=page_size,
    )
    print("API Response:", result)
except Exception as e:
    print(str(e))