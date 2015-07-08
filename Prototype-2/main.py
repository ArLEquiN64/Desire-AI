#! /usr/bin/python2

import gp

class Main:
    def __init__(self):
        print "this is genom program."

if __name__ == "__main__":
    main = Main()
    rf = gp.getrankfunction(gp.buildhiddenset())
    gp.evolve(2, 500, rf, mutationrate = 0.2, breedingrate = 0.1,
            pexp = 0.7, pnew = 0.1)
