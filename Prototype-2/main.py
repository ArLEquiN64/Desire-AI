#! /usr/bin/python2

import gp

class Main:
    def __init__(self):
        print "this is genom program."

if __name__ == "__main__":
    main = Main()
    random1 = gp.makerandomtree(2)
    random1.display()
    hiddenset = gp.buildhiddenset()
    print gp.scorefunction(random1,hiddenset)
