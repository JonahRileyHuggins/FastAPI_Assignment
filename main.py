from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Union, List
import json
import os
from dotenv import load_dotenv
import requests
import enum
from datetime import date, datetime
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field, root_validator
from pydantic.types import ConstrainedStr
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.errors import MissingError, NoneIsNotAllowedError
from Classes import *

app = FastAPI()

api_key = os.getenv('UMLS_API_KEY')
base_url = 'https://uts-ws.nlm.nih.gov/rest/'
endpoint = 'search/current'
query_param = ['''FILL IN LATER''']

@app.post("/create/patients/{patient_id}")
def create_patient(patient: Patient, patient_id: int):
    with open("patients.json", 'r+') as infile:
        patient_db = json.load(infile)
    patient_db[patient_id] = patient.dict()

    # Write the JSON object to a file
    with open("patients.json", "w", encoding='utf-8') as outfile:
        outfile.write('\n')
        json.dump(patient_db, outfile, ensure_ascii=False, indent=4, default=str)
        
  

@app.put("/update/patients/{identifier}")
def update_patient(identifier: str, patient: Patient):
    with open("patients.json", "r+") as infile:
        patient_db = json.load(infile)
        if identifier not in patient_db:
            return "Patient not found"
        patient_db[identifier] = patient.dict()
    with open("patients.json", "w") as outfile:
        outfile.write('\n')
        json.dump(patient_db, outfile, indent=4, default=str)


@app.get("/patients")
def read_patient(patient_id: int = None):
    with open("patients.json", "r+") as infile:
        patient_db = json.load(infile)
        if patient_id is not None:
            return patient_db

    #with open("patients.json", "w") as outfile:
    #    outfile.write('\n')
    #    json.dump(patient_db, outfile, indent=4, default=str)
        #Message if identifier doesn't work:
       
@app.post("/create/condition/{patient_id}/{condition_id}")
def create_condition(patient_id: int, condition_id: int, condition: Condition):
    with open("conditions.json", 'r+') as infile:
        condition_db = json.load(infile)
    condition_db[condition_id] = condition.dict()


    with open("conditions.json", "w") as outfile:
        outfile.write('\n')
        json.dump(condition_db, outfile, indent=4, default=str)
