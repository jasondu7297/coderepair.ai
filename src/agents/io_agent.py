from agent import Agent
import openai

class IOAgent(Agent):
    def __init__(self, openai_key: str, executable: str):
        super().__init__(openai_key=openai_key, executable=executable)

    def generate_tools(self):
        pass

    def fetch_and_execute_cmd(self):
        pass

def _read_file(executable: str):
    pass

def _write_file(executable: str):
    pass
