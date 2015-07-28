class Machine(object):

  def __init__(self, program):
    self.program = program
    self.a = self.b = self.t = None
    self.flag = False
    self.pc = 0

  def execute(self):
    while self.pc < len(self.program):
      i = self.program[self.pc]
      print(self.pc, self.a, self.b, self.t, self.flag)
      instr, rest = i[0], i[1:]
      self.pc += 1
      getattr(self, 'i_' + instr)(*rest)

  def i_copy(self, a, b):
    setattr(self, a, getattr(self, b))

  def i_set(self, a, b):
    setattr(self, a, b)

  def i_exec(self, reg, a, b, op):
    setattr(self, reg, getattr(self, 'o_' + op)(a, b))

  def o_add(self, a, b):
    return getattr(self, a) + getattr(self, b)

  def o_sub(self, a, b):
    return getattr(self, a) - getattr(self, b)

  def o_mult(self, a, b):
    return getattr(self, a) * getattr(self, b)

  def o_div(self, a, b):
    return getattr(self, a) / getattr(self, b)

  def o_mod(self, a, b):
    return getattr(self, a) % getattr(self, b)

def repl():
  print("Enter expression to be evaluated as a string")
  expr = raw_input("> ")
  expr = expr.split(" ")
  op = expr[2]
  m = Machine((('exec','t','a','b',op),))
  m.a = int(expr[0])
  m.b = int(expr[1])
  m.execute()
  print m.t
  print("Perform another operation? y/n")
  ans = raw_input("> ")
  if ans.lower() != 'n' and ans != 'no': 
    repl()

##m = Machine((('exec','t', 'a', 'b', 'add'),('exec','t','b','t','sub')))
##m.a = 56
##m.b = 63
##m.execute()
##print m.t
