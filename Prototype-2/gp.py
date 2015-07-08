from random import random, randint, choice
from copy import deepcopy
from math import log

class fwrapper:
    def __init__(self, function, childcount, name):
        self.function = function
        self. childcount = childcount
        self.name = name

class node:
    def __init__(self, fw, children):
        self.function = fw.function
        self.name = fw.name
        self.children = children

    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self, indent = 0):
        print ('  ' * indent) + self.name
        for c in self.children:
            c.display(indent + 1)

class paramnode:
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, inp):
        return inp[self.idx]

    def display(self, indent = 0):
        print '%sp%d' % ('  ' * indent, self.idx)

class constnode:
    def __init__(self, v):
        self.v = v

    def evaluate(self, inp):
        return self.v

    def display(self, indent = 0):
        print '%s%d' % ('  ' * indent, self.v)

# functions to give node

addw = fwrapper(lambda l: l[0] + l[1], 2, 'add')
subw = fwrapper(lambda l: l[0] - l[1], 2, 'substract')
mulw = fwrapper(lambda l: l[0] * l[1], 2, 'multiply')

def iffunc(l):
    if l[0] > 0:
        return l[1]
    else:
        return l[2]

ifw = fwrapper(iffunc, 3, 'if')

def isgrater(l):
    if l[0] > l[1]:
        return 1
    else:
        return 0

gtw = fwrapper(isgrater, 2, 'isgrater')

flist = [addw, subw, mulw, ifw, gtw]

# tree

def exampletree():
    return node(ifw, [
            node(gtw, [paramnode(0), constnode(3)]),
            node(addw, [paramnode(1), constnode(5)]),
            node(subw, [paramnode(1), constnode(2)]),
            ]
        )

# make random tree
def makerandomtree(pc, maxdepth = 4, fpr = 0.5, ppr = 0.6):
    if random() < fpr and maxdepth > 0:
        f = choice(flist)
        children = [makerandomtree(pc, maxdepth - 1, fpr, ppr)
                for i in range(f.childcount)]
        return node(f, children)

    elif random() < ppr:
        return paramnode(randint(0, pc - 1))

    else:
        return constnode(randint(0, 10))
