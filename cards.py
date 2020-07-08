import numpy as np
import itertools

hand_rank = {8: 'Straight flush',
                7: 'Four of a kind',
                6: 'Full house',
                5: 'Flush',
                4: 'Straight',
                3: 'Three of a kind',
                2: 'Two pair',
                1: 'One pair',
                0: 'High card',
                'Straight flush': 8,
                'Four of a kind': 7,
                'Full house': 6,
                'Flush': 5,
                'Straight': 4,
                'Three of a kind': 3,
                'Two pair': 2,
                'One pair': 1,
                'High card': 0}



suits = ['clubs', 'diamonds', 'hearts', 'spades']
names = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
standard_order = {order: i for i, order in enumerate(names)}
high_card_order = {order: i for i, order in enumerate(names)}
high_card_order['ace'] = len(names)

deck = {}
for i, suit in enumerate(suits):
    for j, name in enumerate(names):
        deck[(i,high_card_order[name])] ={'suit': suit, 
                      'name': name, 
                      'order':standard_order[name], 
                      'high_order': high_card_order[name]}





class Game:
   

    def __init__(self, number_players):
        
        self.unused_cards = [key for key in deck.keys()]
        self.player_list = [Player(i) for i in range(number_players)]
        self.common = []
        self.common_combinations ={}
        self.setMaxes()


    def dealCard(self, card = None):
        """
        Method pulls cards from the unused list of card dictionaries. These cards removed from the unused cards list.  
        Input: Number of cards to be deal.
        Output: Returns list of card dictionaries. 
        """
        if card:
            index = self.unused_cards.index(card)
        else:
            index = int(np.random.choice([i for i in range(len(self.unused_cards))], 1))
        new = self.unused_cards[index]
        del self.unused_cards[index]   
        
        return new

    def setMaxes(self, common_max =None, hand_size = 5):
        """
        Setting the amount in a individual player's hand  or common cards
        """
        self.max_common_pile = common_max
        self.max_hand_size = hand_size
        return None

    def fillPile(self, list, max):
        """
        Fill pile or hand with randomly selected card from the unused pile.
        Input: list- Pile to add to, max- maximum cards allow in pile
        Output: None
        """
        
        if max == None:
            
            return list

        if max <= len(list):
            return list
        
        deal = []
        
        for i in range(max - len(list)):
            deal.append(self.dealCard())
        
        for card in deal:
            
            list.append(card)
        
        return list

    def fillHands(self):
        """
        Iterating thru player list and filling their hands.
        Input: None
        Output: None
        """
        for i in range(len(self.player_list)):

            self.player_list[i].cards = self.fillPile(self.player_list[i].cards, self.max_hand_size)

        pass

    def setPlayerOneCard(self, no, suit, name):
        """
        Add card to player's hand.
        Input: no- which player, suit- Suit of the Card, name- Which card
        Output: None
        """
        if self.max_hand_size < len(self.player_list[no].cards):
            print('Hand is full (2 cards).')
            return None 
        card = self.dealCard((suit, name))
        self.player_list[no].cards.append(card)
        # self.unused_cards = [new_card for new_card in self.unused_cards if new_card != card]
        
        return self.player_list[no].cards

    def setCommonPileCard(self, suit, name):
        """
        Add card to Common Pile
        Input: no- which player, suit- Suit of the Card, name- Which card
        Output: None
        """
        if self.max_common_pile < len(self.common):
            print('Common Cards are full (5 cards).')
            return None
        card = self.dealCard((suit, name))
        self.common.append(card)
        # self.unused_cards = [new_card for new_card in self.unused_cards if new_card != card]
        
        return self.common

    def showCards(self):
        """
        Show all the players hands in print statements
        """
        for player in self.player_list:
            print(player.no)
            for card in player.cards:
                print(deck[card]['suit'], deck[card]['name'])
        print('Common Cards')

        for card in self.common:
            print(deck[card]['suit'], deck[card]['name'])
        pass
          
    def testForMultiples(self, hand):
        """
        Generate order:multiple pairs based on a hand.
        Input : hand - list of card dictionaries
        Output: Dictionary of multiples
        """
        # creating key based on the order in the hand
        orders = list(set([deck[card]['high_order'] for card in hand]))

        # making initial dictionary of orders
        order_dictionary = {i:0 for i in orders}

        # added orders
        for word in [deck[card]['high_order'] for card in hand]:
            order_dictionary[word] += 1

        # create order:multiple pairs with multiples more than 1
        return {key:order_dictionary[key] for key in order_dictionary.keys() if order_dictionary[key] > 1}

    def findHighOrder(self, hand):
        """
        Output the highest card
        Input : hand - list of card dictionaries
        Output: Maximum order in the hand
        """
        return sorted([deck[card]['high_order'] for card in hand])

    def pullHighCard(self, hand):
        """
        Pull high card
        """
        return self.findHighOrder(hand)[-1]

    def pullStraightHighCard(self, hand):
        """
        Selecting the second highest card because of the dual nature of the ace
        """
        return self.findHighOrder(hand)[-2]

    def testForStraight(self, hand):
        """
        Testing for a straight in a hand
        Input : hand - list of card dictionaries
        Output: Boolean
        """
        high_orders = sorted([deck[card]['high_order'] for card in hand])
        high_orders = len([1 for i, order in enumerate(high_orders[1:]) if high_orders[i]+ 1 == order])-len(hand) == -1 
        # if length of the generated list is one less then the hand

        low_orders = sorted([deck[card]['order'] for card in hand])
        low_orders = len([1 for i, order in enumerate(low_orders[1:]) if low_orders[i]+ 1 == order])-len(hand) == -1

        return high_orders | low_orders

    def testForFlush(self,hand):
        """
        Testing for a flush
        Input : hand - list of card dictionaries
        Output: Boolean
        """
        # creating key based on the suit in the hand
        suits = set([deck[card]['suit'] for card in hand])
        return len(suits) == 1

    def testForStraightFlush(self, flush, straight):
        """
        Determine if theres is a straight flush.
        Input :  testForStraight and testForFlush
        Output: Boolean
        """
        return (flush) & (straight)



    def checkRank(self, rank, player, hand):
        """
        Change rank of player base on previous rank
        """
        if rank > player.rank:
            # print(rank)
            player.rank = rank
            player.full_hand = hand
        return None  

    def assignRank(self):  
        """
        Run thru all possible hands and assign the highest ranking hand. 
        """
        for i, player in enumerate(self.player_list):
            # print(player.no)
            for j, hand in enumerate(player.hands):
                
                flush = self.testForFlush(hand)
                straight = self.testForStraight(hand)
                if self.testForStraightFlush(flush, straight):
                    rank = (8, self.pullStraightHighCard(hand))
                    self.checkRank(rank, self.player_list[i], hand)    
                        
                if self.player_list[i].rank > (8,0):
                    break
                    
                multiple = self.testForMultiples(hand)
                            
                four = [key for key in multiple.keys() if multiple[key] == 4] 
                
                if four != []:
                    rank = (7, four[-1])
                    self.checkRank(rank, self.player_list[i], hand)
                        
                if self.player_list[i].rank > (7,0):
                    break
                
                three = [key for key in multiple.keys() if multiple[key] == 3] 
                two = [key for key in multiple.keys() if multiple[key] == 2] 
                
                if (three != []) & (two != []):
                    rank = (6, three[-1]*100 +two[-1])
                    self.checkRank(rank, self.player_list[i], hand)
                    
                if self.player_list[i].rank > (6,0):
                    break
                
                if flush:
                    rank = (5, self.findHighOrder(hand)[-1])
                    self.checkRank(rank, self.player_list[i], hand)
                        
                if self.player_list[i].rank > (5,0):
                    break
                    
                if (straight):
                    rank = (4, self.findHighOrder(hand)[-2])
                    self.checkRank(rank, self.player_list[i], hand)
                
                
                if self.player_list[i].rank > (4,0):
                    break
                    
                if three != []:
                    rank = (3, three[-1])
                    self.checkRank(rank, self.player_list[i], hand)
                
                if self.player_list[i].rank > (3,0):
                    break
                    
                two = [key for key in multiple.keys() if multiple[key] == 2] 
                
                if two != []:
                    
                    if len(two) == 2:
                        two = sorted(two)
                        rank = (2, two[-1]*100 + two[-2])
                        self.checkRank(rank, self.player_list[i], hand)
                        
                    else:
                        if self.player_list[i].rank > (2,0):
                            break
                        rank = (1, two[-1])
                        self.checkRank(rank, self.player_list[i], hand)
                    
                if self.player_list[i].rank > (1,0):
                    break
                
                rank = (0, self.findHighOrder(player.hands[j])[-1])
                self.checkRank(rank, self.player_list[i], hand)
                
            # print(self.player_list[i].rank)
            # print(self.player_list[i].full_hand)
        
        pass


    
class Player:

    def __init__(self, number):
        self.cards = []
        self.no = number
        self.name = None
        self.test = {}  #test dictionary
        self.full_hand = []
        self.rank = (0,0)
        self.hands = []
        self.multiples = None
        self.flushes = None
        self.straights = None
        
        

        


    


            


