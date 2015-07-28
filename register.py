class Machine(object):

  def __init__(self, program):
    self.program = program
    self.a = self.b = self.t = None
    self.flag = False
    self.pc = 0

  def execute(self):
    while self.pc < len(self.program):
      i = self.program[self.pc]
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
