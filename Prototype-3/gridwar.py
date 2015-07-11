from random import randint

def gridgame(p):
    max = (3, 3)
    lastmove = [-1, -1]
    location = [[randint(0, max[0]), randint(0, max[1])]]
    location.append([(location[0][0] + 2) % 4, (location[0][1] + 2) % 4])

    for o in range(50):
        for i in range(2):
            locs = location[i][:] + location[1 - i][:]
            locs.append(lastmove[i])

            '''
            print '%d-%d' % (o, i)
            for j in range(max[0] + 1):
                for k in range(max[1] + 1):
                    if (j, k) == (location[0][0], location[0][1]):
                        print '0',
                    elif (j, k) == (location[1][0], location[1][1]):
                        print '1',
                    else:
                        print '-',
                print
            '''

            move = p[i].evaluate(locs) % 4
            if lastmove[i] == move:
                return 1 - i
            lastmove[i] = move
            if move == 0:
                location[i][0] -= 1
                if location[i][0] < 0:
                    location[i][0] = 0
            if move == 1:
                location[i][0] += 1
                if location[i][0] > max[0]:
                    location[i][0] = max[0]
            if move == 2:
                location[i][1] -= 1
                if location[i][1] < 0:
                    location[i][1] = 0
            if move == 3:
                location[i][1] += 1
                if location[i][1] > max[1]:
                    location[i][1] = max[1]

            if location[i] == location[1 - i]:
                return i + 2
    return -1

def tournament(pl):
    losses = [0 for p in pl]

    for i in range(len(pl)):
        for j in range(len(pl)):
            if i == j:
                continue
            winner = gridgame([pl[i], pl[j]])
            if winner == 0:
                losses[j] += 2
            elif winner == 1:
                losses[i] += 2
            elif winner == 2:
                losses[j] += 2
                losses[i] -= 1
            elif winner == 3:
                losses[i] += 2
                losses[j] -= 1
            elif winner == -1:
                losses[i] += 1
                losses[j] += 1
                pass
    '''
    for i in range(len(pl)):
        winner = gridgame([pl[i], humanplayer()])
        if winner == 1:
            losses[i] += 2
        elif winner == -1:
            losses[i] += 1
            pass
    '''

    z = zip(losses, pl)
    z.sort()
    return z

class humanplayer:
    def evaluate(self, board):
        me = tuple(board[0:2])
        others = [tuple(board[x:x + 2])
                for x in range(2, len(board) - 1, 2)]

        for i in range(4):
            for j in range(4):
                if (i, j) == me:
                    print 'o',
                elif (i, j) in others:
                    print 'X',
                else:
                    print '-',
            print
        print 'Your last move is %d.' % board[len(board) - 1]
        print ' 0'
        print '2 3  please enter your next move.'
        print ' 1'
        
        move = int(raw_input())
        return move
