from abc import ABC, abstractmethod
from pydantic import BaseModel
import openai
import logging

class Agent(BaseModel, ABC):
    cmd_history: list[str]

    def __init__(self, openapi_key):
        openai.api_key = openapi_key
        self.cmd_history = []

    # TODO: Fix prompt to be dynamic with cmd_history
    def spawn_gpt(self, prompt, tools):
        should_continue = True
        while should_continue:
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                tools=tools
            )

            response_msg = response.choices[0].message.content.strip()

            logging.info('Action generation completed: ', response_msg)

            if response.msg.upper().startswith("FINISH"):
                logging.info("Finishing code repair session based on OpenAI suggestion:", response_msg)
                break

            if response_msg:
                result = self.fetch_and_execute_cmd(response_msg)
                self.cmd_history.append(f'Command: {response_msg}\nOutput: {result}')

    @abstractmethod
    def generate_tools(self):
        pass
    
    @abstractmethod
    def fetch_and_execute_cmd(self, command):
        pass