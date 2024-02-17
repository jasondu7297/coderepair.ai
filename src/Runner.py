import subprocess
from pydantic import BaseModel

class Runner(BaseModel):
    def run(self):
        pass