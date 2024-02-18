from typing import Any, Dict, List
from command import Command, CommandType
import subprocess
import openai
import logging

class AgentConfig():
    openai_key: str
    executable_path: str
    use_gdb: bool

    def __init__(self, openai_key: str, executable_path: str, use_gdb = True):
        self.openai_key = openai_key
        self.executable_path = executable_path
        self.use_gdb = True

class Agent():
    cmd_history: List[str] = []
    error_trace: str
    executable: str

    use_gdb: bool
    gdb_instance: object

    prompt: str

    def __init__(self, config: AgentConfig, error_trace: str):
        self.executable = config.executable_path
        self.error_trace = error_trace
        self.use_gdb = config.use_gdb

        self.update_prompt()
        openai.api_key = config.openai_key
    
    def spawn_gpt(self) -> Any:
        if self.use_gdb:
            self.gdb_instance = spawn_persisting_gdb(self.executable)

        '''
        Define the behaviour of GPT4 model
        '''

        should_continue = True
        while should_continue:
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "user",
                        "content": self.prompt,
                    },
                ],
            )
            response_msg = response.choices[0].message

            if response_msg.content:
                cmd_str = response_msg.content.strip()                
                serialized_cmd = Command(cmd_str, self.use_gdb)

                print(cmd_str)

                if serialized_cmd.cmd_type == CommandType.END:
                    if self.use_gdb:
                        terminate_persisting_gdb(self.gdb_instance)

                    print("Finishing code repair session based on OpenAI suggestion:", response_msg.content)
                    return response_msg

                elif serialized_cmd.cmd_type == CommandType.GDB:
                    self.gdb_instance.stdin.write(serialized_cmd.cmd_str + "\n")
                    self.gdb_instance.stdin.flush()

                    execution_result = self.gdb_instance.stdout.readline().strip()
                    self.cmd_history.append("Command: " + serialized_cmd.cmd_str + "\nOutput: " + execution_result)
                    self.update_prompt()
                    continue

                execution_result = serialized_cmd.execute()          
                self.cmd_history.append("Command: " + serialized_cmd.cmd_str + "\nOutput: " + execution_result)
                self.update_prompt()

    def update_prompt(self) -> None:
        self.prompt = f"""        
Traceback Error: {self.error_trace}

Previous commands that have been run and their respective outputs: 
""" + ('\n'.join(self.cmd_history) if self.cmd_history else "None") + """
You are to assume that we are already in a GDB debugging session. You are to analyze and change source code only. You are not to change any other code such as ASM, machine code, and file metadata. Any bash commands used should be to find and replace error-inducing lines of code.

REMEMBER: You are at the root-level of the codebase and all code related to the errors are within that scope. All commands will be run from your location, which is root-level.

You are to respond with exactly one GDB command OR one bash command—nothing more, nothing less. Under no circumstances should you deviate from this instruction, unless you are absolutely certain that the debugging process has concluded AND THAT WE HAVE used bash to fix the bugs in the code. In that case, and that case only, you may indicate completion by stating “FINISH!”, followed by a concise explaination of the bug and where it is in the same line, and info on how you fixed it. Do not attempt to provide explanations, elaborations, or multiple commands. Your sole output must be a single, precise GDB command or bash command relevant to the given context. Failure to adhere to these guidelines is not an option.

The bash command is to be executed using 

BASH COMMAND: <command>

The GDB command is to be executed using 

GDB COMMAND: <gdb command>
"""

def spawn_persisting_gdb(executable: str) -> object:
    return subprocess.Popen(['gdb', executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def terminate_persisting_gdb(gdb_instance: object) -> None:
    gdb_instance.terminate()
