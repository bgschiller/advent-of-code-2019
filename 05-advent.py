import sys
from dataclasses import dataclass
from typing import Callable

class Args:
  def __init__(self, instructions, inst_ptr):
    code = int(str(instructions[inst_ptr])[-2:])
    self.instructions = instructions
    self.inst_ptr = inst_ptr
    self.modes = str(instructions[inst_ptr])[:-2][::-1]
    for op in OPERATORS:
      if op.code == code:
        self.op = op
        break
    else:
      raise ValueError('Unrecognized instruction {}'.format(code))

  def is_immediate(self, ix):
    return (ix - 1) < len(self.modes) and self.modes[ix-1] == '1'

  def _get_address(self, ix):
    if not (1 <= ix <= self.op.num_args):
      raise IndexError('Operation {} has only {} args, you asked for {}'.format(
        self.op.code, self.op.num_args, ix))
    return self.instructions[self.inst_ptr + ix]

  def __getitem__(self, ix):
    address = self._get_address(ix)
    if self.is_immediate(ix):
      return address
    return self.instructions[address]

  def __setitem__(self, ix, val):
    address = self._get_address(ix)
    self.instructions[address] = val

  def execute(self):
    return self.op.func(self)

@dataclass
class Operator:
  code: int
  num_args: int
  func: Callable[[Args], int]

def add_and_store(args: Args):
  args[3] = args[1] + args[2]
  return args.inst_ptr + 4

def mul_and_store(args: Args):
  args[3] = args[1] * args[2]
  return args.inst_ptr + 4

def read(args: Args):
  args[1] = int(sys.stdin.readline())
  return args.inst_ptr + 2

def write(args: Args):
  print(args[1], flush=True)
  return args.inst_ptr + 2

def jump_if_true(args: Args):
  if args[1] != 0:
    return args[2]
  return args.inst_ptr + 3

def jump_if_false(args: Args):
  if args[1] == 0:
    return args[2]
  return args.inst_ptr + 3

def less_than(args: Args):
  args[3] = 1 if args[1] < args[2] else 0
  return args.inst_ptr + 4

def equals(args: Args):
  args[3] = 1 if args[1] == args[2] else 0
  return args.inst_ptr + 4

class HaltProgram(StopIteration):
  pass

def halt(args: Args):
  raise HaltProgram()

OPERATORS = [
  Operator(func=add_and_store, code=1, num_args=3),
  Operator(func=mul_and_store, code=2, num_args=3),
  Operator(func=read, code=3, num_args=1),
  Operator(func=write, code=4, num_args=1),
  Operator(func=halt, code=99, num_args=0),
  Operator(func=jump_if_true, code=5, num_args=2),
  Operator(func=jump_if_false, code=6, num_args=2),
  Operator(func=less_than, code=7, num_args=3),
  Operator(func=equals, code=8, num_args=3),
]


instructions = [int(x) for x in '''3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'''.replace('\n', '').split(',')]
inst_ptr = 0

while instructions[inst_ptr] != 99:
  args = Args(instructions, inst_ptr)
  inst_ptr = args.execute()
