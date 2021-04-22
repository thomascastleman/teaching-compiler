
class Operand:
  def isImm(self):
    return isinstance(self, Imm)

  def isRans(self):
    return isinstance(self, Rans)

  def isRsp(self):
    return isinstance(self, Rsp)

  def isStackOff(self):
    return isinstance(self, StackOff)

class Imm(Operand):
  """Immediate value"""
  def __init__(self, value):
    self.value = value

  def __eq__(self, other):
    return isinstance(other, Imm) and \
      self.value == other.value

  def __str__(self):
    return str(self.value)

class Rans(Operand):
  """Answer register rans"""
  def __init__(self):
    pass

  def __eq__(self, other):
    return isinstance(other, Rans)

  def __str__(self):
    return "rans"

class Rsp(Operand):
  """Stack pointer register rsp"""
  def __init__(self):
    pass

  def __eq__(self, other):
    return isinstance(other, Rsp)

  def __str__(self):
    return "rsp"

class StackOff(Operand):
  """Offset from stack pointer"""
  def __init__(self, off):
    self.off = off
  
  def __eq__(self, other):
    return isinstance(other, StackOff) and \
      self.off == other.off

  def __str__(self):
    return f"[rsp + {self.off}]"