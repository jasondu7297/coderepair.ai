from agent import Agent
from command import Command
from gdb_agent import GDBAgent
import openai

import sys

from pydantic import BaseModel

class MainAgent(Agent, BaseModel):
    def generate_tools():
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "_debug_session",
                    "description": "Initialize and run a debugger that will set breakpoints, step through the code, and return a reasoning to why code is broken",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "executable": {
                                "type": "string",
                                "description": "The executable file for GDB to use",
                            },
                        },
                        "required": ["executable"],
                    },
                }
            }
        ]
        return tools

    def fetch_and_execute_cmd(self, command):
        cmd = Command()
        return cmd

    def _debug_session(self):
        debug_agent = GDBAgent(openapi_key=openai.api_key)

        prompt = ""
        tools = self.generate_tools()

        debug_agent.spawn_gpt(prompt, tools)

    def _read_file(self):
        io_agent = GDBAgent(openapi_key=openai.api_key)

        prompt = ""
        tools = self.generate_tools()

        io_agent.spawn_gpt(prompt, tools)

    def _write_file(self):
        io_agent = GDBAgent(openapi_key=openai.api_key)

        prompt = ""
        tools = self.generate_tools()

        io_agent.spawn_gpt(prompt, tools)

if __name__ == '__main__':
    executable = sys.argv[1]
    mainAgent = MainAgent(openapi_key='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')


    mainAgent.spawn_gpt(prompt="prompt", tools=mainAgent.generate_tools())