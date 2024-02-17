import pexpect
import sys
import os
import openai

history_buffer = []

openai.api_key = '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'

def fetch_and_execute_gdb_command(command, child):
    """
    Execute a GDB command using pexpect and return its output.
    """
    print(f'Sending command: {command}')
    child.sendline(command)
    child.expect(r'\(gdb\) $')
    output = child.before.strip()
    # print(f'Output:\n{output}')
    return output

def debug_session(executable):
    """
    Start the debugging session, interact with OpenAI API to get command suggestions.
    """
    # Start GDB with pexpect
    child = pexpect.spawn(f'gdb {executable}', encoding='utf-8', timeout=10)
    child.expect(f'.*(gdb)')
    fetch_and_execute_gdb_command('break main', child)
    fetch_and_execute_gdb_command('run', child)
    fetch_and_execute_gdb_command('step', child)


    should_continue = True
    while should_continue:
        # Set your OpenAI API key here (recommended to use environment variable for security)

        # Get the content of the file being debugged, replace this with actual content or fetching mechanism
        text_file_content = "contents of the file being debugged"

        # Replace 'info locals' and 'where' with actual commands you need to run and fetch their outputs
        info_locals = fetch_and_execute_gdb_command('info locals', child)
        where_output = fetch_and_execute_gdb_command('where', child)

        # Construct the prompt

        prompt = """
Listen carefully, GPT-4. Your task is to debug code based on the following context:
- Contents of the text file: """ + text_file_content + """
- Current output of info locals: """ + info_locals + """
- Current output of where: """ + where_output + """
- History of commands and outputs: """ + "\n".join(history_buffer) + """

You are to respond with exactly one GDB command—nothing more, nothing less. Under no circumstances should you deviate from this instruction, unless you are absolutely certain that the debugging process has concluded. In that case, and that case only, you may indicate completion by stating "finish", followed by an explaination of the bug in the same line. Do not attempt to provide explanations, elaborations, or multiple commands. Your sole output must be a single, precise GDB command relevant to the given context. Failure to adhere to these guidelines is not an option.
"""


        # print('Prompt:', prompt)

        # Make a call to the OpenAI API

        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        completion = response.choices[0].message.content.strip()

        print('Completion generated:', completion)

        if completion.lower().startswith("finish"):

            print("Finishing debug session based on OpenAI suggestion:", completion)
            break

        if completion:
            result = fetch_and_execute_gdb_command(completion, child)
            history_buffer.append(f'Command: {completion}\nOutput: {result}')

    child.sendline('quit')  # Quit GDB

if __name__ == '__main__':
    executable = sys.argv[1]
    debug_session(executable)
