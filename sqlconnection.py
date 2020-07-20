import sqlite3
from texas import TexasHoldThem


class DBManager():

    def __init__ (self, dbName = 'sqlite3 texas_holdem.db'):
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
        # for col in columns:
        #     print(col)
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

        cards = str(sorted(hand))
        
        pull = f'SELECT probability FROM hands WHERE cards = "{cards}"'
        
        print(pull)
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
        
    def loadEmptyRecord(self,primary_key_list, value_strings_list, primary_key_name = 'cards'):
        """
        Add new record to database. First checking to see if there is an existing record. Then run a INSERT INTO command if the record does not exist. 
        """
        for i, key in enumerate(primary_key_list):
                # creating SQL query to check if the record exists
                query  = f'select count(*) from hands where {primary_key_name} ="{key}"' 
                if conn.query(query)[0][0] == 0:
                    #creating SQL query to insert new record
                    query = f'INSERT INTO hands VALUES ("{key}", {value_strings_list})'
                    conn.query(query)
        pass
    
        



        
        
