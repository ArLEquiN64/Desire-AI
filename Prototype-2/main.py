#! /usr/bin/python2

import gp
import gridwar

class Main:
    def __init__(self):
        print "this is genom program."

if __name__ == "__main__":
    main = Main()
    '''
    rf = gp.getrankfunction(gp.buildhiddenset())
    gp.evolve(2, 500, rf, mutationrate = 0.2, breedingrate = 0.1,
            elite = 20, pnew = 0.1)
    '''
    t_winner = gp.evolve(5, 100, gridwar.tournament, maxgen = 100,
            mutationrate = 0.1, breedingrate = 0.3,
            elite = 10, pnew = 0.05)
    winner = gridwar.gridgame([t_winner, gridwar.humanplayer()])
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
