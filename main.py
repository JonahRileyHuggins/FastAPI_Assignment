from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Union, List
import json
import os
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

base_url = 'https://uts-ws.nlm.nih.gov/rest/'
endpoint = 'search/current'

with open('key.txt', 'r') as file:
    api_key = file.read().replace('\n', '')

#Creates a patient 
@app.post("/patients/{patient_id}")
def create_patient(patient: Patient, patient_id: int):
    with open("patients.json", 'r+') as infile:
        patient_db = json.load(infile)
    patient_db[patient_id] = patient.dict()

    # Write the JSON object to a file
    with open("patients.json", "w", encoding='utf-8') as outfile:
        outfile.write('\n')
        json.dump(patient_db, outfile, ensure_ascii=False, indent=4, default=str)
        
  

@app.put("/patients/{identifier}")
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



#Make a function that makes a GET request to UMLS for the ui code associated with a diagnosis.
def ICD10_Code(diagnosis: str):
    query_param = f'?string={diagnosis}&sab=ICD10CM&returnIdType=code&apiKey={api_key}'
    response = requests.get(base_url + endpoint + query_param)
    result = response.json()['result']['results']
    return result[0]['ui']

#Make a POST function that updates the conditions.json file with the ui code of the patient's condition.
@app.post("/condition/{patient_id}")
def UMLSIntoConditon(patient_id: int, condition: Condition):
    with open('conditions.json', 'r') as infile:
        condition_data = json.load(infile)
#Make an object that inherits from the Condition class in Classes.py    
    condition_data = condition.dict()    
#Assign the subject attribute the value of the given patient id
    condition_data['subject'] = patient_id
#Make a diagnosis object that obtains from the condition text section
    diagnosis = condition_data['code']['text']
#Make an object that uses the ICD10_Code funtion defined above to populate the text section of the condition 
    get_ICD10_Code = ICD10_Code(diagnosis)
#Now populate the condition_data object with the correct ICD10 code! 
    condition_data['code']['coding'] = get_ICD10_Code
#Now dump to the conditions.json!!!
    with open("conditions.json", "w") as outfile:
        outfile.write('\n')
        json.dump(condition_data, outfile, indent=4, default=str)



@app.put("/condition/{patient_id}/{condition_id}")
def create_condition(patient_id: int, condition_id: str, condition: Condition):
    with open("conditions.json", 'r+') as infile:
        condition_db = json.load(infile)
    condition_db[patient_id] = condition.dict()
    condition_db['subject'] = patient_id
    diagnosis = condition_db['code']['text']
    get_ICD10_Code = ICD10_Code(diagnosis)
    condition_db['code']['coding']
    with open("conditions.json", "w") as outfile:
        outfile.write('\n')
        json.dump(condition_db, outfile, indent=4, default=str)



#Make a function that retrieves the LOINC code from UMLS
def LOINC_CODE(labValue:str):
     query_param = f'?string={labValue}&sab=ICD10CM&returnIdType=code&apiKey={api_key}'
     response = requests.get(base_url + endpoint + query_param)
     result = response.json()['result']['results']
     return result[0]['ui']

#Creating a POST endpoint to lead to an Observation file
@app.post("/condition/{patient_id}")
def UMLSIntoConditon(patient_id: int, observation: Observation):
    with open('observation.json', 'r') as infile:
        observation_data = json.load(infile)
    observation_data = observation.dict()    
    observation_data['subject'] = patient_id
    labValue = observation_data['code']['text']
    get_LabValue = ICD10_Code(labValue)
    observation_data['code']['coding'] = get_LabValue
    with open("observations.json", "w") as outfile:
        outfile.write('\n')
        json.dump(observation_data, outfile, indent=4, default=str)