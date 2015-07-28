from __future__ import print_function
import sys
import tokenize
from StringIO import StringIO
from collections import deque

def parse(text):
  tokens = tokenize.generate_tokens(StringIO(text).readline)
  for toknum, tokval, _, _, _ in tokens:
    if toknum == tokenize.NUMBER:
      yield int(tokval)
    elif toknum in [tokenize.OP, tokenize.STRING, tokenize.NAME]:
      yield tokval
    elif toknum == tokenize.ENDMARKER:
      break
    else:
      raise RuntimeError("Unknown token %s: '%s'" % (tokenize.tok_name[toknum], tokval))
    
class Stack(deque):
  push = deque.append

  def top(self):
    return self[-1]


class Machine:

  def __init__(self, code):
    self.code = code
    self.data_stack = Stack()
    self.return_addr_stack = Stack()
    self.instruction_pointer = 0

  def pop(self):
    return self.data_stack.pop()

  def push(self, value):
    self.data_stack.push(value)

  def top(self):
    return self.data_stack.top()

  def run(self):
    while self.instruction_pointer < len(self.code):
      opcode = self.code[self.instruction_pointer]
      self.instruction_pointer += 1
      self.dispatch(opcode)


  def dispatch(self, op):
    dispatch_map = {
      "*": self.mul,
      "+": self.plus,
      "/": self.div,
      "-": self.minus,
      "==": self.equal,
      "jmp": self.jmp, 
      "if": self.if_stmt,
      "print": self.print,
      "println": self.println,
      "cast_int": self.cast_int,
      "over": self.over,
      "read": self.read,
      "dup": self.dup,
      "%": self.mod,
      }
    if op in dispatch_map:
      dispatch_map[op]()
    elif isinstance(op, int):
      self.push(op)
    elif isinstance(op, str) and op[0]==op[-1]=='"':
      self.push(op[1:-1])
    else:
      raise RuntimeError("Unknown opcode: '%s'" % op)

  def plus(self):
    self.push(self.pop() + self.pop())

  def minus(self):
    last = self.pop()
    self.push(self.pop() - last)

  def mul(self):
    self.push(self.pop() * self.pop())

  def div(self):
    last = self.pop()
    self.push(self.pop() / last)

  def equal(self):
    self.push(self.pop() == self.pop())

  def jmp(self):
    addr = self.pop()
    if isinstance(addr, int) and 0 <= addr < len(self.code):
      self.instruction_pointer = addr
    else:
      raise RuntimeError("JMP address must be a valid integer.")

  def if_stmt(self):
    false_clause = self.pop()
    true_clause = self.pop()
    test = self.pop()
    self.push(true_clause if test else false_clause) 

  def cast_int(self):
    self.push(int(self.pop()))

  def over(self):
    b = self.pop()
    a = self.pop()
    self.push(a)
    self.push(b)
    self.push(a)

  def read(self):
    self.push(raw_input())

  def dup(self):
    a = self.push(self.top())

  def mod(self):
    last = self.pop()
    self.push(self.pop() % last)

  def print(self):
    sys.stdout.write(str(self.pop()))
    sys.stdout.flush()

  def println(self):
    sys.stdout.write("%s\n" % self.pop())
    sys.stdout.flush()



def repl():
  print('Enter expression to be evaluated as a string')
  expr = raw_input("> ")
  expr = expr.split(' ')
  ar = []
  for i in expr:
    try:
      ar.append(int(i))
    except:
      ar.append(i)
  ar.append('println')
  ans = Machine(ar).run()
