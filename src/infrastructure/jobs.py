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
            result = subprocess.run(self.exec, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            '''
            When check=True, a CalledProcessError exception is thrown if subprocess.run results in non-zero exit code
            If CalledProcessError exception thrown, init GPTJob to execute with GPT assistance
            '''
            logging.info("Program failed with output: ", e.stdout)
            logging.info("Program failed with error: ", e.stderr)

            gptJob = GPTJob(
                exec=self.exec,
                compile_cmd=self.compile_cmd
            )
            while _remaining_attempts:
                # Initiate early stoppage to prevent indefinite iterations
                # Throw ATTEMPTS_LIMITED_EXCEEDED
                if _remaining_attempts == 0:
                    logging.info("No solution for executable failure found, sorry!")
                    break

                if gptJob.execute():
                    gptJob.cleanup()
                    break

                _remaining_attempts -= 1

    def terminate(self):
        pass

class GPTJobMetadata(BaseModel):
    changes: dict
    failed: bool

class GPTJob(BaseModel):
    '''
    For each execution of GPTJob, we should retain the suggested change, the actual output, and expected output
    '''
    history: list[GPTJobMetadata]
    
    exec: str
    compile_cmd: str

    def execute() -> bool:
        ''' 
        Iterate in the following loop:
          - Initiate GPT prompt
          - If function call: serialize and execute command
          - Otherwise: end and onto the next
        '''

    def cleanup():
        pass