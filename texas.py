import numpy as np
import itertools
from cards import Game, deck, Player



class TexasHoldThem(Game):
    
    def setMaxes(self, common_max =5, hand_size = 2):
        """
        Texas Hold Them rules. 
        """
        
        
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
        


    def fill(self):
        """

        """
        self.fillCommonCards()
        
        for i in range(len(self.player_list)):
            self.player_list[i].cards = self.fillPile(self.player_list[i].cards, self.max_hand_size)
            self.player_list[i].hands = [self.player_list[i].cards + combo for combo in self.common_combinations]
            self.player_list[i].flushes = [self.testForFlush(hand) for hand in self.player_list[i].hands]
            self.player_list[i].straights = [self.testForFlush(hand) for hand in self.player_list[i].hands]
            straight_flush = [(flush) & (straight) for flush, straight in zip(self.player_list[i].flushes, self.player_list[i].straights)]
            if sum(straight_flush) > 0:
                rank

            self.player_list[i].multiples = [self.testForMultiples(hand) for hand in self.player_list[i].hands]
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

        rank = [player.rank for player in self.player_list]
        return self.player_list[0].test['rank'] == max(rank)


      
