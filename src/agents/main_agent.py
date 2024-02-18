from agent import Agent
from src.command.command import Command
from gdb_agent import GDBAgent
from io_agent import IOAgent
from typing import Any, Dict
import openai

import sys

class MainAgent(Agent):
    def generate_tools(self) -> Dict[str, Any]:
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "_debug_session",
                    "description": "Initialize and run a debugger that will set breakpoints, step through the code, and return a reasoning to why code is broken",
                }
            }
        ]
        return tools

    def fetch_and_execute_cmd(self, cmd: str) -> Any:
        serialized_cmd = Command(cmd)
        return serialized_cmd

    def _debug_session(self) -> Any:
        debug_agent = GDBAgent(openapi_key=openai.api_key, executable=self.executable)

        prompt = ""
        tools = self.generate_tools()

        return debug_agent.spawn_gpt(prompt, tools)

    def _read_file(self) -> Any:
        io_agent = IOAgent(openapi_key=openai.api_key, executable=self.executable)

        prompt = ""
        tools = self.generate_tools()

        return io_agent.spawn_gpt(prompt, tools)

    def _write_file(self) -> Any:
        io_agent = IOAgent(openapi_key=openai.api_key, executable=self.executable)

        prompt = ""
        tools = self.generate_tools()

        return io_agent.spawn_gpt(prompt, tools)

if __name__ == '__main__':
    executable = sys.argv[1]
    mainAgent = MainAgent(openapi_key='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', executable=executable)


    mainAgent.spawn_gpt(prompt=
                        """You are to respond with exactly one GDB command—nothing more, nothing less. Under no circumstances should you deviate from this instruction, unless you are absolutely certain that the debugging process has concluded. In that case, and that case only, you may indicate completion by stating "finish", followed by an explaination of the bug in the same line. Do not attempt to provide explanations, elaborations, or multiple commands. Your sole output must be a single, precise GDB command relevant to the given context. Failure to adhere to these guidelines is not an option.
                        """, tools=mainAgent.generate_tools())