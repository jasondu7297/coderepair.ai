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

    def fetch_and_execute_cmd(self, cmd: str, executable: str) -> Any:
        cmd_instance = Command(cmd, executable)
        serialized_cmd = cmd_instance.serialize()
        return eval(serialized_cmd)

def _debug_session(executable: str) -> Any:
    debug_agent = GDBAgent(openai_key=openai.api_key, executable=executable)

    prompt = ""
    tools = debug_agent.generate_tools()

    return debug_agent.spawn_gpt(prompt, tools)

def _read_file(executable: str) -> Any:
    io_agent = IOAgent(openai_key=openai.api_key, executable=executable)

    prompt = ""
    tools = io_agent.generate_tools()

    return io_agent.spawn_gpt(prompt, tools)

def _write_file(executable: str) -> Any:
    io_agent = IOAgent(openai_key=openai.api_key, executable=executable)

    prompt = ""
    tools = io_agent.generate_tools()

    return io_agent.spawn_gpt(prompt, tools)
