def generate_persona_prompt(profile: dict, data_type: str) -> str:
    data = profile.get(data_type, {})

    if hasattr(data, "dict") and callable(data.dict):
        data = data.dict()

    if not isinstance(data, dict):
        try:
            data = data.__dict__
        except Exception:
            raise TypeError(f"{type(data)} is not a valid persona format.")

    chars = data.get("characteristics", [])
    if isinstance(chars, (list, tuple)):
        chars_str = ";".join(str(c) for c in chars)
    else:
        chars_str = str(chars or "")

    prompt = (
        f"Age Type: {data.get('age_type','')}, "
        f"Gender: {data.get('gender','')}, "
        f"Life Event: {data.get('life_event','')}, "
        f"Children: {data.get('children','')}, "
        f"Years of Experience: {data.get('years_of_experience','')}, "
        f"Characteristics: {chars_str}, "
        f"Desired Income: {data.get('desired_income','')}"
    )

    return prompt
