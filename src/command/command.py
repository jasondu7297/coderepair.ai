import json
import subprocess
from enum import Enum
from typing import Any
from pydantic import BaseModel

class CommandType(Enum):
    BASH = 0
    GDB = 1
    WRITE = 2
    END = 3

class Command(BaseModel):
    cmd_str: str
    cmd_type: CommandType
    params: list[str] = []

    def __init__(self, cmd_raw):
        if cmd_raw.upper().startswith("BASH"):
            self.cmd_str[len("BASH:"):].strip()
            self.cmd_type = CommandType.BASH
        elif cmd_raw.upper().startswith("GDB"):
            self.cmd_str[len("GDB:"):].strip()
            self.cmd_type = CommandType.GDB
        elif cmd_raw.upper().startswith("WRITE"):
            self.cmd_str[len("WRITE:"):].strip()
            self.cmd_type = CommandType.WRITE
        elif cmd_raw.upper() == "FINISH!":
            self.cmd_type = CommandType.END
        else:
            raise ValueError("GPT response not of valid type")

    def execute(self) -> Any:
        kwargs = {
            "capture_output": True,
            "text": True,
        }

        if self.cmd_type == CommandType.GDB:
            kwargs["shell"] = True

        response = subprocess.run(self.cmd_str, **kwargs)
        return response.stdout