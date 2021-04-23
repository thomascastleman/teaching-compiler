from .Defn import *
from .Expr import *
from .Env import *
from rasm.Instr import *

def compile(defns: list[Defn], body: Expr) -> list[Instr]:
  """Consumes a program (list of function definitions and a body) 
  and generates equivalent code in the target language"""
  pass

def compile_expr(defns: list[Defn], exp: Expr, si: int, env: Env) -> list[Instr]:
  """Generates instructions for a given expression, at a given stack
  index, and in a given environment"""
  pass

def compile_defn(defn: Defn) -> list[Instr]:
  """Generates instructions for a function definition"""
  pass