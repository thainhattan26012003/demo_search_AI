import random
from faker import Faker

fake = Faker()

def generate_user_name_unique():
    base = fake.first_name().lower()
    suffix = random.randint(1000, 9999)
    return f"{base}{suffix}"