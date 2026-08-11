def truncate(value: str, max_length: int = 4096) -> str:
    if len(value) > max_length:
        return value[:max_length] + "...[truncated]"
    else:
        return value
