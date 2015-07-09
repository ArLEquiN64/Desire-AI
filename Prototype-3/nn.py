from math import tanh
from sqlite3 import dbapi2 as sqlite

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
                'select strength from %s where formid = %d and toid = %d'
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
                    'insert into %s (fromid, toid, strength) values (?, ?, ?'
                    % (table, fromid, toid, strength))
        else:
            rowid = res[0]
            self.con.execute(
                    'update %s set strength = %f where rowid = %d'
                    % (table, strength, rowid))

    def generatehiddennode(self, inputs, outputs):
        if len(inputs) > 3:
            return None
        createkey = '_'.join(sorted([str(it) for it in inputs]))
        res = self.con.execute(
                "select rowid from hiddennode where create_key = '%s'"
                % createkey).fetchone()

        if res == None:
            cur = self.con.execute(
                    "insert into hiddennode (create_key) values ('%s')"
                    % createkey)
            hiddenid = cur.lastrowid
            for ip in inputs:
                self.setstrength(ip, hiddenid, 0, 1.0 / len(inputs))
            for op in outputs:
                self.setstrength(hiddenid, op, 1, 0.1)
            self.con.commit()
