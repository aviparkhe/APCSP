import math

print("COMMANDS:")
print('''
A + B        add A and B
A - B        subtract B from A
A * B        multiply A and B
A / B        divide A by B (B ≠ 0)
A ^ B        raise A to the Bth power
A mod B      find the remainder when A is divided by B (B ≠ 0)
A log B      find the logarithm of B with base A
ANS          the most recent computed value
MEM          display current memory
MEM#         the #th item in memory
MEM#=A       set the #th term in memory to A
CLEAR MEM    clear the memory
EXIT         quit the calculator
''')

mem = [0.0] * 20
ans = 0


def calculate(exp):
  parts = exp.split()
  if len(parts) != 3:
    return "ERROR: INVALID FORMAT"

  if parts[0] == "E":
    n1 = math.e
  elif parts[0] == "PI":
    n1 = math.pi
  else:
    n1 = float(parts[0])

  if parts[2] == "E":
    n2 = math.e
  elif parts[2] == "PI":
    n2 = math.pi
  else:
    n2 = float(parts[2])

  op = parts[1]
  try:
    if op == "+":
      r = n1 + n2
    elif op == "-":
      r = n1 - n2
    elif op == "*":
      r = n1 * n2
    elif op == "/":
      try:
        r = n1 / n2
      except ZeroDivisionError:
        return "ERROR: DIVISION BY ZERO"
    elif op == "^":
      r = n1**n2
    elif op == "MOD":
      try:
        r = n1 % n2
      except ZeroDivisionError:
        return "ERROR: MODULO BY ZERO"
    elif op == "LOG":
      r = math.log(n2) / math.log(n1)  # using change of base formula with ln
    else:
      return "ERROR: INVALID OPERATION"
  except OverflowError:
    return "ERROR: RESULT TOO LARGE"

  try:
    return int(r) if r == int(r) else round(r, 3)
  except ValueError:
    return round(r, 3)


def store(val, pos=None):
  if pos is None:
    mem.append(val)
  else:
    mem[pos - 1] = val


def print_mem(pos=None):
  if pos:
    print(f"MEM{pos}".ljust(10) + str(mem[pos - 1]))
  else:
    for i, term in enumerate(mem):
      print(f"MEM{i + 1}".ljust(10) + str(term))


# program running loop
while True:
  expression = input("> ").upper().replace("ANS", str(ans))

  if "MEM" in expression:

    if len(expression) == 3:
      print_mem()
    elif expression.split() == [expression
                                ]:  # checks if expression is MEM# or MEM=#
      if "=" in expression:
        expression = expression.replace("ANS", str(ans))
        idx = expression.find("=")
        val = float(expression[(idx + 1):])
        mem_loc = int(expression[:idx][3:])
        mem[mem_loc - 1] = val
        print_mem(mem_loc)
      else:
        try:
          location = int(expression[3:])
          print_mem(location)
        except IndexError:
          print(f"MEM{expression[3:]} doesn't have a value.")
    elif expression == "CLEAR MEM":
      mem = [0.0] * 20
    else:
      split_expression = expression.split()
      n1 = split_expression[0]
      n2 = split_expression[2]

      new_n1 = None
      new_n2 = None
      new_expression = ""
      if "MEM" in n1 and "MEM" not in n2:
        location_n1 = int(n1[3:])
        new_n1 = mem[location_n1 - 1]
        new_expression = f"{str(new_n1)} {split_expression[1]} {str(n2)}"
      elif "MEM" in n2 and "MEM" not in n1:
        location_n2 = int(n2[3:])
        new_n2 = mem[location_n2 - 1]
        new_expression = f"{str(n1)} {split_expression[1]} {str(new_n2)}"
      elif "MEM" in n1 and "MEM" in n2:
        location_n1 = int(n1[3:])
        new_n1 = mem[location_n1 - 1]

        location_n2 = int(n2[3:])
        new_n2 = mem[location_n2 - 1]

        new_expression = f"{str(new_n1)} {split_expression[1]} {str(new_n2)}"

      new_expression = new_expression.replace("ANS", str(ans))
      ans = calculate(new_expression)
      print(ans)
  elif "ANS" in expression:
    if expression == "ANS":
      print(ans)
    else:
      expression = expression.replace("ANS", str(ans))
      ans = calculate(expression)
      print(ans)
  elif expression in ["QUIT", "EXIT"]:
    break
  else:
    ans = calculate(expression)
    print(ans)
