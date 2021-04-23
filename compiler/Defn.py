
class Defn:
  def __init__(self, name, params, body):
    self.name = name
    self.params = params
    self.body = body
  
  def __eq__(self, other):
    return isinstance(other, Defn) and \
      self.name == other.name and \
      self.params == other.params and \
      self.body == other.body

  def __str__(self):
    params = " ".join(self.params)
    return f"(def ({self.name} {params})\n\t{self.body})"