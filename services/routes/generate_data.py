import uuid
import os
import csv
import random
from fastapi import APIRouter, HTTPException, status
from logger import startup_logger, get_logger
from models.generate_data import generate_data
from data_types.personal import InputRequest
from models.logic import PersonalTypeAllocator
from utils.unique_name import generate_user_name_unique


# Khởi tạo logger
startup_logger()
logger = get_logger()

router = APIRouter()

@router.post("/generate_data", status_code=status.HTTP_201_CREATED)
async def generate_data_endpoint(samples: int):
    if samples is None or samples <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parameter `samples` must be a positive integer"
        )

    output_dir = "generation_data"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "generated_data.csv")

    header = [
        "user_name",
        "age_type",
        "gender",
        "life_event",
        "children",
        "years_of_experience",
        "characteristics",
        "desired_income"
    ]

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for i in range(samples):
                logger.info(f"Generating sample {i+1}/{samples}")
                
                persona_data = generate_data()
                
                request = InputRequest(
                    user_name=generate_user_name_unique(),
                    persona_data=persona_data
                )
                
                personal_type = PersonalTypeAllocator.type_allocator(request.persona_data)
                logger.debug(f"Classified persona: {personal_type}")

                chars_list = personal_type.characteristics or []
                chars_str = ";".join(chars_list)

                writer.writerow([
                    request.user_name,
                    personal_type.age_type,
                    personal_type.gender,
                    personal_type.life_event,
                    personal_type.children,
                    personal_type.years_of_experience,
                    chars_str,
                    personal_type.desired_income
                ])

        logger.info(f"Saved {samples} samples to {file_path}")
        return {
            "status": "OK",
            "message": f"Generated and saved {samples} samples to {file_path}"
        }

    except Exception as e:
        logger.error(f"Error generating or writing CSV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error during data generation"
        )
