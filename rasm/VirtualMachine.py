
from .Operand import *
from .Instr import *

STACK_SIZE = 10_000
ENTRY_LABEL = "entry"

class VirtualMachine:
  def __init__(self):
    # registers
    self.rip = 0
    self.rans = 0
    self.rsp = 0

    # stack, a big buffer
    self.stack = [0 for i in range(STACK_SIZE)]

    # flags
    self.fequal = False
    self.fless = False

    # for running a program
    self.pgrm = None
    self.label_addrs = {}

  def __str__(self):
    """Dump machine state into a string for error messages"""
    if self.rip >= 0 and self.rip < len(self.pgrm):
      cur_instr = str(self.pgrm[self.rip])
    else:
      cur_instr = f"no instruction at rip={self.rip}"

    return \
      "Registers:\n" + \
      f"rip={self.rip} rans={self.rans} rsp={self.rsp}\n" + \
      "Flags:\n" + \
      f"fequal={self.fequal} fless={self.fless}" + \
      "Stack: (first 15)\n" + \
      f"{self.stack[:15]}..." + \
      "Current Instruction:\n" + \
      cur_instr

  def load_operand(self, op: Operand) -> int:
    """Get the current value stored in an operand"""
    if op.isRans():
      return self.rans
    if op.isRsp():
      return self.rsp
    if op.isStackOff():
      idx = self.rsp + op.off
      if idx >= 0 and idx < STACK_SIZE:
        return self.stack[idx]
      else:
        raise BadStackAccess(self, op.off)
    if op.isImm():
      return op.value

  def store_operand(self, op: Operand, value: int):
    """Store a value in the given operand"""
    if op.isRans():
      self.rans = value
    if op.isRsp():
      self.rsp = value
    if op.isStackOff():
      idx = self.rsp + op.off
      if idx >= 0 and idx < STACK_SIZE:
        self.stack[idx] = value
      else:
        raise BadStackAccess(self, op.off)
    if op.isImm():
      raise BadDest(self, op)

  def map_labels(self, pgrm: list) -> dict:
    """Map string labels in a program to the index of 
    the instruction that follows them"""
    label_addrs = {}
    for addr in range(len(pgrm)):
      ins = pgrm[addr]
      if ins.isLabel():
        # duplicate labels are not allowed
        if ins.label in label_addrs:
          raise DuplicateLabel(ins.label)
        label_addrs[ins.label] = addr + 1
    return label_addrs

  def label_target(self, label: str) -> int:
    """Return the address of the instruction indicated
    by the given label, or errors if no label mapping exists"""
    if label in self.label_addrs:
      return self.label_addrs[label]
    else:
      raise InvalidTarget(self, label)

  def execute(self, pgrm: list):
    """Execute a program (list of instructions), leaving
    the machine in a new state"""
    self.pgrm = pgrm
    self.label_addrs = self.map_labels(pgrm)

    if ENTRY_LABEL not in self.label_addrs:
      raise NoEntry(pgrm)

    # start execution at the entry label
    self.rip = self.label_addrs[ENTRY_LABEL]

    # when rip has incremented past last instr, halt
    while self.rip != len(pgrm):
      if self.rip < 0 or self.rip > len(pgrm):
        raise InvalidRip(self)
      self.execute_instr(pgrm[self.rip])

  def execute_instr(self, instr: Instr):
    """Execute a single instruction"""
    # copy src into dest
    if instr.isMov():
      self.store_operand(instr.dest, self.load_operand(instr.src))

    # add operands
    elif instr.isAdd():
      src = self.load_operand(instr.src)
      dest = self.load_operand(instr.dest)
      self.store_operand(instr.dest, dest + src)

    # subtract operands
    elif instr.isSub():
      src = self.load_operand(instr.src)
      dest = self.load_operand(instr.dest)
      self.store_operand(instr.dest, dest - src)

    # multiply operands
    elif instr.isMul():
      src = self.load_operand(instr.src)
      dest = self.load_operand(instr.dest)
      self.store_operand(instr.dest, dest * src)

    # compare operands, set flags
    elif instr.isCmp():
      left = self.load_operand(instr.left)
      right = self.load_operand(instr.right)
      self.fequal = (left == right)
      self.fless = (left < right)

    # labels don't need to do anything
    elif instr.isLabel():
      pass

    # unconditionally update rip
    elif instr.isJmp():
      self.rip = self.label_target(instr.target)
      return

    # jump only if fequal set
    elif instr.isJe():
      target = self.label_target(instr.target)
      if self.fequal:
        self.rip = target
        return

    # jump only if fequal NOT set
    elif instr.isJne():
      target = self.label_target(instr.target)
      if not self.fequal:
        self.rip = target
        return 

    # push ret addr and jump to function label
    elif instr.isCall():
      target = self.label_target(instr.target)

      # push return address
      self.rsp += 1
      if self.rsp < 0 or self.rsp >= STACK_SIZE:
        raise InvalidRsp(self)
      self.stack[self.rsp] = self.rip + 1

      # jump to call target
      self.rip = target
      return

    # pop ret addr, jump to it
    elif instr.isRet():
      if self.rsp < 0 or self.rsp >= STACK_SIZE:
        raise InvalidRsp(self)

      # pop return address and decrement rsp
      addr = self.stack[self.rsp]
      self.rsp -= 1

      # jump to return address
      self.rip = addr
      return

    else:
      raise InvalidInstr(self, instr)

    # default: increment instruction pointer
    self.rip += 1


# ============= Virtual Machine Errors =============

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

class InvalidRip(Exception):
  """Bad value for rip"""
  def __init__(self, vm):
    self.vm = vm

class InvalidRsp(Exception):
  """Bad value for rsp"""
  def __init__(self, vm):
    self.vm = vm

class DuplicateLabel(Exception):
  """More than one instance of a given label"""
  def __init__(self, label):
    self.label = label

class NoEntry(Exception):
  """Program has no entry label"""
  def __init__(self, pgrm):
    self.pgrm = pgrm