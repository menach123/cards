from texas import TexasHoldThem, deck, stringcode_card
import itertools



def main():
    game = TexasHoldThem(10)
    player_hands = [[card for card in hand] for hand in itertools.combinations([card for card in deck.keys()], 2)]
    conn = game.connection

    for hand in player_hands:
        print(conn.convertTupleToStringCode(hand))
        prob10 = game.samplingSimulation(hand, simulations=50)
        conn.insertHandScenario(hand, prob10)
        print(conn.convertTupleToStringCode(hand), prob10)

    pass

if __name__ == "__main__":
    main()

print("Guru99")