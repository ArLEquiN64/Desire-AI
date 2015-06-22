#! /usr/bin/python2
from AI import AI
import random

class Main:
    def __init__(self):
        self.ai = AI()
        self.ai.drawStatus()

if __name__ == "__main__":
    main = Main()
    for value in range(1000):
        main.ai.routin()
