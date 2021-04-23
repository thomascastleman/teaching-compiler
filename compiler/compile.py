from typing import List
from .Defn import *
from .Expr import *
from .Env import *
from .util import *
from rasm.Instr import *
from rasm.Operand import *

def compile(defns: List[Defn], body: Expr) -> List[Instr]:
  """Consumes a program (list of function definitions and a body) 
  and generates equivalent code in the target language"""
  # compile definitions
  defn_instrs = []
  for d in defns:
    defn_instrs += compile_defn(defns, d)

  # compile body
  body_instrs = compile_expr(defns, body, 1, Env())

  return defn_instrs + [Label("entry")] + body_instrs

def compile_expr(defns: List[Defn], exp: Expr, si: int, env: Env) -> List[Instr]:
  """Generates instructions for a given expression, at a given stack
  index, and in a given environment"""
  if exp.isNum():
    return [Mov(Imm(exp.value), Rans())]

  if exp.isAdd1():
    return \
      compile_expr(defns, exp.operand, si, env) + \
      [Add(Imm(1), Rans())]

  elif exp.isSub1():
    return \
      compile_expr(defns, exp.operand, si, env) + \
        [Sub(Imm(1), Rans())]

  elif exp.isPlus():
    return \
      compile_expr(defns, exp.left, si, env) + \
      [Mov(Rans(), StackOff(si))] + \
      compile_expr(defns, exp.right, si + 1, env) + \
      [Add(StackOff(si), Rans())]

  elif exp.isMinus():
    return \
      compile_expr(defns, exp.left, si, env) + \
      [Mov(Rans(), StackOff(si))] + \
      compile_expr(defns, exp.right, si + 1, env) + \
      [Sub(Rans(), StackOff(si)),
      Mov(StackOff(si), Rans())]

  elif exp.isTimes():
    return \
      compile_expr(defns, exp.left, si, env) + \
      [Mov(Rans(), StackOff(si))] + \
      compile_expr(defns, exp.right, si + 1, env) + \
      [Mul(StackOff(si), Rans())]

  elif exp.isEquals():
    not_equal = gensym("not_equal")
    cont = gensym("continue")
    return \
      compile_expr(defns, exp.left, si, env) + \
      [Mov(Rans(), StackOff(si))] + \
      compile_expr(defns, exp.right, si + 1, env) + \
      [Cmp(StackOff(si), Rans()), # compare operands
      Jne(not_equal),
      Mov(Imm(1), Rans()), # evaluates to 1
      Jmp(cont),
      Label(not_equal),
      Mov(Imm(0), Rans()), # evaluates to 0
      Label(cont)]

  elif exp.isIf():
    else_lbl = gensym("else")
    cont = gensym("continue")

    cond_instrs = compile_expr(defns, exp.cond, si, env)
    thn_instrs = compile_expr(defns, exp.thn, si, env)
    els_instrs = compile_expr(defns, exp.els, si, env)

    return \
      cond_instrs + \
      [Cmp(Imm(0), Rans()), # if condition is 0, go to else
      Je(else_lbl)] + \
      thn_instrs + \
      [Jmp(cont),
      Label(else_lbl)] + \
      els_instrs + \
      [Label(cont)]

  elif exp.isLet():
    value_instrs = compile_expr(defns, exp.value, si, env)
    ext_env = env.extend(exp.name, si)
    body_instrs = compile_expr(defns, exp.body, si + 1, ext_env)

    return value_instrs + \
      [Mov(Rans(), StackOff(si))] + \
      body_instrs

  elif exp.isApp():
    defn = lookup_defn(defns, exp.fname)

    if defn is None:
      raise UndefinedFun(exp.fname)

    if len(exp.args) != len(defn.params):
      raise ArityMismatch(exp.args, defn)

    # stack base is highest currently in-use stack index
    stack_base_idx = si - 1
    fn_label = function_label(defn.name)

    arg_instrs = []
    for i in range(len(exp.args)):
      arg = exp.args[i]

      # arguments start at stack base + 2
      # return addr goes at stack base + 1
      arg_si = stack_base_idx + 2 + i

      arg_instrs += compile_expr(defns, arg, arg_si, env)
      arg_instrs += [Mov(Rans(), StackOff(arg_si))]

    return \
      arg_instrs + \
      [Add(Imm(stack_base_idx), Rsp()),
      Call(fn_label),
      Sub(Imm(stack_base_idx), Rsp())]

  elif exp.isName():
    name_si = env.lookup(exp.name)

    if name_si is None:
      raise UnboundName(exp.name)

    return [Mov(StackOff(name_si), Rans())]

  else:
    raise ValueError(f"compile_expr: unexpected expression: {exp}")

def compile_defn(defns: List[Defn], defn: Defn) -> List[Instr]:
  """Generates instructions for a function definition"""
  # bind parameters to successive stack locs starting at si = 1
  # si = 0 is the return address
  env = Env()
  for i in range(len(defn.params)):
    param = defn.params[i]
    env = env.extend(param, i + 1)

  # next si is stack index after all arguments
  next_si = 1 + len(defn.params)

  # function label, then body, then return
  return \
    [Label(function_label(defn.name))] + \
    compile_expr(defns, defn.body, next_si, env) + \
    [Ret()]


# ============= Compile Errors =============

class CompileError(Exception):
  pass

class ArityMismatch(CompileError):
  def __init__(self, args, defn):
    self.args = args
    self.defn = defn

class UndefinedFun(CompileError):
  def __init__(self, fname):
    self.fname = fname

class UnboundName(CompileError):
  def __init__(self, name):
    self.name = name