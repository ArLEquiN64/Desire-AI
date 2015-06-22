import random
import math

class AI:
    def __init__(self):
        self.tick = 0
        self.status = {
            'hungriness': 50,
            'health': 50,
            'happiness': 50
        }
        self.beforeStatus = self.status;
        self.costEat = 0.5

    def __eat_diet(self):
        self.status['hungriness'] += 10

    def __eat_snack(self):
        self.status['hungriness'] += 2
        self.status['happiness'] += 10

    def drawStatus(self):
        print 'now status is ......'
        for param in self.status:
            print param.ljust(15, " ") + ":" + str(self.status[param]).rjust(4, " ")

    def dormcost(self, before, after):
        if before['health'] > after['health']:
            self.costEat += 0.05
        else:
            self.costEat -= 0.05

        if before['happiness'] < after['happiness']:
            self.costEat += 0.01
        else:
            self.costEat -= 0.01

    def routin(self):
        if random.random() < 0.5 :
            print 'hungry!'
            self.status['hungriness'] -= 5
        if random.random() < 0.5 :
            print 'unhappiness!'
            self.status['happiness'] -= 5
        pre = self.status
        if random.random() < self.costEat :
            print 'choice diet'
            self.__eat_diet()
        else :
            print 'choice snack'
            self.__eat_snack()
        self.drawStatus()
        self.status['health'] -= (math.fabs(50 - self.status['hungriness']) - 10) / 10
        self.dormcost(pre, self.status)

    # def start(self):
