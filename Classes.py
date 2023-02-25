from dataclasses import dataclass
from datetime import datetime
from pydantic import Field, BaseModel
from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Union, List



@dataclass
class Period:
    start: datetime
    end: datetime

@dataclass
class CodeableConcept:
	coding: str = None
	text: str = None
@dataclass
class Address:
    use: str 
    text: str
    line:str
    city: str
    district: str 
    state: str
    postalcode: str
    country: str
    period = Period

@dataclass
class HumanName:
    code: str = None
    family: str = None
    given: str = None
    prefix: str = None
    suffix: str = None 


@dataclass
class Identifier:
    use: Optional[str] = None
    system: Optional[str] = None  
    value: Optional[str] = None
    period = Period 
    assigner: Optional[str] = None

@dataclass
class Contact:
        relationship: Optional[str] = None
        name = HumanName
        telecom: Optional[int] = None
        address = Address
        gender: Optional[str] = None
        Organization: Optional[str] = None
        period = Period

@dataclass
class Communication:
    language: str
    preferred: bool    

@dataclass
class link: 
        other: str = None


class clinicalStatus(BaseModel):
    #active | recurrence | relapes | inactive | remission | resolved
    clinical_status: str 

class verificationStatus(BaseModel):
    # Unconfirmed | provisional | differential | confirmed | refuted | entered-in-error
    verification_status: str = None

class Category(BaseModel):
    category: Optional[str] = None

class Severity(BaseModel):
    severity: Optional[str] = None

class Code(BaseModel):
    coding: Optional[str] = None
    text: Optional[str] = None

class BodySite(BaseModel):
    bodySite: str = None

class Subject(BaseModel):
    subject: str = None

class Encounter(BaseModel):
    encounter: str = None

class OnsetDateTime(BaseModel):
    onsetDateTime: datetime = None

class OnsetAge(BaseModel): 
    onsetage: datetime = None

class OnsetPeriod(BaseModel):
    onsetperiod: datetime = None

class OnsetRange(BaseModel):
    onsetrange: str

class RecordedDate(BaseModel):
    recordeddate: datetime = None


class Patient(BaseModel):
    resource_type: str = None
    identifier: int
    active: bool
    birthDate: datetime = None
    telecom: int
    name: HumanName
    gender: str 
    deceasedBoolean: bool
    deceasedDateTime: datetime = None
    address: Address
    maritalStatus: str
    multipleBirthBoolean: bool
    multipleBirthInteger: int
    contact: Contact
    comunication: Communication
    generalPractitioner: str
    managingOrganization: str
    link: link


class Condition(BaseModel):
    resource_type: str = 'Condition'
    identifier: Identifier
    clinicalStatus: clinicalStatus
    verificationstatus: verificationStatus
    category: Category
    severity: Severity
    code: Code
    bodysite: BodySite
    subject: Subject
    encounter: Encounter
    onsetdatetime: OnsetDateTime
    onsetage: OnsetAge
    onsetperiod: OnsetPeriod
    onsetrange: OnsetRange
    recordeddate: RecordedDate
    recorder: str = None
    
    






