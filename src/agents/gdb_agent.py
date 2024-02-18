from agent import Agent
from typing import Any, Dict
import subprocess
import openai

class GDBAgent(Agent):
    executable: str

    def __init__(self, executable: str):
        self.exeuctable = executable

    def generate_tools(self) -> Dict[str, Any]:
        return []

    def fetch_and_execute_cmd(self, cmd) -> Any:
        response = subprocess.run(cmd, capture_output=True, text=True)
        return response.stdout