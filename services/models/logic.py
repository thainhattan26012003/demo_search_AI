from typing import Optional
from data_types.personal import PersonaType, PersonaData
from logger import startup_logger, get_logger

startup_logger()
logger = get_logger()


def classify_age(age: int) -> str:
    if age < 25:
        return "<25"
    elif 25 <= age < 30:
        return "25-30"
    elif 30 <= age < 45:
        return "30-45"
    elif 45 <= age < 50:
        return "45-50"
    elif 50 <= age <= 60:
        return "50-60"
    else:
        return ">60"


def classify_income(ratio: float) -> str:
    if ratio < 10000000:
        return "< 10tr"
    elif 10000000 <= ratio < 30000000:
        return "10tr - 30tr"
    elif 30000000 <= ratio < 50000000:
        return "30tr - 50tr"
    else:
        return "> 50tr"


class PersonalTypeAllocator:
    @staticmethod
    def type_allocator(personal_data: PersonaData) -> PersonaType:
        
        chars: list[str] | None = personal_data.characteristics
        
        return PersonaType(
            age_type=classify_age(personal_data.age) if personal_data.age is not None else None,
            gender=personal_data.gender if personal_data.gender is not None else None,
            life_event=personal_data.life_event if personal_data.life_event is not None else None,
            children=personal_data.children if personal_data.children is not None else None,
            years_of_experience=personal_data.years_of_experience if personal_data.years_of_experience is not None else None,
            characteristics=chars if chars is not None else None,
            desired_income=classify_income(personal_data.desired_income) if personal_data.desired_income is not None else None
        )



