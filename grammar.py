# -*- coding: utf-8 -*-
from funcoes import *
import re

class Grammar:
    def __init__(self, rules):
        rules = tuple(rules)
        self.rules = tuple(self._parse(rule) for rule in rules)

    def _parse(self, rule):
        return tuple(rule.replace(' ', '').split('->'))

    @property
    def nonterminals(self):
        return set([nt for nt, _ in self.rules])

    @property
    def terminals(self):
        a = [
            expression
            for _, expression in self.rules
        ]
        
        nt = sorted([nt for nt, _ in self.rules], key=len, reverse=True)
        a = [i for j in [tr3(i, nt) for i in a] for i in j]

        for i in nt:
            for j in range(0, len(a)):
                if re.search(i, a[j]):
                    a[j] = a[j].replace(i, '')
                a[j] = " ".join(a[j].split())

        tmp = []
        for i in a:
            if i != '' and i not in tmp:
                tmp.append(i)
        a = tmp

        tmp = []
        for i in a:
            if len(i) > 1 and not i.isalpha():
                tmp2 = []
                tmp2.append(list(i))
                tmp2 = [i for j in tmp2 for i in j]
                for j in tmp2:
                    tmp.append(j)
            else:
                tmp.append(i)
        a = tmp

        tmp = []
        
        # a = [i for j in [list(i) for i in a] for i in j]
        return set(a)