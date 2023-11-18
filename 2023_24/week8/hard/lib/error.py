class IllegalWrite(Exception):
    def __init__(self, cls: type, field: str) -> None:
        super().__init__(f"Attempted illegal write to {cls.__name__}.{field}")
