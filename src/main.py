import sys
from argparse import ArgumentParser, Namespace
from jobs import Job

def parse_args() -> Namespace:
    parser = ArgumentParser(prog='coderepair')

    parser.add_argument(
        "-e",
        "--executable",
        help="Path to the executable to run your test suite",
    )
    parser.add_argument(
        "-c",
        "--compile-cmd",
        help="Command to recompile your executable as inputed with -e/--executable flag",
    )

    args = parser.parse_args()

    if len(vars(args)) < 2:
        parser.error("both the arguments -e/--executable and -c/--compile-cmd are required")

    return args

def main():
    args = parse_args()
    job = Job(
        exec_path=args.executable,
        compile_cmd=args.compile_cmd)
    job.execute()

if __name__ == "__main__":
    main()
