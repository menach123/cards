import sqlite3
from texas import TexasHoldThem


class DBManager():

    def __init__ (self, dbName):
        self.dbName = dbName
        pass

    def query(self, sql):
        """
        Enter SQL Query
        """
        con = sqlite3.connect(self.dbName)
        with con:
            cur = con.cursor()
            cur.execute(sql)
            res = cur.fetchall()
        if con:
            con.close()

        return res



    def showColumnName(self):
        """
        Show column names
        """
        query = "PRAGMA table_info(hands);"
        columns =  [tuple_[1] for tuple_ in self.query(query)]         
        for col in columns:
            print(col)
        return columns

    def insertHandScenario(self, hand, show = False, close = True):
        """
        Upload hand with probability, hand is a list of 7 tuples representing individual cards.
        """
        new_cards = [card for card in hand if card != None]
        game = TexasHoldThem(10)
        probability = sum([game.win_loss(new_cards) for i in range(10000)])/ 10000
        query = self.convertHandToColumn(hand)
        input_query = query + [probability]
        input_query = str(input_query)[1:-1].replace('None', "NULL")
        insert_query = f"INSERT INTO hands VALUES ({input_query});"
        
        self.query(insert_query)
        
        if show:
            return self.showProbablity(hand, just_probabilty= False)




        pass

    def showAll(self):
        query = "SELECT * FROM hands"
        return self.query(query)


    def showProbablity(self, hand, just_probabilty = True):

        query = self.convertHandToColumns(hand)
        
        columns = conn.showColumnName()

        pull = 'SELECT win_probabilty FROM hands WHERE ' if just_probabilty else 'SELECT * FROM hands WHERE '
        for i, j in zip(columns, query):
            if j == None:
                pull += f" {i} is NULL AND"
            else:
                pull += f" {i} = {j} AND"
            
        pull= pull[:-4]

        return self.query(pull)




    def convertHandToColumns(self, hand):
        """
        Taking list of 7 tuples represent card and converting it to column of alternating suits names
        """
        query = []
        for i in hand:
            if i == None:
                query.append(None)
                query.append(None)
            else:
                query.append(i[0])
                query.append(i[1])
        return query
        
    
        



        
        
