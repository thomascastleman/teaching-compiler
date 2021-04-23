from typing import List
from enum import Enum, auto
from compiler.Defn import *
from compiler.Expr import *
from .Lexer import *

class Tok(Enum):
  LPAREN = auto()
  RPAREN = auto()
  SYM = auto()
  NUM = auto()
  DEF = auto()
  ADD1 = auto()
  SUB1 = auto()
  PLUS = auto()
  MINUS = auto()
  TIMES = auto()
  EQUALS = auto()
  IF = auto()
  LET = auto()

def parse_program(pgrm: str) -> (List[Defn], Expr):
  """Parses a string program to produce a list of function
  definitions and a program body expression"""
  lexer = Lexer([
    Pattern(r"\(",                        lambda s: Token(Tok.LPAREN, None)),
    Pattern(r"\)",                        lambda s: Token(Tok.RPAREN, None)),
    Pattern(r"\s+",                       lambda s: None),
    Pattern(r"def",                       lambda s: Token(Tok.DEF, None)),
    Pattern(r"add1",                      lambda s: Token(Tok.ADD1, None)),
    Pattern(r"sub1",                      lambda s: Token(Tok.SUB1, None)),
    Pattern(r"\+",                        lambda s: Token(Tok.PLUS, None)),
    Pattern(r"\-",                        lambda s: Token(Tok.MINUS, None)),
    Pattern(r"\*",                        lambda s: Token(Tok.TIMES, None)),
    Pattern(r"=",                         lambda s: Token(Tok.EQUALS, None)),
    Pattern(r"if",                        lambda s: Token(Tok.IF, None)),
    Pattern(r"let",                       lambda s: Token(Tok.LET, None)),
    Pattern(r"-?[0-9]+(\.[0-9]+)?",       lambda s: Token(Tok.NUM, float(s))),
    Pattern(r"[a-zA-Z][a-zA-Z0-9\?\!-]*", lambda s: Token(Tok.SYM, s)),
  ])

  tokens = lexer.lex(pgrm)
  parser = ProgramParser(tokens)

  return parser.parse()

class ProgramParser(Parser):

  def parse() -> (List[Defn], Expr):
    """Parses a full program (defns and then a body) from its 
    input token stream"""
    assert self.tokens is not None

    defn_prefix = [
      Tok.LPAREN,
      Tok.DEF
    ]

    # parse any defns in the program
    defns = []
    while self.prefix_matches(defn_prefix):
      defns.push(self.parse_defn())

    # parse program body
    body = self.parse_expr()

    if len(self.tokens) > 0:
      raise BodyNotLast()

    return (defns, body)

  def parse_defn() -> Defn:
    self.eat_prefix([
      Tok.LPAREN,
      Tok.DEF,
      Tok.LPAREN,
    ])

    # function name should be a valid symbol
    if not self.prefix_matches([Tok.SYM]):
      raise InvalidFunName(self.next())
    fname = self.next().lexeme

    # parse parameter names (symbols)
    params = []
    while self.prefix_matches([Tok.SYM]):
      params.push(self.next().lexeme)

    # closing paren for param list
    self.eat(Tok.RPAREN)  

    # parse body and defn closing paren
    body = self.parse_expr()
    self.eat(Tok.RPAREN)

    return Defn(fname, params, body)

  def parse_expr() -> Expr:
    """Parses an expression off the input stream"""
    if self.matches(Tok.LPAREN):
      self.eat(Tok.LPAREN)

      if self.matches(Tok.ADD1):
        self.eat(Tok.ADD1)
        operand = self.parse_expr()
        self.eat(Tok.RPAREN)
        return Add1(operand)

      elif self.matches(Tok.SUB1):
        self.eat(Tok.SUB1)
        operand = self.parse_expr()
        self.eat(Tok.RPAREN)
        return Sub1(operand)

      elif self.matches(Tok.PLUS):
        self.eat(Tok.PLUS)
        left = self.parse_expr()
        right = self.parse_expr()
        self.eat(Tok.RPAREN)
        return Plus(left, right)

      elif self.matches(Tok.MINUS):
        self.eat(Tok.MINUS)
        left = self.parse_expr()
        right = self.parse_expr()
        self.eat(Tok.RPAREN)
        return Minus(left, right)

      elif self.matches(Tok.TIMES):
        self.eat(Tok.TIMES)
        left = self.parse_expr()
        right = self.parse_expr()
        self.eat(Tok.RPAREN)
        return Times(left, right)

      elif self.matches(Tok.EQUALS):
        self.eat(Tok.EQUALS)
        left = self.parse_expr()
        right = self.parse_expr()
        self.eat(Tok.RPAREN)
        return Equals(left, right)

      # conditionals
      elif self.matches(Tok.IF):
        self.eat(Tok.IF)
        cond = self.parse_expr()
        thn = self.parse_expr()
        els = self.parse_expr()
        self.eat(Tok.RPAREN)
        return If(cond, thn, els)

      # let bindings
      elif self.matches(Tok.LET):
        self.eat(Tok.LET)
        self.eat(Tok.LPAREN)
        
        if not self.matches(Tok.SYM):
          raise InvalidVarName(self.next())
        
        name = self.next().lexeme
        value = self.parse_expr()
        self.eat(Tok.RPAREN)
        body = self.parse_expr()
        self.eat(Tok.RPAREN)

        return Let(name, value, body)
      
      # must be an App
      else:
        if not self.matches(Tok.SYM):
          raise InvalidFunInApp(self.next())
        
        name = self.next().lexeme
        args = []
        while not self.matches(Tok.RPAREN):
          args.push(self.parse_expr())
        
        self.eat(Tok.RPAREN)
        return App(name, args)

    # number literals
    elif self.matches(Tok.NUM):
      n = self.next().lexeme
      return Num(n)

    # identifier names
    elif self.matches(Tok.SYM):
      name = self.next().lexeme
      return Name(name)

    else:
      raise InvalidExpr(self.tokens)

class BodyNotLast(Exception):
  def __init__(self, extra_tokens):
    self.extra_tokens = extra_tokens

class InvalidFunName(Exception):
  def __init__(self, token):
    self.token = token

class InvalidVarName(Exception):
  def __init__(self, token):
    self.token = token

class InvalidFunInApp(Exception):
  def __init__(self, token):
    self.token = token

class InvalidExpr(Exception):
  def __init__(self, tokens):
    self.tokens = tokens