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
        with open('./arm.cxx', 'r') as file:
            text_file_content = file.read()

        text_file_content = '\n'.join([f"{i+1}: {line}" for i, line in enumerate(text_file_content.split('\n'))])

        with open('./003.s', 'r') as file:
            input_contents = file.read()
        with open('./003.out', 'r') as file:
            output = file.read() 

        with open('./003.ok', 'r') as file:
            expected_output = file.read() 
        # Replace 'info locals' and 'where' with actual commands you need to run and fetch their outputs
        info_locals = fetch_and_execute_gdb_command('info locals', child)
        where_output = fetch_and_execute_gdb_command('where', child)

        # Construct the prompt

        prompt = """
- Contents of the program: """ + text_file_content + """
- Contents of the input file: """ + input_contents + """
- Contents of the output file: """ + output + """
- Expected output: """ + expected_output + """
- Current output of info locals: """ + info_locals + """
- Current output of where: """ + where_output + """

Listen carefully, GPT-4. Your task is to debug code based on the following context. Please use gdb to set breakpoints at functions or lines and step through them to investigate the issue. You are to provide a single GDB command that will help us understand the bug in the code. Above is the context for the debugging session.

You are to respond with exactly one GDB command—nothing more, nothing less. Your sole output must be a single, precise GDB command relevant to the given context. Failure to adhere to these guidelines is not an option. Make sure to set breakpoints and use step thrououghly. If you are absolutely certain that the debugging process has concluded, you may indicate completion by stating 'finish', followed by an explaination of the bug in the SAME LINE. However, you MUST at least throughly set MULTIPLE BREAKPOINTS and call RUN and step through a program before finishing. Example gdb command history: break main, break file.c:123, run, next, next, step, print variable_name, step, break 456, next, next, next, where, set variable=expression, next, next, step, where, continue, break file.c:789, run, next, where, quit

- History of commands and outputs: """ + "\n".join(history_buffer) + """

"""         
        prompt += "" if (len(history_buffer)> 50) else ""


        print('Prompt:', prompt)

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

        if completion.lower().startswith("finish"):

            print("Finishing debug session based on OpenAI suggestion:", completion)
            break

        print('Completion generated:', completion)

        if completion:
            result = fetch_and_execute_gdb_command(completion, child)
            history_buffer.append(f'Command: {completion}\nOutput: {result}')

    child.sendline('quit')  # Quit GDB

if __name__ == '__main__':
    executable = sys.argv[1]
    debug_session(executable)
