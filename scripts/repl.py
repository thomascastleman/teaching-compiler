import signal
import sys
import argparse
from .util import *
from parsing.parse_program import *
from rasm.VirtualMachine import *
from compiler.compile import *

argparser = argparse.ArgumentParser(description="Launch a repl")
argparser.add_argument(
  '-d', '--demo', 
  help='launch a repl using the demo implementation',
  action='store_true')
args = argparser.parse_args()

def quit_handler(sig, frame):
  """Quit from the REPL on receipt of a signal"""
  print("\nExiting REPL")
  sys.exit(0)

def launch_repl(compile):
  """Creates a REPL which reads input from stdin, parses/compiles/runs, 
  then prints the resulting value"""
  # handle SIGINT by exiting gracefully
  signal.signal(signal.SIGINT, quit_handler)

  defns = []
  vm = VirtualMachine()

  # REPL loop
  while True:
    pgrm = input("> ")
    try:
      parsed = parse_program(pgrm)

      # add defns to running list
      defns += parsed[0]
      body = parsed[1]

      # if body expression entered, run it with current defns
      if body:
        instrs = compile(defns, body)
        vm.execute(instrs)
        print_num(vm.rans)
    except EmptyProgram:
      continue
    except (LexError, ParseError, CompileError, VMError) as err:
      print(err)
    except Exception as err:
      print(f"InternalError: {err}")

print(args.demo)

# TODO: if args.demo then use the demo implementation
launch_repl(compile)