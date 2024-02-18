import pexpect
import sys
import os
import openai
import re
from gdbdemo import debug_session

history_buffer = []

openai.api_key = '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'

def fix_file(file_path, bug_description, gdb_history):

    # read the contents of the file we want to change
    with open(file_path, 'r') as file:
        file_contents = file.read()

    # number lines to allow for making unique references to substrings
    numbered_lines = [f"{line} //{i+1}" for i, line in enumerate(file_contents.split('\n'))]
    file_contents = '\n'.join(numbered_lines)

    # Construct the prompt
    prompt = """
Description of the Bug: """ + bug_description + """
GDB Debugging History:
""" + "\n".join(history_buffer) + """

Current Contents of the File with line numbers added to end (prepended by #):
""" + file_contents + """

Instructions for GPT-4:
Your task is to generate a list of argument pairs that, when passed to the str.replace() function with all of these argument pairs applied, will resolve the bug in the provided code. These argument pairs should address the specific issue described in the bug report and identified during the debugging session. Whenever you specify an old substring to be replaced (as the first argument in a pair) make sure this substring only occurs once in the code. The line numbers are appended to the end of each line to make this possible.

Expected Output:
Output a list of argument pairs in the following format:
OLD1<delim>NEW1<endofpair>OLD2 <delim> NEW2<endofpair>...OLDN <delim> NEWN<endofpair>

Where:
OLDx is the substring of the old string 
Each argument pair is separated by the delimiter <endofpair>.
Within each pair, use the delimiter <delim> to separate the old substring (OLD) from the replacement string (NEW).
The replacement string (NEW) follows the delimiter without any additional separators, allowing for easy parsing.

Additional Notes:

Aim for clarity, accuracy, and effectiveness in your solution.
Consider edge cases and potential side effects when generating the argument pairs.
Verify that the proposed solution aligns with the identified bug and does not introduce new issues into the code.
"""

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

    arg_pairs = completion.strip().split("<endofpair>")
    for arg_pair in arg_pairs:
        if len(arg_pair) == 0:
            break
        arg_list = arg_pair.split("<delim>")
        if len(arg_list) != 2:
            raise ValueError('Invalid argument pair structure given by GPT4: {arg_pair}')

        if file_contents.count(arg_list[0]) > 1:
            continue
            print(f'Non-unique substring given to string replace: {arg_list[1]}')
        file_contents = file_contents.replace(arg_list[0], arg_list[1])

    with open(file_path, 'w') as file:
        file.write(file_contents)


if __name__ == '__main__':
    executable = sys.argv[1]
    src_path = sys.argv[2]
    bug_description, gdb_history = debug_session(executable)

    fix_file(src_path, bug_description, gdb_history)