from typing import List
from .Expr import *
from .Defn import *

# ============= Compile Errors =============

class CompileError(Exception):
  pass

class ArityMismatch(CompileError):
  def __init__(self, args: List[Expr], defn: Defn):
    self.args = args
    self.defn = defn

  def __str__(self):
    return f"CompileError: arity mismatch: {self.defn.name} expects " + \
      f"{len(self.defn.params)} arguments, but given {len(self.args)}"

class UndefinedFun(CompileError):
  def __init__(self, fname: str):
    self.fname = fname

  def __str__(self):
    return f"CompileError: function '{self.fname}' not defined"

class UnboundName(CompileError):
  def __init__(self, name: str):
    self.name = name

  def __str__(self):
    return f"CompileError: unbound name '{self.name}'"