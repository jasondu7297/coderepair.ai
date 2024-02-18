import logging
import subprocess
from typing import List
from agent import Agent, AgentConfig

class Job():
    exec_path: str
    compile_cmd: str

    # For any job, there will be a minimum of 1 attempt
    _remaining_attempts: int = 9

    def __init__(self, exec_path: str, compile_cmd: str):
        self.exec_path = exec_path
        self.compile_cmd = compile_cmd

    def execute(self) -> int:
        try:
            result = subprocess.run(self.exec_path, capture_output=True, text=True, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            '''
            When check=True, a CalledProcessError exception is thrown if subprocess.run results in non-zero exit code
            If CalledProcessError exception thrown, init GPTJob to execute with GPT assistance
            '''
            logging.info("Program failed with output: ", e.stdout)
            logging.info("Program failed with error: ", e.stderr)

            gptJob = GPTJob(
                exec_path=self.exec_path,
                compile_cmd=self.compile_cmd,
                error_trace=e.stderr
            )
            while self._remaining_attempts:
                # Initiate early stoppage to prevent indefinite iterations
                # Throw ATTEMPTS_LIMITED_EXCEEDED
                if self._remaining_attempts == 0:
                    logging.info("No solution for executable failure found, sorry!")
                    break

                response_msg = gptJob.execute()
                if gptJob.recompile() and gptJob.run_tests():
                    logging.info("YAYYYYY! " + response_msg)
                    break

                self._remaining_attempts -= 1

    def terminate(self):
        pass

class GPTJobMetadata():
    changes: dict
    failed: bool

class GPTJob():
    '''
    For each execution of GPTJob, we should retain the suggested change, the actual output, and expected output
    '''
    history: list[GPTJobMetadata] = []
    
    exec_path: str
    compile_cmd: str
    error_trace: str

    def __init__(self, exec_path: str, compile_cmd: str, error_trace: str):
        self.exec_path = exec_path
        self.compile_cmd = compile_cmd
        self.error_trace = error_trace

    def execute(self) -> bool:
        agentConfig = AgentConfig(openai_key='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', executable_path=self.exec_path)
        gptAgent = Agent(agentConfig)

        return gptAgent.spawn_gpt(self.get_initial_prompt())            

    def recompile(self) -> int:
        response = subprocess.run(self.compile_cmd, shell=True, capture_output=True, text=True)
        return response.returncode
    
    def run_tests(self) -> int:
        response = subprocess.run(self.exec_path, shell=True, capture_output=True, text=True)
        return response.returncode

    def get_initial_prompt(self) -> str: 
        return f"""
Traceback Error: {self.error_trace}
You are trying to fix the bug in this code. At each point you may specify a single command to run. We will then execute this command and respond to you with the output before you produce your next command. This command can be one of the following three types.
1. A bash command.
Expected Structure:
BASH COMMAND: <place bash command to execute here>
Note that if you use the bash commands to modify a source code file, I want you to only do this via find and replace operations.
2. A gdb debugger command.
Expected structure:
GDB COMMAND: <place gdb command to execute here>
3. Termination Command. Output this command if you think you have fixed the bug in the code and no more changes have to be made to the code. If you output the termination command, no more subsequent commands.
Expected structure:
FINISH!
You must not provide any additional explanations or elaborations. Only provide the command in the structure specified above. Nothing more, nothing less.
"""