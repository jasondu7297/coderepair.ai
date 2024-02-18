import json
from pydantic import BaseModel

class Command(BaseModel):
    cmd_str: str
    description: str
    params: list[str]

    @classmethod
    def __init__(self, response: dict):
        function = response.function
        self.cmd_str = function.name

        arguments = function.arguments
        self.params = [f"{key}={value}" for key, value in json.loads(arguments).items()]

    @classmethod
    def serialize(self) -> str:
        return f"{self.cmd_str}({', '.join(self.params)})"

    @classmethod
    def deserialize(self) -> str:
        pass

    @classmethod
    def execute(self) -> None:
        eval(self.serialize())
