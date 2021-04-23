from .Defn import *
from .Expr import *
from .Env import *
from .util import *
from rasm.Instr import *
from rasm.Operand import *

def compile(defns: list[Defn], body: Expr) -> list[Instr]:
  """Consumes a program (list of function definitions and a body) 
  and generates equivalent code in the target language"""
  # compile definitions
  defn_instrs = []
  for d in defns:
    defn_instrs += compile_defn(d)

  # compile body
  body_instrs = compile_expr(defns, body, 1, Env())

  return defn_instrs + [Label("entry")] + body_instrs

def compile_expr(defns: list[Defn], exp: Expr, si: int, env: Env) -> list[Instr]:
  """Generates instructions for a given expression, at a given stack
  index, and in a given environment"""
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

    if len(exp.args) != len(defn.args):
      raise ArityMismatch(exp.args, defn)

    # compile arguments, put them on the stack above ret addr loc
    # adjust rsp
    # call
    # adjust rsp

  elif exp.isName():
    pass
  else:
    raise ValueError(f"compile_expr: unexpected expression: {exp}")

def compile_defn(defn: Defn) -> list[Instr]:
  """Generates instructions for a function definition"""
  pass

# ============= Compile Errors =============

class ArityMismatch(Exception):
  def __init__(self, args, defn):
    self.args = args
    self.defn = defn

class UndefinedFun(Exception):
  def __init__(self, fname):
    self.fname = fname

class UnboundName(Exception):
  def __init__(self, name):
    self.name = name