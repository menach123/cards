import numpy as np

suits = ['clubs', 'diamonds', 'hearts', 'spades']
names = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
standard_order = {order: i for i, order in enumerate(names)}
high_card_order = {order: i for i, order in enumerate(names)}
high_card_order['ace'] = len(names)

deck = []
for suit in suits:
    for name in names:
        deck.append({'suit': suit, 'name': name, 'order':standard_order[name], 'high_order': high_card_order[name]})

class Game:
   

    def __init__(self, number_players):
        
        self.unused_cards = deck
        self.player_list = [Player(i) for i in range(number_players)]
        self.common = []
        self.setMaxes()

    def dealCard(self, number):
        """
        Method pulls cards from the unused list of card dictionaries. These cards removed from the unused cards list.  
        Input: Number of cards to be deal.
        Output: Returns list of card dictionaries. 
        """

        index = np.random.choice(range(len(self.unused_cards)), number)
        deal = [self.unused_cards[i] for i in index]
        
        self.unused_cards = [card for i, card in enumerate(self.unused_cards) if i not in index]       
        # for i in index:
        #     self.unused_cards.pop(i)
        return deal

    def setMaxes(self, common_max =None, hand_size = None):
        self.max_common_pile = common_max
        self.max_hand_size = hand_size

    def pullSpecificCard(self, suit, name):

        for card in self.unused_cards:
            if (card['name'] == name) & (card['suit'] == suit):
                return card
        
        print("Card is not in the deck")
        return None

    def fillPile(self, list, max):
        """
        Fill pile or hand with randomly selected card from the unused pile.
        Input: list- Pile to add to, max- maximum cards allow in pile
        Output: None
        """
        if max == None:
            
            return None

        if max <= len(list):
            return None
        print(max-len(list))
        deal = self.dealCard(max-len(list))
        
        for card in deal:
            list.append(card)
        
        pass

    def fillHands(self):
        """
        Iterating thru player list and filling their hands.
        Input: None
        Output: None
        """
        for i in range(len(self.player_list)):
            self.fillPile(self.player_list[i].cards, self.max_hand_size)

        pass

    def setPlayerOneCard(self, no, suit, name):
        """
        Add card to player's hand.
        Input: no- which player, suit- Suit of the Card, name- Which card
        Output: None
        """
        if self.max_hand_size >= len(self.player_list[no].cards):
            print('Hand is full (2 cards).')
            return None 
        self.player_list[no].cards.append(self.pullSpecificCard(suit, name))
        pass

    def setCommonPileCard(self, suit, name):
        """
        Add card to Common Pile
        Input: no- which player, suit- Suit of the Card, name- Which card
        Output: None
        """
        if self.max_common_pile >= len(self.common):
            print('Common Cards are full (5 cards).')
            return None
        self.common.append(self.pullSpecificCard(suit, name))
        pass
    
        


            

class Player:

    def __init__(self, number):
        self.cards = []
        self.no = number


class TexasHoldThem(Game):

    def setMaxes(self, common_max =5, hand_size = 2):
        print(f"Common Pile {common_max}, Hand Size {hand_size}")
        self.max_common_pile = common_max
        self.max_hand_size = hand_size

    def fill(self):
        """

        """
        self.fillPile(self.common, self.max_common_pile)
        self.fillHands()
        pass




    


            


