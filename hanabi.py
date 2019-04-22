from deck import Deck
from player import Player
from functools import reduce
import random
from pprint import pprint

class Hanabi:
    players = []
    deck = None
    discard_pile = []
    clock = 8
    fuse = 3
    fireworks = {'green': 0,
                 'white': 0,
                 'red': 0,
                 'yellow': 0,
                 'blue': 0}
    last_round_counter = 0

    def __init__(self, n_players):
        self.discard_pile = []
        self.clock = 8
        self.fuse = 3
        self.last_round_counter = 0
        self.last_round = False
        self.hints = {}
        
        self.deck = Deck()
        self.deck.shuffle()

        self.n_players = n_players

        for i in range(n_players):
            self.players.append(Player(i))
            self.hints[i] = []

        if n_players <= 3:
            n_cards = 5
        else:
            n_cards = 4
        
        for p in self.players:
            p.hand = [[]]*n_cards
            for i in range(n_cards):
                self.draw_card(p, i)
                #p.draw(self.deck)

        self.next_player = random.randint(0,n_players-1)



    def next_turn(self):
        if self.last_round:
            self.last_round_counter += 1

        print("\n")
        print("-"*20)
        print("Player #{}'s turn.\n".format(self.next_player))

        print("Time left: {}".format(self.clock))
        print("Fuse length: {}\n".format(self.fuse))
        print("Discarded/played cards:")
        print(self.discard_pile)
        
        print("\nFireworks: {}\n".format(self.fireworks))
        print("{} cards left in deck. ".format(self.deck.cards_left()))

        print("\nOther players' hands:")
        for p in self.players:
            if p.player_number == self.next_player:
                pass
            else:
                print("Player #{}: {}".format(p.player_number, p.hand))

        print("\nHints given:")
        pprint(self.hints)

        self.players[self.next_player].take_turn(self)
        self.next_player = (self.next_player + 1) % self.n_players


    def give_hint(self, player_number, hint):
        self.hints[player_number].append(hint)
        self.clock -= 1


    # def discard_card(self, card):
    #     self.discard_pile.append(card)
    #     self.clock = min(self.clock + 1, 8)

    def discard_card(self, player, card_num):
        # discard the card
        card = player.hand[card_num]
        self.discard_pile.append(card)
        print("Card {} discarded.".format(card))
        self.clock = min(self.clock + 1, 8)

        self.draw_card(player, card_num)

    def draw_card(self, player, card_num):
        # draw new card and put it in the place of the old one
        if self.deck.cards_left() > 0:
            player.hand[card_num] = self.deck.pop()
        else:
            player.hand[card_num] = None
            print("No more cards in deck. No card drawn")
            pass

            # remove hints relating to the old card

        print("removing hints")
        print("hints for player {}".format(player.player_number))
        print("card_num: {}".format(card_num))


        player_hints = self.hints[player.player_number]
        print(player_hints)


        new_hints = []
        for h in player_hints:
            try: 
                h[0].remove(card_num)
            except:
                pass
            if len(h[0]) == 0:
                continue
            else:
                new_hints.append(h)   
        self.hints[player.player_number] = new_hints

        print(self.hints[player.player_number])

    def play_card(self, player, card_num):
        # play the card
        card = player.hand[card_num]
        self.discard_pile.append(card)

        stack_count = self.fireworks[card[0]]
        if card[1] == stack_count + 1:
            self.fireworks[card[0]] += 1
            print("Card {} successfully added".format(card))
            print("Fireworks: {}".format(self.fireworks))
            # 5 - firework complete
            if self.fireworks[card[0]] == 5:
                print("{} firework complete! 1 hour has been added to the clock.".format(card[0]))
                self.clock = min(self.clock + 1, 8)
        else:
            print("Card {} does not match any fireworks.".format(card))
            print("Card discarded and fuse has been shortened. Fuse: {}".format(self.fuse))
            self.fuse -= 1

        self.draw_card(player, card_num)



def game_end_check(game):
    return (game.fuse == 0 
            or game.last_round_counter == game.n_players 
            or reduce(lambda x,y: x+y, game.fireworks.values()) == 25)


if __name__ == "__main__":
    print("Hanabi")
    print("Race the clock... build the fireworks... launch your rockets!\n")  
    try:
        n_players = int(input("# players (2-5): "))
    except: 
        n_players = None

    while n_players < 2 or n_players > 5:
        print("Wrong # of players.")
        try:
            n_players = int(input("# players (2-5): "))
        except: 
            n_players = None
    
    game = Hanabi(n_players)

    while not game_end_check(game):
        game.last_round = (game.deck.cards_left() == 0)

        game.next_turn()

    print("*"*20)
    final_score = reduce(lambda x,y: x+y, game.fireworks.values())
    print("Game Over. Final Score: {}".format(final_score))
    if final_score <= 5:
        print("Horrible.")
    elif final_score <= 10:
        print("Mediocre.")
    elif final_score <= 15:
        print("Honorable Attempt")
    elif final_score <= 20:
        print("Excellent, crowd pleasing.")
    elif final_score <= 24:
        print("Amazing, they will be talking about it for weeks!")
    elif final_score >= 25:
        print("Legendary, everyone left speechless, stars in their eyes!")



        
        




