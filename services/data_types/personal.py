from typing import Optional, List
from pydantic import BaseModel, Field

class PersonaData(BaseModel):
    age: int = Field(..., ge=0, description="User's age")
    gender: Optional[str] = Field(None, description="User's gender")
    life_event: Optional[str] = Field(None, description="User's recent life event")
    children: Optional[int] = Field(None, ge=0, description="Number of children user has")
    years_of_experience: Optional[int] = Field(None, ge=0, description="User's years of experience in their field")
    characteristics: Optional[List[str]] = Field(None, description="User's characteristics")
    desired_income: Optional[float] = Field(None, ge=0, description="User's desired income")


class PersonaType(BaseModel):
    age_type: str
    gender: Optional[str] = None
    life_event: Optional[str] = None
    children: Optional[int] = None
    years_of_experience: Optional[int] = None
    characteristics: Optional[List[str]] = None
    desired_income: Optional[str] = None


class InputRequest(BaseModel):
    user_name: Optional[str] = Field(None, description="Unique identifier for the user")
    persona_data: PersonaData

class OutputResponse(BaseModel):
    user_name: Optional[List[str]] = Field(None, description="Unique identifier for the user")
    personal_type: List[PersonaType]
