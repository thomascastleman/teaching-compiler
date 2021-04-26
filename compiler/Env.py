import copy

class Env:
  """Environment, mapping names to stack indices"""

  def __init__(self):
    """Constructs a new empty environment"""
    self.map = {}

  def extend(self, name: str, si: int):
    """Extends an environment with a new binding (returns extended env)"""
    cp = copy.deepcopy(self)
    cp.map[name] = si
    return cp

  def lookup(self, name: str) -> int:
    """Lookup the stack index associated with a name in an Env.
    Returns None if no stack index found."""
    if name in self.map:
      return self.map[name]
    else:
      return None