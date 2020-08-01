import numpy as np
import itertools
from cards import Game, deck, Player, stringcode_card
from sqlconnection import DBManager




class TexasHoldThem(Game):
    
    def setMaxes(self, common_max =5, hand_size = 2):
        """
        Texas Hold Them rules. 
        """
        
        self.connection = DBManager()
        self.max_common_pile = common_max
        self.max_hand_size = hand_size
        self.really_hand = 5
        self.common_combinations= None

    def fillCommonCards(self):
        """
        Filling the commons that are not filled
        """
        check = self.fillPile(self.common, self.max_common_pile)
        
        # generating all 3 hand combinations
        self.common_combinations = [list(i) for i in itertools.combinations(self.common, 3)]
        self.common_combinations = [sorted(hand) for hand in self.common_combinations]
        


    def fill(self):
        """

        """
        self.fillCommonCards()
        
        for i in range(len(self.player_list)):
            self.player_list[i].cards = self.fillPile(self.player_list[i].cards, self.max_hand_size)
            
            self.player_list[i].hands = [self.player_list[i].cards + combo for combo in self.common_combinations]
            
        pass

    def win_loss(self, player1_common_cards):
        """
        Input: list of card tuples. The first 2 is player 1, and the next 5 are the common cards. There are will be 0, 3, 4, and 5  common card inputed.   
        """
        
        for i, card in enumerate(player1_common_cards):
            
            if i < 2:
                self.setPlayerOneCard(0 ,card[0], card[1])
            else: 
                self.setCommonPileCard(card[0], card[1])
            
        self.fill()
        self.assignRank()
        rank = [player.rank for player in self.player_list]
        return self.player_list[0].rank == max(rank)


    def addPlayerAndCommon(self, player1_common_cards):
        """
        """
        
        for i, card in enumerate(player1_common_cards):
            
            if i < 2:
                self.setPlayerOneCard(0 ,card[0], card[1])
            else: 
                self.setCommonPileCard(card[0], card[1])
        pass


    def makingSimulation(self, hand, simulations = 50, players = 10):
        """
        Running certain number of games and record win probability of the hand relative to the win probability of one player.
        """
        sims = []
        for i in range(simulations):

            self.__init__() 
            sims.append(self.win_loss(hand))


        
        return (sum(sims)/ simulations)/ (1/players)

    def samplingSimulation(self, hand, samples = 1000, simulations = 50, players = 10):
        """
        Running mulitple simulations and averaging the output to determine the best win score for the hand. 
        """
        results = []
        for i in range(samples):
            results.append(self.makingSimulation(hand, simulations = 50, players = 10))
        

        return round(sum(results)/ samples, ndigits=2)  

    def findProb10(self, player_no):
        """
        Return win probabilty relative to win probability of one player in the game. The score 
        """
        hand = self.player_list[player_no].cards +self.common
        hand = sorted(hand)
        if self.connection.checkCard(hand):
            return self.connection.showProbablity(hand)
        
        prob10 = self.samplingSimulation(hand, samples= 100, simulations = 10)

        # self.connection.insertHandScenario(hand, prob10)
        return prob10

    def pullHands(self):
        """
        Pulling all hands recorded in the database
        """
        cards = self.connection.query('SELECT cards from hands')

        # hands = [self.connection.convertStringCodeToTuple(card) for card in cards]
        hands = []
        for card in cards:
            
            
            hands.append(self.connection.convertStringCodeToTuple(card[0]))
        return hands

    def enterHand(self):
        """
        """
        first = input()
        second = input()
        cards
        print(self.findProb10)


    

        

