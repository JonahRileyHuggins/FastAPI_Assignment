#!/usr/bin/env python3

from typing import Union
import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class responseapi(BaseModel):
    id: int
    name: str
    research_interests: str
    hobbies: str
    spirit_animal: str

@app.post("/items")
def update_item(item: responseapi):
    # Create an instance of the responseapi class
    # with the data provided in the request body
    item_instance = responseapi(**item.dict())
    # Serialize the instance to a JSON object
    json_object = json.dumps(item_instance.dict(), indent=4)
    # Write the JSON object to a file
    with open("sample.json", "a") as outfile:
        outfile.write(json_object)
    return {"message": "Data written successfully to file"}
  
@app.get("/items")
def read_items():
    try:
        with open("sample.json", "r") as infile:
            data = json.load(infile)
            return data
    except FileNotFoundError:
        return {"message": "sample.json file not found"}
    except json.decoder.JSONDecodeError:
        return {"message": "sample.json file is empty"}
