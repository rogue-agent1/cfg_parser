#!/usr/bin/env python3
"""Context-free grammar parser — CYK algorithm."""
import sys
from collections import defaultdict

class CFG:
    def __init__(self):
        self.rules = defaultdict(list); self.start = None
    def add(self, lhs, *rhs):
        if self.start is None: self.start = lhs
        self.rules[lhs].append(list(rhs))
    def cyk(self, tokens):
        n = len(tokens)
        table = [[set() for _ in range(n)] for _ in range(n)]
        # Fill diagonal
        for i, t in enumerate(tokens):
            for lhs, prods in self.rules.items():
                for prod in prods:
                    if len(prod) == 1 and prod[0] == t:
                        table[i][i].add(lhs)
        # Fill upper triangle
        for span in range(2, n+1):
            for i in range(n-span+1):
                j = i + span - 1
                for k in range(i, j):
                    for lhs, prods in self.rules.items():
                        for prod in prods:
                            if len(prod) == 2 and prod[0] in table[i][k] and prod[1] in table[k+1][j]:
                                table[i][j].add(lhs)
        return self.start in table[0][n-1]

if __name__ == "__main__":
    g = CFG()
    g.add('S', 'NP', 'VP'); g.add('NP', 'Det', 'N'); g.add('NP', 'N')
    g.add('VP', 'V', 'NP'); g.add('VP', 'V')
    g.add('Det', 'the'); g.add('Det', 'a')
    g.add('N', 'dog'); g.add('N', 'cat'); g.add('N', 'fish')
    g.add('V', 'sees'); g.add('V', 'eats'); g.add('V', 'runs')
    tests = [["the","dog","sees","a","cat"], ["dog","runs"], ["the","sees","cat"], ["a","fish","eats","the","dog"]]
    print("CFG Parser (CYK):")
    for t in tests:
        result = g.cyk(t)
        print(f"  {' '.join(t):>30s}: {'✅ valid' if result else '❌ invalid'}")
