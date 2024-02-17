from pydantic import BaseModel

class CommandGenerator(BaseModel):
    cmd_str: str
    description: str
    params: dict

    def __init__(self, json_str: str):
        pass

    def serialize():
        pass

    def deserialize():
        pass