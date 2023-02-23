from dataclasses import dataclass
from datetime import datetime
from pydantic import Field, BaseModel
from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Union, List



@dataclass
class Period:
    start: datetime
    end: datetime

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
    period: Period

@dataclass
class HumanName:
    code: str = None
    family: str = None
    given: str = None
    prefix: str = None
    suffix: str = None 


@dataclass
class Identifier:
    use: str = None
    system: str = None
    value: str = None
    period: datetime = None
    assigner: str = None

@dataclass
class Contact(BaseModel):
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

@dataclass
class Communication:
    language: str
    preferred: bool    

@dataclass
class link: 
        other: str = None



@dataclass
class clinicalStatus:
    #active | recurrence | relapes | inactive | remission | resolved
    clinical_status: str = None

@dataclass
class verificationStatus:
    # Unconfirmed | provisional | differential | confirmed | refuted | entered-in-error
    verification_status: str = None

@dataclass
class Category:
    category: str = None

@dataclass
class Severity:
    severity: str = None

@dataclass
class Code:
    code: str = None

@dataclass
class BodySite:
    bodySite: str = None

@dataclass
class Subject:
    subject: str = None

@dataclass
class Encounter:
    encounter: str = None

@dataclass
class OnsetDateTime:
    onsetDateTime: datetime = None

@dataclass
class OnsetAge: 
    onsetage: datetime = None

@dataclass
class OnsetPeriod:
    onsetperiod: datetime = None

@dataclass
class OnsetRange:
    onsetrange: str

@dataclass
class RecordedDate:
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
    recorder: str
    
    






