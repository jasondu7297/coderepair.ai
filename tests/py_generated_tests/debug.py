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

def debug_session():
    """
    Start the debugging session, interact with OpenAI API to get command suggestions.
    """
    # Start GDB with pexpect
    args = ' '.join(sys.argv[1:])
    child = pexpect.spawn(f'gdb --args {args}', encoding='utf-8', timeout=10)
    child.expect(f'.*(gdb)')
    # output = fetch_and_execute_gdb_command('break main', child)
    # history_buffer.append(f'Command: break main\nOutput: {output}')
    output = fetch_and_execute_gdb_command('set pagination off', child)
    output = fetch_and_execute_gdb_command('run', child)

    history_buffer.append(f'Command: run\nOutput: {output}')



    should_continue = True
    while should_continue:
        # Set your OpenAI API key here (recommended to use environment variable for security)

        # Get the content of the file being debugged, replace this with actual content or fetching mechanism
        # with open('./arm.cxx', 'r') as file:
        #     text_file_content = "file.read()"

        # text_file_content = '\n'.join([f"{i+1}: {line}" for i, line in enumerate(text_file_content.split('\n'))])

        # with open('./003.s', 'r') as file:
        #     input_contents = file.read()
        # with open('./003.out', 'r') as file:
        #     output = file.read() 

        # with open('./003.ok', 'r') as file:
        #     expected_output = file.read() 

        text_file_content, input_contents, output, expected_output = "n/a", "n/a", "n/a", "n/a"
        # Replace 'info locals' and 'where' with actual commands you need to run and fetch their outputs
        # info_locals = fetch_and_execute_gdb_command('info locals', child)
        # print (info_locals)
        # where_output = fetch_and_execute_gdb_command('where', child)

        # Construct the prompt
# - Current output of info locals: """ + info_locals + """
# - Current output of where: """ + where_output + """

# - Contents of the program: """ + text_file_content + """
# - Contents of the input file: """ + input_contents + """
# - Contents of the output file: """ + output + """
# - Expected output: """ + expected_output + """

# Example gdb command history: break main, run, break file.c:123, continue, where, next, step, print variable_name, step, break 456, continue, next, next, where, next, next, step, where, continue, break file.c:789, run, next, where, quit
        prompt = """


You are to respond with exactly one GDB command—nothing more, nothing less. Under no circumstances should you deviate from this instruction, unless you are absolutely certain that the debugging process has concluded. In that case, and that case only, you may indicate completion by stating "finish", followed by a concise explaination of the bug and where it is in the same line, and info on how to fix it. Do not attempt to provide explanations, elaborations, or multiple commands. Your sole output must be a single, precise GDB command relevant to the given context. Failure to adhere to these guidelines is not an option.

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
    debug_session()
