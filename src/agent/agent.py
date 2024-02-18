from typing import Any, Dict, List
from src.command.command import Command, CommandType
import openai
import logging

class AgentConfig():
    openai_key: str
    executable_path: str

class Agent():
    cmd_history: List[str] = []
    msg_history: List[Dict[str, Any]]
    executable: str

    def __init__(self, config: AgentConfig):
        self.executable = config.executable_path
        openai.api_key = config.openai_key
    
    def update_msg_history(self, execution_result: str) -> None:
        execution_msg = {
            "role": "user", 
            "content": execution_result,
        }
        self.msg_history.append(execution_msg)
    
    def spawn_gpt(self, initial_prompt: str) -> Any:
        should_continue = True

        '''
        Define the behaviour of GPT4 model
        '''
        current_msg = {
            "role": "system", 
            "content": initial_prompt,
        }
        self.msg_history.append(current_msg)

        while should_continue:
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "user",
                        "content": self.msg_history[-1],
                    },
                ],
            )

            response_msg = response.choices[0].message
            logging.info('Action generation completed: ', response_msg)

            if response_msg.content:
                serialized_cmd = Command(response_msg.content)

                if serialized_cmd.cmd_type == CommandType.END:
                    logging.info("Finishing code repair session based on OpenAI suggestion:", response_msg)
                    return response_msg

                execution_result = serialized_cmd.execute()            
                self.update_msg_history(execution_result)
