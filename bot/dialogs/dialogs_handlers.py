def validate_weight(text: str) -> str | None:
    weight = round(float(text), 2)
    if 20 <= weight <= 500:
        return text

    raise ValueError


