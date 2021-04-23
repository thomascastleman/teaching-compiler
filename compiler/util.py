from .Defn import *
from typing import List

GENSYM_COUNTER = 0

def gensym(name: str) -> str:
  """Generates a globally unique name, using the given one as a base"""
  uniq = f"{name}__{GENSYM_COUNTER}"
  GENSYM_COUNTER += 1
  return uniq

def lookup_defn(defns: List[Defn], name: str) -> Defn:
  """Searches a list of defns to find the one that matches
  the given name, or returns None"""
  for d in defns:
    if d.name == name:
      return d
  return None

def normalize(c: str) -> str:
  """Returns the given char if alphanumeric, or normalizes/elides it"""
  if c.isalnum():
    return c
  elif c == '-':
    return '_'
  else:
    return ''

def function_label(name: str) -> str:
  """Gets a function's unique label name, given its source name"""
  norm = "".join([normalize(c) for c in name])
  hsh = abs(hash(name))
  return f"function_{norm}_{hsh}"