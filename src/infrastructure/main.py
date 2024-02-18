import subprocess
import sys
from argparse import ArgumentParser, Namespace
from jobs import Job

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <executable_path> <compile_cmd>")
        sys.exit(1)

    job = Job(
        exec_path=sys.argv[1],
        compile_cmd=sys.argv[2])
    job.execute()

if __name__ == "__main__":
    main()
