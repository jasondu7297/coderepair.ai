import logging
import subprocess
from pydantic import BaseModel

class Job(BaseModel):
    exec: str
    compile_cmd: str
    input: object
    expected_output: object

    # For any job, there will be a minimum of 1 attempt
    _remaining_attempts: int = 9

    def execute(self):
        try:
            result = subprocess.run(exec, capture_output=True, text=True)
            gptJob = GPTJob()
            while result.returncode:
                gptJob.execute()
                _remaining_attempts -= 1
                
                # Initiate early stoppage to prevent indefinite iterations
                # Throw ATTEMPTS_LIMITED_EXCEEDED
                if _remaining_attempts == 0:
                    logging.info("No solution for executable failure found, sorry!")
                    break
            
            # If result return code is 0, GPT was able to solve the problem!
            if result.returncode == 0:
                logging.info("yay")

            
        except Exception as e:
            logging.error("An unexpected error occurred while running the program...")

    def terminate(self):
        pass

class GPTJob(BaseModel):
    '''
    For each execution of GPTJob, we should retain the suggested change, the actual output, and expected output
    '''