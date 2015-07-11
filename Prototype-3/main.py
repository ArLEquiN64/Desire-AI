#! /usr/bin/python

import nn
import gridwar
from random import randint

class Main:
    def __init__(self):
        self.net = nn.searchnet('gridwar.db')
        # self.net.maketables()
        self.oUP = 0
        self.oDown = 1
        self.oLeft = 2
        self.oRight = 3
        self.outputs = [self.oUP, self.oDown, self.oLeft, self.oRight]

    def train_ai(self):
        self.ai = trainai(self)
        return gridwar.gridgame([self.ai, gridwar.humanplayer()])

    def vs_ai(self):
        self.ai = vsai(self)
        return gridwar.gridgame([self.ai, gridwar.humanplayer()])

class trainai:
    def __init__(self, main):
        self.main = main

    def evaluate(self, board):
        me = tuple(board[0:2])
        others = [tuple(board[x:x + 2])
                for x in range(2, len(board) - 1, 2)]
        for i in range(4):
            for j in range(4):
                if (i, j) == me:
                    print 'a',
                elif (i, j) in others:
                    print 'X',
                else: print '-',
            print
        ans = self.main.net.getresult(
                [me[0], me[1], i, j, board[len(board) - 1]],
                self.main.outputs)
        print ' 0   train ai Your last move is %d' % board[len(board) - 1]
        print '2 3  please input next move'
        print ' 1   now ai answer is ',
        print ans
        move = int(raw_input())
        for i in range(4):
            for j in range(4):
                if (i, j) in others:
                    self.main.net.trainquery(
                            [me[0], me[1], i, j, board[len(board) - 1]],
                            self.main.outputs, move)
        return move

class vsai:
    def __init__(self, main):
        self.main = main

    def evaluate(self, board):
        me = tuple(board[0:2])
        others = [tuple(board[x:x + 2])
                for x in range(2, len(board) - 1, 2)]
        for i in range(4):
            for j in range(4):
                if (i, j) in others:
                    move = self.main.net.getresult(
                            [me[0], me[1], i, j, board[len(board) - 1]],
                            self.main.outputs)
        return move.index(max(move))

if __name__ == "__main__":
    main = Main()
    winner =  main.train_ai()
    if winner == 0:
        print 'You lose.'
    elif winner == 1:
        print 'You win!'
    elif winner == 2:
        print 'KO! You lose.'
    elif winner == 3:
        print 'KO! You win!'
    else:
        print 'Draw'
