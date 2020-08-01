import sqlite3
from cards import deck, stringcode_card


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

    def showAll(self):
        """
        Show all data
        """
        query = "SELECT * FROM hands"
        return self.query(query)


    def showProbablity(self, hand):
        """
        Show probability of a certain hand
        """
        if self.checkCard(hand) != True:
            print('No Record')
            pass

        cards = self.convertTupleToStringCode(hand)
        
        pull = f'SELECT probability FROM hands WHERE cards = "{cards}"'
        return self.query(pull)

    
       
    def loadEmptyRecord(self,primary_key_list, value_strings_list, primary_key_name = 'cards'):
        """
        Add new record to database. First checking to see if there is an existing record. Then run a INSERT INTO command if the record does not exist. 
        """
        for i, key in enumerate(primary_key_list):
                # creating SQL query to check if the record exists
                query  = f'select count(*) from hands where {primary_key_name} ="{key}"' 
                if self.query(query)[0][0] == 0:
                    #creating SQL query to insert new record
                    query = f'INSERT INTO hands VALUES ("{key}", {value_strings_list})'
                    self.query(query)
        pass

    def checkCard(self, hand):
        """
        Check database for hand
        Input: hand, list of card tuples
        Output: Boolean, true if there is a record. 
        """
        
        cards = self.convertTupleToStringCode(hand)
        query = f'select count(*) from hands where cards ="{cards}"'
        return self.query(query)[0][0] != 0

   
        
    def convertTupleToStringCode(self, hand):
        """
        Converting list of card tuples to string code representing a hand
        """
        hand =sorted(hand)
        cards = [deck[card]['picture'] for card in hand]
        return ' '.join(cards)

    def convertStringCodeToTuple(self,stringcode):
        """
        Convert string code to a list of card tuples.
        """
        
        cards = stringcode.split(' ')
        cards = [stringcode_card[code] for code in cards]
        return cards

    def insertHandScenario(self, hand, prob10):
        """
        Upload hand with probability, hand is a list of 7 tuples representing individual cards.
        """
        hand =sorted(hand)
        if self.checkCard(hand):
            pass

        cards = self.convertTupleToStringCode(hand)
        query = f'INSERT INTO hands VALUES ("{cards}", {prob10})'
        self.query(query)
        pass

    def updateHandScenario(self, hand, prob10):
        """
        Upload hand with probability to an existing record, hand is a list of 7 tuples representing individual cards.
        """
        hand =sorted(hand)
        if self.checkCard(hand):
            cards = self.convertTupleToStringCode(hand)
            query =    f"""
                        UPDATE hands
                        SET cards = {cards}, prob10 = {prob10}
                        WHERE cards = {cards}; 
                        """ 
            
            self.query(query)
            pass



#    


        
        
