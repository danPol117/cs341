#!/usr/bin/env python3
"""
pda_parser.py

Recursive-descent PDA parser with embedded PDA transition logging:
  - Users may enter a number of strings or a file path containing one string per line.
  - All output is printed to the console and logged to pda_output.txt, including line numbers of accept/reject messages.

Usage:
  $ python3 pda_parser.py
  Enter number of strings or file path: [n | path]
"""
import sys
from pathlib import Path

# Terminal set Σ
SIGMA = set(".0123456789+-*/()ab")

# PDA δ transitions: (state, input_symbol, stack_top) -> [(next_state, push_list), ...]
TRANS = {
    ('q0', None, None):       [('q1', ['S'])],
    ('q1', None, 'S'):        [('q2', ['a','T','a'])],
    ('q2', None, 'T'):        [('q2', ['b','T','b']), ('q3', ['a','C','a'])],
    ('q3', None, 'C'):        [
        ('q3', ['C','+','C']), ('q3', ['C','-','C']),
        ('q3', ['C','*','C']), ('q3', ['C','/','C']),
        ('q3', ['(', 'C', ')']), ('q4', ['H'])
    ],
    ('q4', None, 'H'):        [('q5', ['Y','.','Y']), ('q5', ['Y','.']), ('q5', ['.','Y'])],
    ('q5', None, 'Y'):        [('q6', ['N','Y']), ('q6', ['N'])],
    ('q6', None, 'N'):        [( 'q6', [str(d)]) for d in range(10)]
}
VT = SIGMA

# Globals for logging
line_no = 0
msg_lines = []  # record line numbers of accept/reject messages

class PDARecorder:
    """Maintains PDA state, stack, and logs transitions."""
    def __init__(self):
        self.state = 'q0'
        self.stack = []
        self.path = []  # list of (state, inp, top, pop, push, next_state)

    def apply_epsilon(self, push_list):
        pre = self.state
        top = self.stack[-1] if self.stack else None
        pop = self.stack.pop() if self.stack else None
        for sym in push_list:
            self.stack.append(sym)
        for ns, pl in TRANS.get((pre, None, top), []):
            if pl == push_list:
                self.state = ns
                break
        self.path.append((pre, 'epsilon', top or 'epsilon', pop or 'epsilon', ''.join(push_list) or 'epsilon', self.state))

    def apply_match(self, sym):
        pre = self.state
        top = self.stack[-1] if self.stack else None
        pop = self.stack.pop() if self.stack else None
        self.path.append((pre, sym, top or 'epsilon', pop or 'epsilon', 'epsilon', pre))


def parse_string(s):
    rec = PDARecorder()
    parser = Parser(s, rec)
    ok = parser.parse_S()
    return ok, rec.path

class Parser:
    def __init__(self, s, rec):
        self.s = s
        self.i = 0
        self.rec = rec
    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else None
    def match(self, c):
        if self.peek() == c:
            self.rec.apply_match(c)
            self.i += 1
            return True
        return False
    def parse_S(self):
        self.rec.apply_epsilon(['S'])
        self.rec.apply_epsilon(['a','T','a'])
        if not self.match('a'): return False
        if not self.parse_T(): return False
        if not self.match('a'): return False
        return self.i == len(self.s)
    def parse_T(self):
        if self.peek() == 'b':
            self.rec.apply_epsilon(['b','T','b'])
            if not self.match('b'): return False
            if not self.parse_T(): return False
            if not self.match('b'): return False
            return True
        if self.peek() == 'a':
            self.rec.apply_epsilon(['a','C','a'])
            if not self.match('a'): return False
            if not self.parse_C(): return False
            if not self.match('a'): return False
            return True
        return False
    def parse_C(self):
        if self.peek() == '(':
            self.rec.apply_epsilon(['(', 'C', ')'])
            if not self.match('('): return False
            if not self.parse_C(): return False
            if not self.match(')'): return False
        else:
            self.rec.apply_epsilon(['H'])
            if not self.parse_H(): return False
        while self.peek() in '+-*/':
            op = self.peek()
            self.rec.apply_epsilon(['C', op, 'C'])
            if not self.match(op): return False
            if self.peek() == '(':
                self.rec.apply_epsilon(['(', 'C', ')'])
                if not self.match('('): return False
                if not self.parse_C(): return False
                if not self.match(')'): return False
            else:
                if not self.parse_H(): return False
        return True
    def parse_H(self):
        if self.peek() and self.peek().isdigit():
            self.rec.apply_epsilon(['Y','.','Y'])
            if not self.parse_Y(): return False
            if not self.match('.'): return False
            if self.peek() and self.peek().isdigit():
                if not self.parse_Y(): return False
            return True
        if self.peek() == '.':
            self.rec.apply_epsilon(['.','Y'])
            if not self.match('.'): return False
            if not self.parse_Y(): return False
            return True
        return False
    def parse_Y(self):
        if self.peek() and self.peek().isdigit():
            self.rec.apply_epsilon(['N','Y'])
            if not self.parse_N(): return False
            while self.peek() and self.peek().isdigit():
                self.rec.apply_epsilon(['N'])
                if not self.parse_N(): return False
            return True
        return False
    def parse_N(self):
        if self.peek() and self.peek().isdigit():
            self.rec.apply_epsilon([self.peek()])
            if not self.match(self.peek()): return False
            return True
        return False

# Main
if __name__ == '__main__':
    logf = open('pda_output.txt', 'w')
    def log(msg):
        global line_no, msg_lines
        line_no += 1
        print(msg)
        logf.write(msg + '\n')
        if msg.startswith("String '") and (msg.endswith(" is accepted.") or msg.endswith(" is rejected.")):
            msg_lines.append(line_no)

    inp = input("Enter number of strings or file path: ").strip()
    # determine mode
    if inp.isdigit():
        n = int(inp)
        strings = [input(f"Enter string {i+1} of {n}\n").strip() for i in range(n)]
    else:
        path = Path(inp)
        if not path.is_file():
            log(f"Invalid file path: {inp}")
            sys.exit(1)
        lines = path.read_text().splitlines()
        n = len(lines)
        strings = [line.strip() for line in lines]

    log(str(n))
    if n == 0:
        sys.exit(0)

    for idx, s in enumerate(strings, 1):
        log(f"Testing: {s}")
        if any(ch not in SIGMA for ch in s):
            log("Entered string contains invalid input bits")
            continue
        ok, path = parse_string(s)
        if ok:
            for st, inp_sym, top, pop, push, nxt in path:
                log("-----------------------------------------------------------")
                log(f"Present State: {st}")
                log(f"Current input symbol under R-head: {inp_sym}")
                log(f"Stack Top: {top}")
                log(f"Symbol popped from Stack: {pop}")
                log(f"Symbols pushed onto Stack: {push}")
                log(f"Next state: {nxt}")
            log("-----------------------------------------------------------")
            log(f"String '{s}' is accepted.")
        else:
            log(f"String '{s}' is rejected.")

    # Summary of accept/reject line numbers
    log('')
    log(f"Acceptance/Rejection messages at lines: {', '.join(map(str,msg_lines))}")
    logf.close()
