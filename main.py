from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Union, List
import json
import os
import uuid
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

with open('key.txt', 'r') as file:
    api_key = file.read().replace('\n', '')

databases_dir = os.path.join(os.path.abspath('.'), 'databases')
###############################################################################################################################################################################################################################################
#Patient Profile Start

#Creates a patient 
@app.post("/patients/{patient_id}")
def create_patient(patient: Patient, patient_id: int):
    #Check if the patient json database already exists
    if './databases/patients.json' not in os.listdir():
        raise HTTPException(status_code=404, detail='Patient not found')
        patients_JSON = {'{}'}
        with open('./databases/patients.json', 'w') as outfile:
            json.dump(patients_JSON, outfile)
    with open("./databases/patients.json", 'r+') as infile:
        patient_db = json.load(infile)
    patient_db[patient_id] = patient.dict()

    # Write the JSON object to a file
    with open("./databases/patients.json", "w", encoding='utf-8') as outfile:
        outfile.write('\n')
        json.dump(patient_db, outfile, ensure_ascii=False, indent=4, default=str)
        
  
#Update a patient instance
@app.put("/patients/{identifier}")
def update_patient(identifier: str, patient: Patient):
    with open("./databases/patients.json", "r+") as infile:
        patient_db = json.load(infile)
        if identifier not in patient_db:
            return "Patient not found"
        patient_db[identifier] = patient.dict()
    with open("./databases/patients.json", "w") as outfile:
        outfile.write('\n')
        json.dump(patient_db, outfile, indent=4, default=str)


#Retrieve a patient instance
@app.get("/patients")
def read_patient(patient_id: int = None):
    with open("./databases/patients.json", "r+") as infile:
        patient_db = json.load(infile)
        if patient_id is not None:
            return patient_db

###############################################################################################################################################################################################################################################
#Patient Encounter Endpoints

#Create Unique Encounter ID
def encounter_id():
    today = date.today()
    now = datetime.now()
    return today.strftime("%Y%m%d")+now.strftime("%H%M%S")

#Create Encounter
#Creating a POST endpoint to lead to an Encounter file
@app.post("/encounters/{patient_id}")
def Create_Encounter(patient_id: int, encounter: Encounter):
    with open(os.path.join(databases_dir, 'encounters.json'), 'r') as infile:
        encounter_data = json.load(infile)
    encounter_data = encounter.dict()
    encounter_data['subject'] = patient_id
    encounter_data['encounterIdentifier']['uniqueID'] = encounter_id()
    with open(os.path.join(databases_dir, 'encounters.json'), 'w') as outfile:
        outfile.write('\n')
        json.dump(encounter_data, outfile, indent=4, default=str)

@app.put("/encounters/{patient_id}/{encounter_id}")
def update_encounter(patient_id: int, encounter_id: str, encounter: Encounter):
    with open("./databases/encounters.json", 'r+') as infile:
        encounter_db = json.load(infile)
    encounter_db = encounter.dict()
    encounter_db['subject'] = patient_id
    encounter_db['encounterIdentifier']['uniqueID'] = encounter_id
    with open("./databases/encounters.json", "w") as outfile:
        outfile.write('\n')
        json.dump(encounter_db, outfile, indent=4, default=str)

@app.get("/encounters/{patient_id}")
def read_encounter(patient_id: int):
    with open("./databases/encounters.json", "r+") as infile:
        encounter_db = json.load(infile)
        if patient_id is not None:
            return encounter_db


#############################################################################################################################################################################################################################
#Single Encounter Endpoints
#function for grabbing an encounter unique ID from the encounters.json file
def get_encounter_id(patient_id: int):
    with open('./databases/encounters.json', 'r') as infile:
        encounter_data = json.load(infile)
    return encounter_data[patient_id]['encounterIdentifier']['uniqueID']

#Make a function that makes a GET request to UMLS for the ui code associated with a diagnosis.
def ICD10_Code(diagnosis: str):
    endpoint = 'search/current'
    query_param = f'?string={diagnosis}&sab=ICD10CM&returnIdType=code&apiKey={api_key}'
    response = requests.get(base_url + endpoint + query_param)
    result = response.json()['result']['results']
    return result[0]['ui']

#Make a POST function that updates the databases/conditions.json file with the ui code of the patient's condition.
@app.post("/condition/{patient_id}")
def Create_Conditon(patient_id: int, condition: Condition):
    with open('./databases/conditions.json', 'r') as infile:
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
#Get the encounter ID from the encounters.json file
    encounter_id = get_encounter_id(patient_id)
#Now populate the condition_data object with the correct encounter ID!
    condition_data['encounterIdentifier']['uniqueID'] = get_encounter_id(patient_id)
#Now dump to the databases/conditions.json!!!
    with open("./databases/conditions.json", "w") as outfile:
        outfile.write('\n')
        json.dump(condition_data, outfile, indent=4, default=str)


#Creating a PUT endpoint to update the Condition file
@app.put("/condition/{patient_id}/{condition_id}")
def update_condition(patient_id: int, condition_id: str, condition: Condition):
    with open("./databases/conditions.json", 'r+') as infile:
        condition_db = json.load(infile)
    condition_db[patient_id] = condition.dict()
    condition_db['subject'] = patient_id
    diagnosis = condition_db['code']['text']
    get_ICD10_Code = ICD10_Code(diagnosis)
    condition_db['code']['coding']
    condition_db['encounterIdentifier']['uniqueID'] = get_encounter_id(patient_id)
    with open("./databases/conditions.json", "w") as outfile:
        outfile.write('\n')
        json.dump(condition_db, outfile, indent=4, default=str)



#Make a function that retrieves the LOINC code from UMLS
def LOINC_CODE(labValue: str):
     endpoint = 'content/current'
     query_param = f'/source/LNC/{labValue}?apiKey={api_key}'
     url = base_url + endpoint + query_param
     response = requests.get(url)
     if response.status_code != 200:
         return None
     result = response.json()['result']['name']
     return result

#Creating a POST endpoint to lead to an Observation file
@app.post("/observation/{patient_id}")
def Create_Observation(patient_id: int, observation: Observation):
    with open('./databases/observations.json', 'r') as infile:
        observation_data = json.load(infile)
    observation_data = observation.dict()    
    observation_data['subject'] = patient_id
    labValue = observation_data['code']['text']
    get_LabValue = LOINC_CODE(labValue)
    observation_data['code']['coding'] = get_LabValue
    observation_data['encounterIdentifier']['uniqueID'] = get_encounter_id(patient_id)
    with open("./databases/observations.json", "w") as outfile:
        outfile.write('\n')
        json.dump(observation_data, outfile, indent=4, default=str)

#Creating a PUT endpoint to update the Observation file
@app.put("/observation/{patient_id}/{observation_id}")
def create_observation(patient_id: int, observation_id: str, observation: Observation):
    with open("./databases/observations.json", 'r+') as infile:
        observation_db = json.load(infile)
    observation_db[patient_id] = observation.dict()
    observation_db['subject'] = patient_id
    labValue = observation_db['code']['text']
    get_LabValue = LOINC_CODE(labValue)
    observation_db['code']['coding']
    observation_db['encounterIdentifier']['uniqueID'] = get_encounter_id(patient_id)
    with open("./databases/observations.json", "w") as outfile:
        outfile.write('\n')
        json.dump(observation_db, outfile, indent=4, default=str)

#Creating a GET endpoint to read the Observation file
@app.get("/observations/{patient_id}")
def read_observation(patient_id: int):
    with open("./databases/observations.json", "r+") as infile:
        observation_db = json.load(infile)
        if patient_id is not None:
            return observation_db
        


#Make a function that retrieves the RxNorm code from UMLS
def RxNorm_CODE(medication: str):
    endpoint = '/rxcui.json'
    query_param = f'?name={medication}&search=1&apiKey={api_key}'
    base_rxnorm_url = 'https://rxnav.nlm.nih.gov/REST/'
    url = base_rxnorm_url + endpoint + query_param
    response = requests.get(url)
    result = response.json()['idGroup']['rxnormId']
    return result[0]

#Creating a POST endpoint to lead to a Medication file
@app.post("/medication/{patient_id}")
def Create_Medication(patient_id: int, medication: MedicationRequest):
    with open('./databases/medications.json', 'r') as infile:
        medication_data = json.load(infile)
    medication_data = medication.dict()    
    medication_data['subject'] = patient_id
    rxNormMedication = medication_data['medicationCodeableConcept']['text']
    get_RxNormMedication = RxNorm_CODE(rxNormMedication)
    medication_data['medicationCodeableConcept']['coding'] = get_RxNormMedication
    medication_data['encounterIdentifier']['uniqueID'] = get_encounter_id(patient_id)
    with open("./databases/medications.json", "w") as outfile:
        outfile.write('\n')
        json.dump(medication_data, outfile, indent=4, default=str)

#Creating a PUT endpoint to update the Medication file
@app.put("/medication/{patient_id}/{medication_id}")
def update_medication(patient_id: int, medication_id: str, medication: MedicationRequest):
    with open("./databases/medications.json", 'r+') as infile:
        medication_db = json.load(infile)
    medication_db[patient_id] = medication.dict()
    medication_db['subject'] = patient_id
    medication_db['encounterIdentifier']['uniqueID'] = get_encounter_id(patient_id)
    with open("./databases/medications.json", "w") as outfile:
        outfile.write('\n')
        json.dump(medication_db, outfile, indent=4, default=str)

#Creating a GET endpoint to read the Medication file
@app.get("/medications/{patient_id}")
def read_medication(patient_id: int):
    with open("./databases/medications.json", "r+") as infile:
        medication_db = json.load(infile)
        if patient_id is not None:
            return medication_db
        

