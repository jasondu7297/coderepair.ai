from typing import Any, Dict, List
from command import Command, CommandType
import openai
import logging

class AgentConfig():
    openai_key: str
    executable_path: str

    def __init__(self, openai_key: str, executable_path: str):
        self.openai_key = openai_key
        self.executable_path = executable_path

class Agent():
    cmd_history: List[str] = []
    error_trace: str
    executable: str

    def __init__(self, config: AgentConfig, error_trace: str):
        self.executable = config.executable_path
        self.error_trace = error_trace
        openai.api_key = config.openai_key
        self.prompt = f"""Traceback Error: {error_trace}

Previous commands that have been run and their respective outputs: 
None

You are trying to fix the bug in this code. You are sitting in the main directory of the code being executed and can debug this code using bash commands and gdb commands. You have been given the traceback error message of the bug you are trying to fix and a sequence of commands that you have run in the past with their respective outputs. 
Respond with the next command to run to debug this code. This command can be one of the following three types.

1. A bash command.
Expected Structure:
BASH COMMAND: <place bash command to execute here>
If you are producing a bash command, it must be in the structure above, in which you output "BASH COMMAND: " followed by the bash command you want to run. Deviating from this structure is not an option.
Note that if you use the bash commands to modify a source code file, I want you to only do this via find and replace operations.
2. A gdb debugger command.
Expected structure:
GDB COMMAND: <place gdb command to execute here>
If you are producing a GDB command, it must be in the structure above, in which you output "GDB COMMAND: " followed by the gdb command you want to run. Also, make sure that the gdb command starts with gdb. Deviating from this structure is not an option.
3. Termination Command. Output this command if you think you have fixed the bug in the code and no more changes have to be made to the code. If you output the termination command, no more subsequent commands.
Expected structure:
FINISH!
You must not provide any additional explanations or elaborations. Only provide the command in the structure specified above. Nothing more, nothing less.

All commands that you output MUST be directly runnable
"""
    
    def update_prompt(self) -> None:

        self.prompt = f"""Traceback Error: {self.error_trace}

Previous commands that have been run and their respective outputs: 
""" + {'\n'.join(self.cmd_history)} + """

You are trying to fix the bug in this code. You are sitting in the main directory of the code being executed and can debug this code using bash commands and gdb commands. You have been given the traceback error message of the bug you are trying to fix and a sequence of commands that you have run in the past with their respective outputs. 
Respond with the next command to run to debug this code. This command can be one of the following three types.

1. A bash command.
Expected Structure:
BASH COMMAND: <place bash command to execute here>
If you are producing a bash command, it must be in the structure above, in which you output "BASH COMMAND: " followed by the bash command you want to run. Deviating from this structure is not an option.
Note that if you use the bash commands to modify a source code file, I want you to only do this via find and replace operations.
2. A gdb debugger command.
Expected structure:
GDB COMMAND: <place gdb command to execute here>
If you are producing a GDB command, it must be in the structure above, in which you output "GDB COMMAND: " followed by the gdb command you want to run. Also, make sure that the gdb command starts with gdb. Deviating from this structure is not an option.
3. Termination Command. Output this command if you think you have fixed the bug in the code and no more changes have to be made to the code. If you output the termination command, no more subsequent commands.
Expected structure:
FINISH!
You must not provide any additional explanations or elaborations. Only provide the command in the structure specified above. Nothing more, nothing less.

All commands that you output MUST be directly runnable
"""
    
    def spawn_gpt(self) -> Any:
        should_continue = True

        '''
        Define the behaviour of GPT4 model
        '''

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

            logging.info('Action generation completed: ', response_msg)

            if response_msg.content:
                serialized_cmd = Command(response_msg.content.strip())

                if serialized_cmd.cmd_type == CommandType.END:
                    logging.info("Finishing code repair session based on OpenAI suggestion:", response_msg)
                    return response_msg

                execution_result = serialized_cmd.execute()          
                self.cmd_history.append("Command: " + serialized_cmd.cmd_str + "\nOutput: " + execution_result)
                self.update_prompt
