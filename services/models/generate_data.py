import random
from data_types.personal import PersonaData


life_event = [
    "Starting a Career",
    "Getting Married",
    "Major Illness/Disability",
    "Losing a Job",
    "Retirement"
]

characteristics = ["Responsibility and Carefulness", "Patience", "Communication skills", "Loving and caring nature"]

gender = ["Male", "Female"]


def generate_data():
    
    num_chars = random.randint(2, 3)
    chosen_characteristics = random.sample(characteristics, k=num_chars)
    
    person_type = PersonaData(
        age=random.randint(1,101),
        gender=random.choice(gender),
        life_event=random.choice(life_event),
        children=random.randint(0, 5),
        years_of_experience=random.randint(0, 50),
        characteristics=chosen_characteristics,
        desired_income=random.randint(0, 100000000)
    )
    
    return person_type
