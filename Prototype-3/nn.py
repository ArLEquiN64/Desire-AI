from math import tanh
from sqlite3 import dbapi2 as sqlite

def dtanh(y):
    return 1.0 - y * y

class searchnet:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def maketables(self):
        self.con.execute('create table hiddennode(create_key)')
        self.con.execute('create table inhidden(fromid, toid, strength)')
        self.con.execute('create table hiddenout(fromid, toid, strength)')
        self.con.commit()

    def getstrength(self, fromid, toid, layer):
        if layer == 0:
            table = 'inhidden'
        else:
            table = 'hiddenout'
        res = self.con.execute(
                'select strength from %s where fromid = %d and toid = %d'
                % (table, fromid, toid)).fetchone()
        if res == None:
            if layer == 0:
                return -0.2
            if layer == 1:
                return 0
        return res[0]

    def setstrength(self, fromid, toid, layer, strength):
        if layer == 0:
            table = 'inhidden'
        else:
            table = 'hiddenout'
        res = self.con.execute(
                'select rowid from %s where fromid = %d and toid = %d'
                % (table, fromid, toid)).fetchone()
        if res == None:
            self.con.execute(
                    'insert into %s (fromid, toid, strength) values (%d, %d, %f)'
                    % (table, fromid, toid, strength))
        else:
            rowid = res[0]
            self.con.execute(
                    'update %s set strength = %f where rowid = %d'
                    % (table, strength, rowid))

    def generatehiddennode(self, inputids, outputids):
        if len(inputids) > 3:
            return None
        createkey = '_'.join(sorted([str(ii) for ii in inputids]))
        res = self.con.execute(
                "select rowid from hiddennode where create_key = '%s'"
                % createkey).fetchone()

        if res == None:
            cur = self.con.execute(
                    "insert into hiddennode (create_key) values ('%s')"
                    % createkey)
            hiddenid = cur.lastrowid
            for inputid in inputids:
                self.setstrength(inputid, hiddenid, 0, 1.0 / len(inputids))
            for outputid in outputids:
                self.setstrength(hiddenid, outputid, 1, 0.1)
            self.con.commit()
    
    def getallhiddenids(self, inputids, outputids):
        l1 = {}
        for inputid in inputids:
            cur = self.con.execute(
                    'select toid from inhidden where fromid = %d'
                    % inputid)
            for row in cur:
                l1[row[0]] = 1
        for outputid in outputids:
            cur = self.con.execute(
                    'select fromid from hiddenout where toid = %d'
                    % outputid)
            for row in cur:
                l1[row[0]] = 1
        return l1.keys()

    def setupnetwork(self, inputids, outputids):
        self.inputids = inputids
        self.hiddenids = self.getallhiddenids(inputids, outputids)
        self.outputids = outputids

        self.ai = [1.0] * len(self.inputids)
        self.ah = [1.0] * len(self.hiddenids)
        self.ao = [1.0] * len(self.outputids)
        
        self.wi = [[self.getstrength(inputid, hiddenid, 0)
            for hiddenid in self.hiddenids]
            for inputid in self.inputids]
        self.wo = [[self.getstrength(hiddenid, outputid, 1)
            for outputid in self.outputids]
            for hiddenid in self.hiddenids]

    def feedforward(self):
        for i in range(len(self.inputids)):
            self.ai[i] = 1.0

        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.inputids)):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = tanh(sum)

        for k in range(len(self.outputids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)
        return self.ao[:]

    def getresult(self, inputids, outputids):
        self.setupnetwork(inputids, outputids)
        return self.feedforward()

    def backpropagate(self, targets, N = 0.5):
        outputdeltas = [0.0] * len(self.outputids)
        for k in range(len(self.outputids)):
            error = targets[k] - self.ao[k]
            outputdeltas[k] = dtanh(self.ao[k]) * error
        
        hiddendeltas = [0.0] * len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.outputids)):
                error += outputdeltas[k] * self.wo[j][k]
            hiddendeltas[j] = dtanh(self.ah[j]) * error
        
        for j in range(len(self.hiddenids)):
            for k in range(len(self.outputids)):
                change = outputdeltas[k] * self.ah[j]
                self.wo[j][k] += N * change

        for i in range(len(self.inputids)):
            for j in range(len(self.hiddenids)):
                change = hiddendeltas[j] * self.ai[i]
                self.wi[i][j] += N * change

    def trainquery(self, inputids, outputids, selectedoutput):
        self.generatehiddennode(inputids, outputids)
        self.setupnetwork(inputids, outputids)
        self.feedforward()
        targets = [0.0] * len(outputids)
        targets[outputids.index(selectedoutput)] = 1.0
        error = self.backpropagate(targets)
        self.updatedatabase()

    def updatedatabase(self):
        for i in range(len(self.inputids)):
            for j in range(len(self.hiddenids)):
                self.setstrength(self.inputids[i], self.hiddenids[j],
                        0, self.wi[i][j])
        for j in range(len(self.hiddenids)):
            for k in range(len(self.outputids)):
                self.setstrength(self.hiddenids[j], self.outputids[k],
                        1, self.wo[j][k])
        self.con.commit()
