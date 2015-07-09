#! /usr/bin/python2

import gp

class Main:
    def __init__(self):
        print "this is genom program."

if __name__ == "__main__":
    main = Main()
    '''
    rf = gp.getrankfunction(gp.buildhiddenset())
    gp.evolve(2, 500, rf, mutationrate = 0.2, breedingrate = 0.1,
            pexp = 0.7, pnew = 0.1)
    '''
    t_winner = gp.evolve(5, 100, gp.tournament, maxgen = 200,
            mutationrate = 0.1, breedingrate = 0.3,
            pexp = 0.2, pnew = 0.05)
    winner = gp.gridgame([t_winner, gp.humanplayer()])
    if winner == 0:
        print 'You lose.'
    elif winner == 1:
        print 'You win!'
    else:
        print 'Draw'
