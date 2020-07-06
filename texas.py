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
            # straight_flush = [(flush) & (straight) for flush, straight in self.player_list[i].flushes, self.player_list[i].straights]
            self.player_list[i].multiples = [self.testForMultiples(hand) for hand in self.player_list[i].hands]
        pass

    def result(self, players):
        """
        """
        rank = {key: i+1 for i , key in enumerate(sorted(list(set([player.test['rank'] for player in self.player_list[:players]])), reverse = True))}
        return self.player_list[0].test['rank'] == max(key for key in rank.keys())
      
