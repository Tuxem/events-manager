def to_int_or_none(value):
    try:
        return int(value) if value.strip() else None
    except ValueError:
        return None

