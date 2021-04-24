
def print_num(n):
  """Print a number with proper formatting depending on int/float"""
  if n.is_integer():
    return print(int(n))
  else:
    return print(n)