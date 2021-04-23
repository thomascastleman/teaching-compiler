from typing import List
import re

class Pattern:
  def __init__(self, regex, make_token):
    self.regex = regex
    self.make_token = make_token

  def match(self, text: str):
    """If the text has a prefix matching this pattern, return
    the prefix"""
    m = re.match(self.regex, text)

    if m is None:
      return None

    return m.group(0)

class Token:
  def __init__(self, name, lexeme):
    self.name = name
    self.lexeme = lexeme

class Lexer:
  def __init__(self, patterns):
    self.patterns = patterns

  def lex(pgrm: str) -> List[Token]:
    """Lex a program to produce a list of tokens"""
    tokens = []
    # while there are tokens left to lex
    while len(pgrm) > 0:
      longest_mat = None
      longest_mat_token = None

      for pat in self.patterns:
        mat = pat.match(pgrm)
        if mat is None:
          continue

        # new longest match, replace old
        if longest_mat is None or len(mat) > len(longest_mat):
          longest_mat = mat
          longest_mat_token = pat.make_token(mat)
      
      # didn't match any pattern
      if longest_mat is None: 
        raise InvalidToken(pgrm)

      after_mat = len(longest_mat)
      assert after_mat > 0

      # add token and move past lexeme in input
      if longest_mat_token is not None:
        tokens.push(longest_mat_token)
      pgrm = pgrm[after_mat:]


class InvalidToken(Exception):
  def __init__(self, pgrm):
    self.pgrm = pgrm