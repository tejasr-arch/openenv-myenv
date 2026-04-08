from pydantic import BaseModel

class Action(BaseModel):
    score: int

class Observation(BaseModel):
    resume: str
    job: str

class State(BaseModel):
    step: int = 0