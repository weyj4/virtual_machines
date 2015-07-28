import stack
import register

def repl():
  print("Enter expression to be evaluated as a string")
  expr = raw_input("> ")
  expr = expr.split(" ")
  print("Stack or register?")
  choice = raw_input("> ")
  if choice.lower() == "stack":
    ar = []
    for i in expr:
      try:
        ar.append(int(i))
      except:
        ar.append(i)
    ar.append('println')
    stack.Machine(ar).run()
  elif choice.lower() == "register":
    from register import Machine
    op = expr[2]
    m = register.Machine((('exec','t','a','b',op),))
    m.a = int(expr[0])
    m.b = int(expr[1])
    m.execute()
    print m.t
  print("Perform another operation? y/n")
  ans = raw_input("> ")
  if ans.lower() != 'n' and ans != 'no': 
    repl()

if __name__ == "__main__":
  repl()
