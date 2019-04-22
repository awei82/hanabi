import random

class Deck:
    cards = []
    def __init__(self):
        for card_num in range(1,6):
            if card_num == 1:
                n = 3
            elif card_num == 5:
                n = 1
            else:
                n = 2
            for _ in range(n):
                self.cards.append(('green', card_num))
                self.cards.append(('white', card_num))
                self.cards.append(('red', card_num))
                self.cards.append(('yellow', card_num))
                self.cards.append(('blue', card_num))

    def shuffle(self):
        random.shuffle(self.cards)

    def pop(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            print("No more cards in deck!")
            return None

    def cards_left(self):
        return len(self.cards)

    


    