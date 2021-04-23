import unittest
from compiler.compile import *

ENTRY_LABEL = "entry"

class CompilerTests(unittest.TestCase):
  
  def test_it_works(self):
    self.assertEqual(
      compile([], Num(5)),
      [Label(ENTRY_LABEL),
      Mov(Imm(5), Rans())])

if __name__ == '__main__':
  unittest.main()