from .Defn import *

GENSYM_COUNTER = 0

def gensym(name: str) -> str:
  """Generates a globally unique name, using the given one as a base"""
  uniq = f"{name}__{GENSYM_COUNTER}"
  GENSYM_COUNTER += 1
  return uniq

def lookup_defn(defns: list[Defn], name: str) -> Defn:
  """Search a list of defns to find the one that matches
  the given name, or return None"""
  for d in defns:
    if d.name == name:
      return d
  return None

def normalize(c):
  if c.isalnum():
    return c
  elif c == '-':
    return '_'
  else:
    return ''

def function_label(name: str) -> str:
  """Get a function's unique label name, given its source name"""
  norm = "".join([normalize(c) for c in name])
  hsh = abs(hash(name))
  return f"function_{norm}_{hsh}"