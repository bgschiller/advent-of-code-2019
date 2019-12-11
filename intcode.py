import sys
from dataclasses import dataclass
from typing import Callable
import types

def default_read():
  yield int(sys.stdin.readline())

def default_write(x):
  print(x)

class Program:
  def __init__(self, instructions, read=default_read, write=default_write):
    self.instructions = instructions[:]
    self.inst_ptr = 0
    self.read = read
    self.write = write

  @property
  def code(self):
    return int(str(self.instructions[self.inst_ptr])[-2:])

  @property
  def modes(self):
    return str(self.instructions[self.inst_ptr])[:-2][::-1]

  @property
  def op(self):
    for op in OPERATORS:
      if op.code == self.code:
        return op
    raise ValueError('Unrecognized instruction {}'.format(code))


  def is_immediate(self, ix):
    return (ix - 1) < len(self.modes) and self.modes[ix-1] == '1'

  def _get_address(self, ix):
    if not (1 <= ix <= self.op.num_args):
      raise IndexError('Operation {} has only {} prog, you asked for {}'.format(
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
    res = self.op.func(self)
    if isinstance(res, types.GeneratorType):
      for x in res:
        yield x
    else:
      yield res

  def __iter__(self):
    while self.instructions[self.inst_ptr] != 99:
      for _ in self.execute():
        yield

@dataclass
class Operator:
  code: int
  num_args: int
  func: Callable[[Program], int]

def add_and_store(prog: Program):
  prog[3] = prog[1] + prog[2]
  prog.inst_ptr += 4

def mul_and_store(prog: Program):
  prog[3] = prog[1] * prog[2]
  prog.inst_ptr += 4

def read(prog: Program):
  for val in prog.read():
    yield
  prog[1] = val
  prog.inst_ptr += 2

def write(prog: Program):
  prog.write(prog[1])
  prog.inst_ptr += 2

def jump_if_true(prog: Program):
  if prog[1] != 0:
    prog.inst_ptr =prog[2]
  else:
    prog.inst_ptr += 3

def jump_if_false(prog: Program):
  if prog[1] == 0:
    prog.inst_ptr = prog[2]
  else:
    prog.inst_ptr += 3

def less_than(prog: Program):
  prog[3] = 1 if prog[1] < prog[2] else 0
  prog.inst_ptr += 4

def equals(prog: Program):
  prog[3] = 1 if prog[1] == prog[2] else 0
  prog.inst_ptr += 4

class HaltProgram(StopIteration):
  pass

def halt(prog: Program):
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

if __name__ == '__main__':
  program = list(map(int, '3,225,1,225,6,6,1100,1,238,225,104,0,2,106,196,224,101,-1157,224,224,4,224,102,8,223,223,1001,224,7,224,1,224,223,223,1002,144,30,224,1001,224,-1710,224,4,224,1002,223,8,223,101,1,224,224,1,224,223,223,101,82,109,224,1001,224,-111,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1102,10,50,225,1102,48,24,224,1001,224,-1152,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,1102,44,89,225,1101,29,74,225,1101,13,59,225,1101,49,60,225,1101,89,71,224,1001,224,-160,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1101,27,57,225,102,23,114,224,1001,224,-1357,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,1001,192,49,224,1001,224,-121,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,1102,81,72,225,1102,12,13,225,1,80,118,224,1001,224,-110,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,7,677,226,224,102,2,223,223,1005,224,329,101,1,223,223,108,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,359,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,374,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,389,1001,223,1,223,107,677,226,224,1002,223,2,223,1005,224,404,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,419,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,434,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,107,226,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,479,1001,223,1,223,1008,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,7,677,677,224,102,2,223,223,1005,224,509,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,524,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,539,101,1,223,223,1108,677,677,224,102,2,223,223,1005,224,554,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,569,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,584,101,1,223,223,1107,226,226,224,102,2,223,223,1006,224,599,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,614,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,659,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,674,1001,223,1,223,4,223,99,226'.split(',')))
  for _ in Program(program):
    pass
