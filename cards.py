import numpy as np
import itertools


# dictionary with the ranks and names of the hands in key value pairs. 
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



suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades'] # list of suits
names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] # list of card names
standard_order = {order: i+ 1 for i, order in enumerate(names)} # dictionary of names associated with an Ace low order
high_card_order = {order: i+ 1 for i, order in enumerate(names)} # dictionary of names associated with an Ace high order
high_card_order['Ace'] = 14 # changed the Ace's order to the highest value. 

# creating a dictionary the representing the cards in a deck
deck = {}
for i, suit in enumerate(suits):
    for name in names:
        # keys are 1 by 2 tuple with the first number representing the suit and the second number 
        deck[(i,high_card_order[name])] ={'suit': suit, 
                      'name': name + " of "+ suit , 
                      'order':standard_order[name], 
                      'high_order': high_card_order[name],

                      'picture': f"{name[0] if name[0] != '1' else '10' }{suit[0]}"}
                  
stringcode_card = {deck[key]['picture']: key for key in deck.keys()}




class Game:
    """
    Class builds methods for a 5 card poker game simulation.
    """
    
   

    def __init__(self, number_players = 10, dropped_players = 0):
        
        self.unused_cards = [key for key in deck.keys()]
        self.player_list = [Player(i) for i in range(number_players)]
        self.common = []
        self.common_combinations ={}
        self.setMaxes()
        # Players that discard hands
        self.dropped_players = [-(i+1) for i in range(dropped_players)] if dropped_players < number_players else [] 


    def dealCard(self, card = None):
        """
        Method pulls cards from the unused list of card dictionaries. These cards removed from the unused cards list.  
        Input: Number of cards to be deal.
        Output: Returns list of card dictionaries. 
        """
        
        if card != None:
            if card in self.unused_cards:
                index = self.unused_cards.index(card)
            else:
                print('Card not in deck.')
                return None
                
        else:
            index = int(np.random.choice([i for i in range(len(self.unused_cards))], 1))
        new = self.unused_cards[index]
        del self.unused_cards[index]   
        
        return new

    def setMaxes(self, common_max =None, hand_size = 5):
        """
        Setting the amount in a individual player's hand  or common cards
        Input: common_max, the maximum number of common or community cards
                 hand_size, the maximum number of card in an indvidual players hand.
        Output: None
        """
        self.max_common_pile = common_max
        self.max_hand_size = hand_size
        return None

    def fillPile(self, list, max):
        """
        Fill pile or hand with randomly selected card from the unused pile.
        Input: list- Pile to add to
                max- maximum cards allow in pile
        Output: altered list
        """
        
        #Checking to see the hand size is higher than max level
        if (max == None) | (max <= len(list)):
            return list
        
        #Pulling cards to deal 
        deal = []        
        for i in range(max - len(list)):
            deal.append(self.dealCard())
        
        #Adding dealt cards to the pile
        for card in deal:
            list.append(card)
        
        return list

    def fillHands(self):
        """
        Iterating thru player list and filling their hands.
        Input: None
        Output: None
        """
        # cycle through players
        for i in range(len(self.player_list)):
            # fill player's hands and sorted the card tuples
            self.player_list[i].cards = self.fillPile(self.player_list[i].cards, self.max_hand_size)
            self.player_list[i].cards = sort(self.player_list[i].cards)

        pass

    def setPlayerOneCard(self, no, suit, name):
        """
        Add known card to player's hand.
        Input: no- which player, suit- Suit of the Card, name- Which card
        Output: None
        """
        
        #Check to see if current hand size is at the max level
        if self.max_hand_size < len(self.player_list[no].cards):
            print(F'Hand is full ({self.max_hand_size} cards).')
            return None 
        
        
        card = self.dealCard((suit, name)) # pull one card into from deck
        self.player_list[no].cards.append(card) # deal into the hand
        self.player_list[no].cards = sorted(self.player_list[no].cards) # sort card tuples
        
        
        return self.player_list[no].cards

    def setCommonPileCard(self, suit, name):
        """
        Add card to Common Pile
        Input: no- which player, suit- Suit of the Card, name- Which card
        Output: None
        """
        if self.max_common_pile < len(self.common):
            print(f'Common Cards are full ({self.max_common_pile} cards).')
            return None
        card = self.dealCard((suit, name))
        self.common.append(card)
        self.common = sorted(self.common)
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
        Output the sorted order of the hand
        Input : hand - list of card dictionaries
        Output: Maximum order in the hand
        """
        return sorted([deck[card]['high_order'] for card in hand])


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

    def findingHighCard(self, hand):
        """
        Finding a high card in a hand. Checking where there is a straight and taking the second highest card.
        """
        high_order = self.findHighOrder(hand)
        if (high_order[-1] == 14) & (self.testForStraight(hand)):
            high_card = high_order[-2]
        else:
            high_card = high_order[-1]
        return high_card
       
    def checkRank(self, rank, player, hand):
        """
        Change rank of player base on previous rank
        """
        if rank > player.rank:
            # print(rank)
            player.rank = rank
            player.full_hand = hand
        return None  
    
    def changeRank(self, rank, newrank):
        """
        Change generic rank, output new rank
        """
        return newrank if rank < newrank else rank

    def rankHand(self, hand, player=0):
        """
        """
        rank = (0,0)
        i = player
        flush = self.testForFlush(hand) # checking for a flush
        straight = self.testForStraight(hand) # checking for a straight
        high_card = self.findingHighCard(hand)
        # checking the flush
        if self.testForStraightFlush(flush, straight):
            
            
            rank = self.changeRank(rank, (8, high_card))
               

        # Breaking loop base on current ranking        
        if rank > (8,0): 
            return rank
            
        multiple = self.testForMultiples(hand) # creating vectorization of orders of cards
                    
        
        four = [key for key in multiple.keys() if multiple[key] == 4] # find 4 of kinds
    
        if four != []:
            rank = self.changeRank(rank, (7, four[-1]*100+ high_card))
            

        # Breaking loop base on current ranking        
        if rank > (7,0):
            return rank
        
        three = [key for key in multiple.keys() if multiple[key] == 3]  # find 3 of kind
        two = [key for key in multiple.keys() if multiple[key] == 2] # find pairs
        
        if (three != []) & (two != []):
            rank = self.changeRank(rank, (6, three[-1]*100 +two[-1]))
             # create a rank with 3 of kind order time 100 and adding the pair order
            

        # Breaking loop base on current ranking    
        if rank > (6,0):
            return rank
        
        if flush:
            
            rank = self.changeRank(rank, (5, high_card))

        # Breaking loop base on current ranking        
        if rank > (5,0):
            return rank
            
        if straight:
            rank = self.changeRank(rank, (4, high_card))
        
        # Breaking loop base on current ranking
        if rank > (4,0):
            return rank
            
        if three != []:
            # create a rank with 3 of kind order time 100 and adding the high card
            rank = self.changeRank(rank, (3, three[-1]*100 + high_card))
        
        # Breaking loop base on current ranking
        if rank > (3,0):
            return rank
                            
        if two != []:
            
            if len(two) == 2:
                two = sorted(two)
                # create a rank with high pair times 1000, adding low pair times 100, and adding the high card
                rank = self.changeRank(rank, (2, two[-1]*1000 + two[-2]*100 + high_card))
                
            else:
                # Breaking loop base on current ranking
                if rank > (2,0):
                    return rank
                # create a rank with pair times 100, and adding the high card
                rank = self.changeRank(rank, (1, two[-1]* 100+ high_card))

        # Breaking loop base on current ranking    
        if rank > (1,0):
            return rank
        
        
        rank = self.changeRank(rank, (0, self.findHighOrder(hand)[-1]))
        return rank



    def assignRank(self):  
        """
        Run thru all possible hands and assign the highest ranking hand. 
        """
        for i, player in enumerate(self.player_list):
            # print(player.no)
            for j, hand in enumerate(player.hands):
                

                flush = self.testForFlush(hand) # checking for a flush
                straight = self.testForStraight(hand) # checking for a straight
                high_card = self.findingHighCard(hand)
                # checking the flush
                if self.testForStraightFlush(flush, straight):
                    
                    
                    rank = (8, high_card)
                    self.checkRank(rank, self.player_list[i], hand)    

                # Breaking loop base on current ranking        
                if self.player_list[i].rank > (8,0): 
                    break
                    
                multiple = self.testForMultiples(hand) # creating vectorization of orders of cards
                            
                
                four = [key for key in multiple.keys() if multiple[key] == 4] # find 4 of kinds
            
                if four != []:

                    rank = (7, four[-1]*100+ high_card) # create a rank with multiples order time 100 and adding the high card value
                    self.checkRank(rank, self.player_list[i], hand)

                # Breaking loop base on current ranking        
                if self.player_list[i].rank > (7,0):
                    break
                
                three = [key for key in multiple.keys() if multiple[key] == 3]  # find 3 of kind
                two = [key for key in multiple.keys() if multiple[key] == 2] # find pairs
                
                if (three != []) & (two != []):
                    rank = (6, three[-1]*100 +two[-1]) # create a rank with 3 of kind order time 100 and adding the pair order
                    self.checkRank(rank, self.player_list[i], hand)

                # Breaking loop base on current ranking    
                if self.player_list[i].rank > (6,0):
                    break
                
                if flush:
                    rank = (5, high_card)
                    self.checkRank(rank, self.player_list[i], hand)

                # Breaking loop base on current ranking        
                if self.player_list[i].rank > (5,0):
                    break
                    
                if straight:
                    rank = (4, high_card)
                    self.checkRank(rank, self.player_list[i], hand)
                
                # Breaking loop base on current ranking
                if self.player_list[i].rank > (4,0):
                    break
                    
                if three != []:
                    rank = (3, three[-1]*100 + high_card) # create a rank with 3 of kind order time 100 and adding the high card
                    self.checkRank(rank, self.player_list[i], hand)
                
                # Breaking loop base on current ranking
                if self.player_list[i].rank > (3,0):
                    break
                                   
                if two != []:
                    
                    if len(two) == 2:
                        two = sorted(two)
                        rank = (2, two[-1]*1000 + two[-2]*100 + high_card) # create a rank with high pair times 1000, adding low pair times 100, and adding the high card
                        self.checkRank(rank, self.player_list[i], hand)
                        
                    else:
                        # Breaking loop base on current ranking
                        if self.player_list[i].rank > (2,0):
                            break
                        rank = (1, two[-1]* 100+ high_card) # create a rank with pair times 100, and adding the high card
                        self.checkRank(rank, self.player_list[i], hand)

                # Breaking loop base on current ranking    
                if self.player_list[i].rank > (1,0):
                    break
                
                rank = (0, self.findHighOrder(player.hands[j])[-1])
                self.checkRank(rank, self.player_list[i], hand)
        pass


    
class Player:

    def __init__(self, number):
        self.cards = []
        self.no = number
        self.name = None
        self.test = {}  #test dictionary
        self.best_hand = None
        self.rank = (0,0)
        self.hands = []
        self.multiples = None
        self.flushes = None
        self.straights = None
        self.winscore = 0
        
        
        

        


    


            


