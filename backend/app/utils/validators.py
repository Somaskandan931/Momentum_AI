from bson import ObjectId

def is_valid_object_id(id_str: str) -> bool:
    try:
        ObjectId(id_str)
        return True
    except Exception:
        return False

def validate_priority(priority: str) -> str:
    valid = ["high", "medium", "low"]
    if priority not in valid:
        raise ValueError(f"Priority must be one of {valid}")
    return priority

def validate_task_status(status: str) -> str:
    valid = ["To Do", "In Progress", "Completed"]
    if status not in valid:
        raise ValueError(f"Status must be one of {valid}")
    return status
