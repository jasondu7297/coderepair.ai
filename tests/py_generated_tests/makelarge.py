import os
import random

# Directory to store the generated C and header files
directory = "segfault_program"
os.makedirs(directory, exist_ok=True)

def generate_junk_operations(c_file, num_operations):
    c_file.write("    double a0 = 2.7182818284590452; double a1 = 3.141592635389793;\n")
    for i in range(2, num_operations):
        op = random.choice(["+", "-", "*", "/"])
        operands = random.sample(range(max(0, i - 10), i), 2)
        if op == "/":
            operands[1] = max(operands[1], 1)
        c_file.write(f"    double a{i} = a{operands[0]} {op} a{operands[1]};\n")
        if i % 10 == 0:
            c_file.write(f'    printf("a{i} = %fl\\n", a{i});\n')

def create_c_file(file_id, num_files, cause_segfault=False):
    filename = f"file_{file_id}.c"
    headername = f"file_{file_id}.h"
    function_name = f"function_{file_id}"
    num_operations = random.randint(50, 500)

    with open(os.path.join(directory, headername), "w") as header_file:
        header_file.write(f"void {function_name}();\n")

    with open(os.path.join(directory, filename), "w") as c_file:
        # Include the header of the next file if it's not the last file
        if file_id < num_files - 1:
            c_file.write(f'#include "file_{file_id + 1}.h"\n')
        c_file.write('#include <stdio.h>\n')
        c_file.write(f"void {function_name}() {{\n")
        # c_file.write(f'    printf("Function {file_id} called\\n");\n')
        
        if not cause_segfault:
            generate_junk_operations(c_file, num_operations)
            # Call the next function if it's not the last file
            if file_id < num_files - 1:
                c_file.write(f"    function_{file_id + 1}();\n")
        else:
            c_file.write('    printf("Causing segfault...\\n");\n    int *p = NULL;\n    *p = 10;  // This will cause a segmentation fault\n')
        c_file.write("}\n")

def create_main_file(num_files):
    main_filename = os.path.join(directory, "main.c")
    with open(main_filename, "w") as main_file:
        main_file.write('#include "file_0.h"\n')
        main_file.write("int main() {\n")
        main_file.write("    function_0();\n")
        main_file.write("    return 0;\n}\n")

if __name__ == "__main__":
    num_files = 100  # Adjust this to change the number of files generated
    for i in range(num_files):
        create_c_file(i, num_files, cause_segfault=(i == num_files - 1))
    create_main_file(num_files)
    print(f"Generated {num_files} C files in '{directory}'. Don't forget to compile!")
