import sys
from functools import lru_cache

orbitee = {}

# @lru_cache(128)
def how_many_do_i_orbit(p):
  if p == 'COM': return 0
  return 1 + how_many_do_i_orbit(orbitee[p])

for line in sys.stdin:
  center, orbiter = line.strip().split(')')
  orbitee[orbiter] = center

print(sum(how_many_do_i_orbit(p) for p in orbitee))
