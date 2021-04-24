import signal
import sys
from .util import *
from parsing.parse_program import *
from compiler.compile import *
from rasm.VirtualMachine import *

def quit_handler(sig, frame):
  """Quit from the REPL on receipt of a signal"""
  print("\nExiting REPL")
  sys.exit(0)

def launch_repl():
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

launch_repl()