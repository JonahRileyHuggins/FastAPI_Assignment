from dataclasses import dataclass
from datetime import datetime, time
from pydantic import Field, BaseModel
from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Union, List


class Period(BaseModel):
    start: datetime
    end: datetime

class CodeableConcept(BaseModel):
	coding: str = None
	text: str = None
        
class Address(BaseModel):
    use: str 
    text: str
    line:str
    city: str
    district: str 
    state: str
    postalcode: str
    country: str
    period = Period

class HumanName(BaseModel):
    code: str = None
    family: str = None
    given: str = None
    prefix: str = None
    suffix: str = None 


class Identifier(BaseModel): 
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

class Severity(BaseModel):
    severity: Optional[str] = None

class Code(BaseModel):
    coding: Optional[str] = None
    text: Optional[str] = None

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

class Reference(BaseModel):
     reference: str = None
     type: str = None
     identifier: Identifier
     display: str = None

class Effective(BaseModel):
     effectiveDateTime: datetime
     effectivePeriod: Period
     effectiveTiming: datetime
     effectiveInstant: datetime

class SampleData(BaseModel):
    origin: str
    period: Period
    factor: int
    lowerLimit: int
    uppperLimit: int
    dimensions: int
    data: str

class Value(BaseModel):
    valueQuantity: int
    valueCodeableConcept: CodeableConcept
    valueString: str = None
    valueBoolean: bool
    valueInteger: int
    valueRange: int
    valueRatio:  int
    valueSampledData: SampleData
    valueTime: datetime
    valueDateTime: datetime
    valuPeriod: Period

class Annotation(BaseModel):
    author: HumanName
    time: datetime
    text: str

class ReferenceRange(BaseModel):
    low: int
    high: int
    type: CodeableConcept
    appliesTo: CodeableConcept
    age: int
    text: str

class Component(BaseModel):
    code: CodeableConcept
    value: Value
    dataAbsentRange: CodeableConcept
    iterpretation: CodeableConcept
    referenceRange: ReferenceRange

class dispenseRequest(BaseModel):
    initialFill: int
    dispenseInterval: int
    validityPeriod: Period
    numberOfRepeatsAllowed: int
    quantity: int
    expectedSupplyDuration: int

class substitution(BaseModel):
    allowed: bool
    reason: CodeableConcept

class Participant(BaseModel):
    type: CodeableConcept
    period: Period
    actor: Reference

class Diagnosis(BaseModel):
    condition: Reference
    use: CodeableConcept

class Admission(BaseModel):
    preAdmissionIdentifier: Identifier
    origin: Reference
    admitSource: CodeableConcept
    reAdmission: CodeableConcept
    destination: Reference
    dischargeDisposition: CodeableConcept

class Location(BaseModel):
    location: Reference
    status: str
    physicalType: CodeableConcept
    period: Period

class EncounterID(BaseModel):
    uniqueID: str

#Class for which the patient post function inherits
class Patient(BaseModel):
    resource_type: str = None
    identifier: Identifier
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

#Class for which the Condition POST function inherits from
class Condition(BaseModel):
    resource_type: str = 'Condition'
    encounterIdentifier: EncounterID
    identifier: Identifier
    clinicalStatus: clinicalStatus
    verificationstatus: verificationStatus
    category: CodeableConcept
    severity: Severity
    code: Code
    bodysite: CodeableConcept
    subject: Reference
    encounter: Reference
    onsetdatetime: OnsetDateTime
    onsetage: OnsetAge
    onsetperiod: OnsetPeriod
    onsetrange: OnsetRange
    recordeddate: RecordedDate
    recorder: str = None
    
    
#Class for which the Observation POST function inherits from
class Observation(BaseModel):
     resource_type: str = 'Observation'
     encounterIdentifier: EncounterID
     identifier: Identifier
     basedon: Reference
     partOf: Reference
     status: Code
     category: CodeableConcept
     code: Code
     Subject: Reference
     focus: Reference
     encounter: Reference
     effective: Effective
     issued: datetime
     performer: Reference
     value: Value
     dataAbsentReason: CodeableConcept
     interpretation: CodeableConcept
     note: Annotation
     bodySite: CodeableConcept
     method: CodeableConcept
     specimen: Reference
     device: Reference
     referenceRange: ReferenceRange
     hasMember: Reference
     derivedFrom: Reference
     component: Component
     

#Class for Medications POST function inherits from
class MedicationRequest(BaseModel):
    resource_type: str = 'Medication'
    encounterIdentifier: EncounterID
    identifier: Identifier
    basedon: Reference
    priorPresciption: Reference
    groupIdentifier: Identifier
    status: Code
    statusReason: CodeableConcept
    statusChanged: datetime
    intent: Code
    category: CodeableConcept
    priority: Code
    doNotPerform: bool
    medication: CodeableConcept
    subject: Reference
    informationSource: Reference
    encounter: Reference
    supportingInformation: Reference
    authoredOn: datetime
    requester: Reference
    reported: bool
    performer: Reference
    device: Reference
    recorder: Reference
    reason: CodeableConcept
    courseOfTherapyType: CodeableConcept
    insurance: Reference
    note: Annotation
    renderedDosageInstruction: str
    effectiveDosePeriod: Period
    dosageInstruction: str
    dispenseRequest: dispenseRequest
    substitution: substitution

#FHIR Encounter Class
class Encounter(BaseModel):
    resource_type: str = 'Encounter'
    encounterIdentifier: EncounterID
    identifier: Identifier
    status: Code
    class_: CodeableConcept
    type: CodeableConcept
    serviceType: CodeableConcept
    subjectStatus: CodeableConcept
    priority: CodeableConcept
    subject: Reference
    episodeOfCare: Reference
    basedOn: Reference
    careTeam: Reference
    partOf: Reference
    serviceProvider: Reference
    participant: Participant
    appointment: Reference
    virtualService: Reference
    actualPeriod: Period
    plannedStartDateTime: datetime
    plannedEndDateTime: datetime
    period: Period
    length: int
    reason: CodeableConcept
    diagnosis: Diagnosis
    account: Reference
    dietPreference: CodeableConcept
    specialArrangement: CodeableConcept
    specialCourtesy: CodeableConcept
    admissiion: Admission
    location: Location
   