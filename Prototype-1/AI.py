class AI:
    def __init__(self):
        self.tick = 0
        self.status = {
            'hungriness': 10,
            'health': 10,
            'happiness': 10
        }

    def __eat_diet(self):
        self.status['hungriness'] += 10

    def __eat_snack(self):
        self.status['hungriness'] += 2
        self.status['happiness'] += 10

    def drawStatus(self):
        print 'now status is ......'
        for param in self.status:
            print param.ljust(15, " ") + ":" + str(self.status[param]).rjust(4, " ")

    # def dormcost(self):

    # def routin(self):

    # def start(self):
