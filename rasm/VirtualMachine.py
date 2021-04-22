
class BadDest(Exception):
  """A store was made to a bad operand (imm)"""
  def __init__(self, vm, op):
    self.vm = vm
    self.op = op

class BadStackAccess(Exception):
  """Stack was accessed at an invalid index"""
  def __init__(self, vm, si):
    self.vm = vm
    self.si = si

class InvalidInstr(Exception):
  """Unknown instruction detected in program"""
  def __init__(self, vm, instr):
    self.vm = vm
    self.instr = instr

class InvalidTarget(Exception):
  """Unknown label used as a target"""
  def __init__(self, vm, label):
    self.vm = vm
    self.label = label

class BadRspOnCall(Exception):
  """Stack pointer did not point to the end of the stack
  when call was made"""
  def __init__(self, vm):
    self.vm = vm

class NoRetAddr(Exception):
  """Stack was empty when ret was made, so no addr to return to"""
  def __init__(self, vm):
    self.vm = vm

class VirtualMachine:
  def __init__(self):
    # registers
    self.rip = 0
    self.rans = 0
    self.rsp = 0

    # stack
    self.stack = [None]

    # flags
    self.fequal = False
    self.fless = False

    # for running a program
    self.pgrm = None
    self.label_addrs = {}

  def load_operand(self, op: Operand) -> int:
    """Get the current value stored in an operand"""
    if op.isRans():
      return self.rans
    if op.isRsp():
      return self.rsp
    if op.isStackOff():
      return load_stack_off(op.off)
    if op.isImm():
      return op.value

  def store_operand(self, op: Operand, value: int):
    """Store a value in the given operand"""
    if op.isRans():
      self.rans = value
    if op.isRsp():
      self.rsp = value
    if op.isStackOff():
      return store_stack_off(op.off, value)
    if op.isImm():
      raise BadDest(self, op)

  def load_stack_off(self, si: int) -> int:
    """Load a value from the stack at a given stack index"""
    idx = self.rsp + si
    if idx >= 0 and idx < len(self.stack):
      return self.stack[idx]
    else:
      raise BadStackAccess(self, si)

  def store_stack_off(self, si: int, value: int):
    """Store a value onto the stack at a given stack index"""
    idx = self.rsp + si
    if idx >= 0 and idx < len(self.stack):
      self.stack[idx] = value
    else:
      raise BadStackAccess(self, si)

  def map_labels(self, pgrm: list) -> dict:
    """Map string labels in a program to the index of 
    the instruction that follows them"""
    label_addrs = {}
    for addr in range(len(pgrm)):
      ins = pgrm[addr]
      if ins.isLabel():
        label_addrs[ins.label] = addr + 1
    return label_addrs

  def label_target(self, label: str) -> int:
    """Return the address of the instruction indicated
    by the given label, or errors if no label mapping exists"""
    if label in self.label_addrs:
      return self.label_addrs[label]
    else:
      raise InvalidTarget(self, label)

  def execute(pgrm: list):
    """Execute a program (list of instructions), leaving
    the machine in a new state"""
    self.pgrm = pgrm
    self.label_addrs = map_labels(pgrm)

    while self.rip < len(pgrm):
      self.execute_instr(pgrm[self.rip])

  def execute_instr(instr: Instr):
    """Execute a single instruction"""
    if instr.isMov():
      store_operand(instr.dest, load_operand(instr.src))

    elif instr.isAdd():
      src = load_operand(instr.src)
      dest = load_operand(instr.dest)
      store_operand(instr.dest, dest + src)

    elif instr.isSub():
      src = load_operand(instr.src)
      dest = load_operand(instr.dest)
      store_operand(instr.dest, dest - src)

    elif instr.isMul():
      src = load_operand(instr.src)
      dest = load_operand(instr.dest)
      store_operand(instr.dest, dest * src)

    elif instr.isCmp():
      src = load_operand(instr.src)
      dest = load_operand(instr.dest)
      self.fequal = (src == dest)
      self.fless = (src < dest)

    elif instr.isLabel():
      # labels don't need to do anything
      pass

    elif instr.isJmp():
      self.rip = label_target(instr.target)
      return

    # jump only if fequal set
    elif instr.isJe():
      target = label_target(instr.target)
      if self.fequal:
        self.rip = target
        return

    # jump only if fequal NOT set
    elif instr.isJne():
      target = label_target(instr.target)
      if not self.fequal:
        self.rip = target
        return 

    elif instr.isCall():
      target = label_target(instr.target)

      if self.rsp != len(self.stack) - 1:
        raise BadRspOnCall(self)

      # push return address and bump rsp
      self.stack.append(self.rip)
      self.rsp += 1

      # jump to call target
      self.rip = target
      return

    elif instr.isRet():
      if len(self.stack) == 0:
        raise NoRetAddr(self)

      # pop return address and decrement rsp
      addr = self.stack.pop()
      self.rsp -= 1

      # jump to return address
      self.rip = addr
      return

    else:
      raise InvalidInstr(self, instr)

    # default: increment instruction pointer
    self.rip += 1