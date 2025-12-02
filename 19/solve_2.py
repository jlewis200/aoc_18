#!/usr/bin/env python3
"""
The program finds the sum of all factors of the provided constant.  The main
work for part 2 is reversing the program to determine the algorithm so it can
be rewritten in a more efficient manner.  See 'program_re.odg' for control
flow graph and details.
"""

constant = 10551428
total = 0

for idx in range(1, 1 + constant):
    if constant % idx == 0:
        total += idx

print(total)
