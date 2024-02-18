from agent import Agent
from typing import Any, Dict
import subprocess
import openai

class GDBAgent(Agent):
    def __init__(self, openai_key: str, executable: str):
        super().__init__(openai_key=openai_key, executable=executable)

    def generate_tools(self) -> Dict[str, Any]:
        return []

    def fetch_and_execute_cmd(self, cmd) -> Any:
        response = subprocess.run(cmd, capture_output=True, text=True)
        return response.stdout
