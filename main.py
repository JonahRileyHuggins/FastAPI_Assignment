from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Union, List
import json
from datetime import date, datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import typing
import enum
import re
from pydantic import Field, root_validator
from pydantic.types import ConstrainedStr
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.errors import MissingError, NoneIsNotAllowedError

app = FastAPI()

class Period(BaseModel):
    start: datetime
    end: datetime

class HumanName(BaseModel):
    code: str = Field( 
        ...,
        enum=['usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden'])
    text: str = Field(
        None,
        description="text representation of the full name"
    )
    family: str = Field(
        None, 
        description="Family name (often called 'Surname')"
    )
    given: str = Field(
        None, 
        description="Given names (not always 'first'. Inlcudes middle names)"
    )
    prefix: Optional[str] = Field(
        None, 
        description="Parts that come after the name"
    )
    suffix: str = Field(
        None, 
        description= "Parts that come after the name"
    )
class Address(BaseModel):
    use: str = Field(..., enum=['home', 'work', 'temp', 'old', 'billing'])
    type: str = Field(..., enum=['physical', 'postal', 'both'])
    text: str
    line:str
    city: str
    district: str 
    state: str
    postalcode: str
    country: str
    period: Period

class contact(BaseModel):
        relationship: str = Field(
            ..., 
            enum=('parent', 'sibling', 'spouse', 'other')
        )
        name: HumanName
        telecom: int
        address: Address
        gender: str = Field(
        ..., 
        enum=['male', 'female', 'other', 'unknown']
        )
        Organization: Optional[str]
        period: Period

class Communication(BaseModel):
    language: str
    preferred: bool    
class link(BaseModel): 
        other: str
        type: str

class Patient(BaseModel):
    resource_type = Field("Patient", const=True)
    identifier: int
    active: bool = Field(
        None, 
        alias="active",
        element_property=True    
    )
    birthDate: datetime = Field(
        None, 
        alias ="birthDate",
        description=None, 
        element_property=True
    )  
    telecom: int
    name: HumanName
    gender: str = Field(
        ..., 
        enum=['male', 'female', 'other', 'unknown']
    )
    deceasedBoolean: bool
    deceasedDateTime: datetime = Field(
        None, 
        alias ="deceasedDateTime",
        description=None, 
        element_property=True
    )  
    address: Address
    maritalStatus: str = Field(
        ..., 
        enum = ['married', 'divorced', 'single']
    )
    multipleBirthBoolean: bool
    multipleBirthInteger: int
    contact: contact
    comunication: Communication
    generalPractitioner: str
    managingOrganization: str
    link: link
    


@app.post("/create/patients/{patient_id}")
def create_patient(patient: Patient, patient_id: int):
    with open("patients.json", 'r') as infile:
        patient_db = json.load(infile)
    patient_db[patient_id] = patient.dict()

    # Write the JSON object to a file
    with open("patients.json", "a", encoding='utf-8') as outfile:
        json.dump(patient_db, outfile, ensure_ascii=False, indent=4, default=str)
  
@app.get("/patients")
def read_patient():
    try:
        with open("patients.json", "r") as infile:
            patient_db = json.load(infile)
            return patient_db
    except FileNotFoundError:
        return {"message": "patients.json file not found"}
    except json.decoder.JSONDecodeError:
        return {"message": "patients.json file is empty"}

@app.put("/update/patients/{identifier}")
def update_patient(identifier: str, patient: Patient):
    with open("patients.json", "r") as infile:
        patient_db = json.load(infile)
        if identifier not in patient_db:
            return "Patient not found"
        patient_db[identifier] = patient.dict()
    with open("patients.json", "w") as outfile:
        json.dump(patient_db, outfile, indent=4, default=str)
