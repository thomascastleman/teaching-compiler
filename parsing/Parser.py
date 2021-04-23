
class Parser:

  def __init__(self, display_token_name):
    self.display_token_name = display_token_name

  def setup(self, tokens):
    """Resets the parser state"""
    self.tokens = tokens
    self.index = 0

  def peek(self):
    """Peek at the input stream at the current token"""
    return self.tokens[self.index]

  def next(self):
    """Move past the current token, returning it"""
    tok = self.peek()
    self.index += 1
    return tok

  def eat(self, tok_name):
    """Consume the next token in the input stream,
    erroring if it is not what is expected"""
    actual_tok_name = self.tokens[self.index].name
    if actual_tok_name == tok_name:
      self.index += 1
    else:
      raise ParseError(
        f"expected token {self.display_token_name(tok_name)}, " + \
        f"got {self.display_token_name(actual_tok_name)}")

  def eat_prefix(self, prefix):
    """Eats all token names in a prefix"""
    for name in prefix:
      self.eat(name)

  def matches(self, name) -> bool:
    """Given a token name, determine if the first token
    on the input stream matches"""
    return self.peek().name == name

  def matches_prefix(self, prefix: list) -> bool:
    """Given a prefix of token names, determine if the 
    front of the token stream matches the prefix"""
    if len(self.tokens) - self.index < len(prefix):
      return False

    for i in range(len(prefix)):
      if self.tokens[self.index + i].name != prefix[i]:
        return False
    return True


class ParseError(Exception):
  def __init__(self, msg):
    self.msg = msg