from fastapi import APIRouter, HTTPException, UploadFile, File, status
import pandas as pd
import uuid
from database.vector_db import embed
from database.service_config import vectordb_provider, QDRANT_COLLECTION
from utils.prompt import generate_persona_prompt
from logger import startup_logger, get_logger
from utils.unique_name import generate_user_name_unique

# Initialize logger
startup_logger()
logger = get_logger()
router = APIRouter()

@router.post("/upload_data", status_code=status.HTTP_201_CREATED)
async def upload_data(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=415, detail="Only .csv files are supported")

    try:
        df = pd.read_csv(file.file, index_col=False)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {e}")

    inserted = 0
    errors = []

    for idx, row in df.iterrows():
        try:
            profile = {
                "user_name": str(row["user_name"]),
                "persona_data": {
                    "age_type":               row["age_type"],
                    "gender":                 row["gender"],
                    "life_event":             row["life_event"],
                    "children":               row["children"],
                    "years_of_experience":    row["years_of_experience"],
                    "characteristics":        row["characteristics"],
                    "desired_income":         row["desired_income"],
                }
            }

            persona_text = generate_persona_prompt(profile, "persona_data")

            vector = embed(persona_text)
            if vector is None:
                raise ValueError("Embedding returned None")
            
            unique_id = str(uuid.uuid4())

            payload = {
                "user_name": profile["user_name"],
                **profile["persona_data"],
            }

            vectordb_provider.add_vectors_(
                collection_name=QDRANT_COLLECTION,
                text=persona_text,
                payload=payload,
                id=unique_id
            )

            inserted += 1

        except Exception as ex:
            errors.append({"row": idx, "error": str(ex)})

    return {
        "inserted": inserted,
        "failed": len(errors),
        "errors": errors
    }
