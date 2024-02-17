from agent import Agent
import subprocess
import openai

from pydantic import BaseModel

class GDBAgent(Agent, BaseModel):
    executable: str

    def __init__(self, executable: str):
        self.exeuctable = executable

    def generate_tools():
        return []

    def fetch_and_execute_cmd(self, command):
        response = subprocess.run(command, capture_output=True, text=True)
        return response.stdout