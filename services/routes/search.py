from fastapi import APIRouter, HTTPException, status
from typing import List

from data_types.personal import InputRequest, OutputResponse, PersonaType
from models.logic import PersonalTypeAllocator
from utils.prompt import generate_persona_prompt
from database.vector_db import embed
from database.service_config import QDRANT_COLLECTION, vectordb_provider
from logger import startup_logger, get_logger

startup_logger()
logger = get_logger()
router = APIRouter()

@router.post(
    "/search_persona",
    response_model=OutputResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Invalid input"},
        404: {"description": "No matches found"},
        500: {"description": "Internal server error"}
    }
)
async def search_persona(request: InputRequest):
    if not request.persona_data:
        raise HTTPException(400, "persona_data is required")

    try:
        persona_type: PersonaType = PersonalTypeAllocator.type_allocator(request.persona_data)
        logger.debug("Classified: %s", persona_type.json())

        prompt_text = generate_persona_prompt({"persona_data": persona_type}, "persona_data")
        logger.debug("Prompt: %s", prompt_text)

        vector = embed(prompt_text)
        if vector is None:
            raise HTTPException(500, "Embedding service returned None")

        hits = vectordb_provider.search_vector(
            collection_name=QDRANT_COLLECTION,
            vector=vector,
            limit=3,
            with_payload=True
        )
        if not hits:
            raise HTTPException(404, "No matching profiles found")

        results: List[PersonaType] = []
        user_names: List[str] = []

        for hit in hits:
            pl = hit.payload or {}
            
            logger.info("Hit: %s", pl)

            # Chuẩn hóa characteristics
            ch = pl.get('characteristics')
            if isinstance(ch, str):
                pl['characteristics'] = [s.strip() for s in ch.split(';') if s]

            # Lấy user_name (hoặc user_id nếu chưa có)
            name = pl.get('user_name') or pl.get('user_id', '')
            user_names.append(name)

            try:
                results.append(PersonaType(**pl))
            except Exception as e:
                logger.error("Payload→PersonaType error: %s", e)

        if not results:
            raise HTTPException(404, "No matching profiles found")

        return OutputResponse(
            user_name=user_names,
            personal_type=results
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in search_persona")
        raise HTTPException(500, "Internal server error")