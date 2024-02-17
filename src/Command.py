from pydantic import BaseModel

class Command(BaseModel):
    cmd_str: str
    description: str
    params: dict

    def __init__(self, json_str: str):
        pass

    def serialize() -> str:
        pass

    def deserialize() -> str:
        pass

    def execute() -> None:
        pass