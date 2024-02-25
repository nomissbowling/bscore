#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''bowling_score
type etc\scores.txt | python src/bowling_score.py
'''

from collections import deque
from itertools import islice

class Fr(object):
  def __init__(self, q):
    # n: num, p: pin, f: first, s: second, m: mark (0: no, 1: spare, 2: strike)
    self.q, self.n, self.p, self.f, self.s, self.m = q, -1, -1, -1, -1, 0

  def calc(self, f):
    p = self.f
    if p < 10:
      if self.s < 0: raise Exception("no throw second")
      p += self.s
    if self.m > 0:
      # if f + 1 < len(self.q): u = self.q[f + 1]
      # else: raise Exception("no throw after mark")
      try: u = self.q[f + 1]
      except (IndexError, ) as e: raise Exception("no throw after mark")
      p += u.f
      if self.m == 2:
        if u.f < 10:
          if u.s < 0: raise Exception("no throw second after x")
          p += u.s
        else:
          # if f + 2 < len(self.q): v = self.q[f + 2]
          # else: raise Exception("no throw after xx")
          try: v = self.q[f + 2]
          except (IndexError, ) as e: raise Exception("no throw after xx")
          p += v.f
    return p

  def c(self, f, p):
    if f < 9 and p == 2: return ''
    e = self.q[f + 1] if f + 1 < len(self.q) else Fr(self.q) # eleventh dummy
    t = self.q[f + 2] if f + 2 < len(self.q) else Fr(self.q) # twelfth dummy
    d = self.f if p == 0 else (
      self.s if self.f < 10 else self.f if f < 9 else e.f) if p == 1 else (
      -1 if self.m == 0 else e.f if self.m == 1 else e.s if e.f < 10 else t.f)
    if d == 0:
      if f == 9:
        if p == 1 and self.m == 2: return 'G'
        if p == 2 and self.m == 1: return 'G'
        if p == 2 and self.m == 2 and e.m == 2: return 'G'
      return 'G' if p == 0 else '-'
    if p == 2 and self.m > 0 and e.m == 1: return '/'
    if self.m == 1 and p == 1: return '/'
    if d == 10: return ' ' if f < 9 and p == 0 else 'x'
    if d < 0: return ''
    return f'{d}'

  def __repr__(self):
    return ''.join(self.c(self.n, p) for p in range(3))

  @staticmethod
  def new(q, p, d):
    if p[0] == 0:
      w = Fr(q)
      q.append(w)
      w.f, p[0] = d, 1 if d < 10 else 0
    elif p[0] == 1:
      w = q[-1]
      w.s, p[0] = d, 0
    if w.f == 10: w.m = 2
    elif w.f + w.s == 10: w.m = 1
    else: w.m = 0

def calc_score(q):
  # print(q)
  s = []
  for i, f in enumerate(q):
    t = '' if i == 9 else ' '
    f.n = i
    f.p = f.calc(i) + (q[i - 1].p if i > 0 else 0)
    s.append(f'{t}{f}')
    if i == 9: break
  print(' '.join(s))
  # print(' '.join(f'{q[i].p:3d}' for i in range(10)))
  print(' '.join(f'{f.p:3d}' for f in islice(q, 0, 10)))

def bscore(txt, mode):
  # mode: False (normal), True (shift score when extra frames)
  q = deque()
  p = [0]
  for c in txt:
    if ord('0') <= ord(c) <= ord('9'): Fr.new(q, p, ord(c) - ord('0'))
    if c == '-' or c == 'G' or c == 'F': Fr.new(q, p, 0)
    if c == '/':
      if p[0] == 0: raise('first / is not allowed')
      else: Fr.new(q, p, 10 - q[-1].f)
    if c == 'x' or c == 'X':
      if p[0] == 1: raise('second x is not allowed')
      else: Fr.new(q, p, 10)
  while True:
    try: q[9].calc(9)
    except (IndexError, Exception, ) as e: break
    calc_score(q)
    if not mode: break
    try: q.popleft()
    except (IndexError, Exception, ) as e: break

def bowling_score(mode, fn=0):
  with open(fn, 'r') as f: # b'...\n' when 'rb'
    while True:
      r = f.readline()
      if not r: break
      l = r.rstrip()
      if not len(l): continue # empty line
      # print(l) # '...\n'
      i = l.find('#')
      if i == 0: continue # comment line
      elif i < 0: bscore(l, mode) # line
      else: bscore(l[:i], mode) # cut comment

if __name__ == '__main__':
  bowling_score(False)
