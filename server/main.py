from typing import Any, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pprint import pprint
import json

import clinical_trials
import input_parser

app = FastAPI()
app.debug = True
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/ping')
def ping():
    return { 'pong' }

@app.get("/api/test")
def get_test():
    return "get test"

@app.get("/api/search-studies")
def search_studies(input: str):
    api_params_json = input_parser.generate_clinical_trial_params(input)
    clinical_trials_results = clinical_trials.fetch_clinical_trials(api_params_json)

    return clinical_trials_results

def my_middleware(app):
    def middleware(environ, start_response):
        # Call the original app to get the response
        response = app(environ, start_response)

        # Add custom headers to the response
        headers = [('Access-Control-Allow-Origin', '*'), ('Access-Control-Allow-Headers', '*'), ("X-foo", "bar")]
        new_response = []
        for name, value in response:
            if name.lower() != 'content-length':
                new_response.append((name, value))
        new_response.extend(headers)

        return new_response

    return middleware

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)