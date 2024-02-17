from agent import Agent
import openai

from pydantic import BaseModel

class IOAgent(Agent, BaseModel):
    def generate_tools():
        pass

    def fetch_and_execute_cmd(self):
        pass

    def _read_file(self):
        pass

    def _write_file(self):
        pass