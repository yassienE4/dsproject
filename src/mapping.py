TYPE_TO_NUMBER = {
    "benign": 0,
    "defacement": 1,
    "malware": 2,
    "phishing": 3
}

# Reverse mapping (auto-generated)
NUMBER_TO_TYPE = {v: k for k, v in TYPE_TO_NUMBER.items()}


def number_to_type(number: int) -> str:
    """
    Convert a number to its corresponding type.
    """
    if number not in NUMBER_TO_TYPE:
        raise ValueError(f"Invalid number: {number}")
    return NUMBER_TO_TYPE[number]


def type_to_number(type_name: str) -> int:
    """
    Convert a type to its corresponding number.
    """
    if type_name not in TYPE_TO_NUMBER:
        raise ValueError(f"Invalid type: {type_name}")
    return TYPE_TO_NUMBER[type_name]


