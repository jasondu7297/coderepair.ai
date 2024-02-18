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
            print("Program failed with output: ", e.stdout)
            print("Program failed with error: ", e.stderr)

            gptJob = GPTJob(
                exec_path=self.exec_path,
                compile_cmd=self.compile_cmd,
                error_trace=e.stderr
            )
            while self._remaining_attempts:
                # Initiate early stoppage to prevent indefinite iterations
                # Throw ATTEMPTS_LIMITED_EXCEEDED
                if self._remaining_attempts == 0:
                    raise ATTEMPTS_LIMIT_EXCEEDED

                response_msg = gptJob.execute()
                recompile = gptJob.recompile()
                run_tests = gptJob.run_tests()

                if recompile == 0 and run_tests == 0:
                    print("YAYYYYY! " + response_msg)
                    return 0

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
        gptAgent = Agent(agentConfig, self.error_trace)

        return gptAgent.spawn_gpt()            

    def recompile(self) -> int:
        response = subprocess.run(self.compile_cmd, shell=True, capture_output=True, text=True)
        return response.returncode
    
    def run_tests(self) -> int:
        response = subprocess.run(self.exec_path, shell=True, capture_output=True, text=True)
        return response.returncode

class ATTEMPTS_LIMIT_EXCEEDED(Exception):
    def __init__(self):
        self.message = f"Exceeded limit of maximum attempts"
        super().__init__(self.message)