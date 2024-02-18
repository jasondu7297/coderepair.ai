from abc import ABC, abstractmethod
from typing import Any, Dict, List
import openai
import logging

class Agent(ABC):
    cmd_history: List[str]
    executable: str

    def __init__(self, openai_key: str, executable: str):
        self.cmd_history = []
        self.executable = executable
        openai.api_key = openai_key

    def spawn_gpt(self, prompt, tools) -> Any:
        text_file_content = ""

        full_prompt = f"""
                        Listen carefully, GPT-4. Your task is to debug code based on the following context:
                        - Contents of the text file: """ + text_file_content + """
                        - Executable for GDB to use: """ + self.executable + """
                        - History of commands and outputs: """ + "\n".join(self.cmd_history) + """

                        {prompt}
                        """

        should_continue = True
        while should_continue:
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt,
                    },
                ],
                tools=tools
            )

            response_msg = response.choices[0].message
            logging.info('Action generation completed: ', response_msg)

            if response_msg.tool_calls:
                logging.info(dict(response_msg.tool_calls[0]))
                exec_result = self.fetch_and_execute_cmd(response_msg.tool_calls[0], self.executable)
                self.cmd_history.append(f'Command: {response_msg}\nOutput: {exec_result}')

            elif response_msg.content:
                if response_msg.content.upper().startswith("FINISH"):
                    logging.info("Finishing code repair session based on OpenAI suggestion:", response_msg)
                    return response_msg

                exec_result = self.fetch_and_execute_cmd(response_msg.content)
                self.cmd_history.append(f'Command: {response_msg}\nOutput: {exec_result}')
                
    @abstractmethod
    def generate_tools(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def fetch_and_execute_cmd(self, command: str, executable: str) -> Any:
        pass
