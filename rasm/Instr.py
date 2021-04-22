
class Instr:
  def isMov(self):
    return isinstance(self, Mov)

  def isAdd(self):
    return isinstance(self, Add)

  def isSub(self):
    return isinstance(self, Sub)

  def isMul(self):
    return isinstance(self, Mul)

  def isCmp(self):
    return isinstance(self, Cmp)

  def isLabel(self):
    return isinstance(self, Label)

  def isJmp(self):
    return isinstance(self, Jmp)

  def isJe(self):
    return isinstance(self, Je)

  def isJne(self):
    return isinstance(self, Jne)

  def isCall(self):
    return isinstance(self, isCall)

  def isRet(self):
    return isinstance(self, Ret)

class Mov(Instr):
  def __init__(self, src, dest):
    self.src = src
    self.dest = dest

  def __eq__(self, other):
    return isinstance(other, Mov) and \
      self.src == other.src and \
      self.dest == other.dest

class Add(Instr):
  def __init__(self, src, dest):
    self.src = src
    self.dest = dest

  def __eq__(self, other):
    return isinstance(other, Add) and \
      self.src == other.src and \
      self.dest == other.dest

class Sub(Instr):
  def __init__(self, src, dest):
    self.src = src
    self.dest = dest

  def __eq__(self, other):
    return isinstance(other, Sub) and \
      self.src == other.src and \
      self.dest == other.dest

class Mul(Instr):
  def __init__(self, src, dest):
    self.src = src
    self.dest = dest

  def __eq__(self, other):
    return isinstance(other, Mul) and \
      self.src == other.src and \
      self.dest == other.dest

class Cmp(Instr):
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def __eq__(self, other):
    return isinstance(other, Cmp) and \
      self.left == other.left and \
      self.right == other.right

class Label(Instr):
  def __init__(self, label):
    self.label = label
  
  def __eq__(self, other):
    return isinstance(other, Label) and \
      self.label == other.label
  
class Jmp(Instr):
  def __init__(self, target):
    self.target = target
  
  def __eq__(self, other):
    return isinstance(other, Jmp) and \
      self.target == other.target

class Je(Instr):
  def __init__(self, target):
    self.target = target
  
  def __eq__(self, other):
    return isinstance(other, Je) and \
      self.target == other.target

class Jne(Instr):
  def __init__(self, target):
    self.target = target
  
  def __eq__(self, other):
    return isinstance(other, Jne) and \
      self.target == other.target

class Call(Instr):
  def __init__(self, target):
    self.target = target

  def __eq__(self, other):
    return isinstance(other, Call) and \
      self.target == other.target

class Ret(Instr):
  def __init__(self):
    pass

  def __eq__(self, other):
    return isinstance(other, Ret)