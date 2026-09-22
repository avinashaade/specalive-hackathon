from pydantic import BaseModel, Field
from typing import List, Optional


class Port(BaseModel):
    name: str
    type: str
    description: Optional[str] = None


class Component(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    ports: List[Port] = Field(default_factory=list)
    attributes: dict = Field(default_factory=dict)


class Connection(BaseModel):
    source: str
    target: str
    description: Optional[str] = None


class State(BaseModel):
    name: str
    description: Optional[str] = None


class Transition(BaseModel):
    source: str
    target: str
    trigger: Optional[str] = None
    condition: Optional[str] = None
    action: Optional[str] = None


class Assumption(BaseModel):
    description: str
    reason: Optional[str] = None


class SystemModel(BaseModel):
    name: str
    description: Optional[str] = None

    components: List[Component] = Field(default_factory=list)
    connections: List[Connection] = Field(default_factory=list)

    states: List[State] = Field(default_factory=list)
    transitions: List[Transition] = Field(default_factory=list)

    assumptions: List[Assumption] = Field(default_factory=list)