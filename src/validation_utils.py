
def validate_file_path(file_path: str) -> bool:
    """Validate file path exists and is readable"""
    if not file_path:
        return False
    path = Path(file_path)
    return path.exists() and path.is_file() and os.access(file_path, os.R_OK)

def validate_topic_name(topic: str) -> bool:
    """Validate topic name is not empty and reasonable length"""
    return bool(topic and topic.strip() and len(topic.strip()) <= 200)

def validate_number_input(value: str, min_val: int = 1, max_val: int = 100) -> bool:
    """Validate numeric input is within reasonable range"""
    try:
        num = int(value)
        return min_val <= num <= max_val
    except ValueError:
        return False
