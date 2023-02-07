from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Union, List
import json
from datetime import date, datetime
from fastapi import FastAPI
from pydantic import BaseModel
import typing
import enum
import re
from pydantic import Field, root_validator
from pydantic.types import ConstrainedStr
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.errors import MissingError, NoneIsNotAllowedError

app = FastAPI()


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
    prefix: str = Field(
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
    period: str

#class married(enum):


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

    #telecom: str

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
    maritalStatus: enum = ['married', 'divorced', 'single']



@app.post("/patients")
def create_patient(patient: Patient):
    # Create an instance of the patientinfo class
    # with the data provided in the request body
    item_instance = Patient(**patient.dict())
    # Serialize the instance to a JSON object
    print(item_instance.dict())
    json_object = json.dumps(item_instance.dict(), indent=4, default=str)
    # Write the JSON object to a file
    with open("patients.json", "a") as outfile:
        outfile.write(json_object)
    return {"message": "Data written successfully to file"}
  
@app.get("/patients")
def read_items():
    try:
        with open("patients.json", "r") as infile:
            data = json.load(infile)
            return data
    except FileNotFoundError:
        return {"message": "patients.json file not found"}
    except json.decoder.JSONDecodeError:
        return {"message": "patients.json file is empty"}
