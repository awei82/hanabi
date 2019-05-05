
from deck import Deck
from players.human_cli_player import Player
from functools import reduce
import random
from pprint import pprint
from copy import deepcopy

import colorama
from colorama import Fore, Back, Style

class Log:
    def __init__(self):
        self.__states = []

    def log_state(self, state):
        self.__states.append(deepcopy(state))
        return len(self.__states)

    def get_length(self):
        return len(self.__states)

    def get_state(self, n):
        return deepcopy(self.__states[n].copy())

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
        self.turn_number = 0
        self.discard_pile = []
        self.clock = 8
        self.fuse = 3
        self.last_round_counter = 0
        self.last_round = False
        self.hints = {}
        self.available_hints = []
        self.last_action_taken = None
        
        self.deck = Deck()
        self.deck.shuffle()

        self.n_players = n_players
        self.player_hands = {}

        for i in range(n_players):
            self.players.append(Player(i))
            self.hints[i] = []

        if n_players <= 3:
            n_cards = 5
        else:
            n_cards = 4
        
        for p in self.players:
            #p.hand = [None]*n_cards
            self.player_hands[p.player_number] = [None]*n_cards
            for card_num in range(n_cards):
                #self.draw_card(p, card_num)
                #p.draw(self.deck)

                self.draw_card(p.player_number, card_num)

        self.current_player = random.randint(0,n_players-1)

        for p in self.players:
            p.log_observed_state(self.observed_state(p.player_number))


        

        # log = Log()
        # log.log_state(self.game_state())


    def game_state(self):
        state = {'fireworks': self.fireworks,
             'clock': self.clock,
             'fuse': self.fuse,
             'last_round': self.last_round,
             'last_round_counter': self.last_round_counter,
             'current_player': self.current_player,
             'turn_number': self.turn_number,
             'cards_left': self.deck.cards_left(),
             'player_hands': self.player_hands,
             'discard_pile': self.discard_pile,
             'last_action_taken': self.last_action_taken
             }
        return state

    def observed_state(self, player_number):
        observed_hands = deepcopy(self.player_hands)
        masked_hand = list(map(lambda x: x != None, self.player_hands[player_number])) 
        observed_hands[player_number] = masked_hand
        state = {'fireworks': self.fireworks,
             'clock': self.clock,
             'fuse': self.fuse,
             'last_round': self.last_round,
             'last_round_counter': self.last_round_counter,
             'current_player': self.current_player,
             'turn_number': self.turn_number,
             'cards_left': self.deck.cards_left(),
             'player_hands': observed_hands,
             'discard_pile': self.discard_pile,
             'hints': self.hints,
             'last_action_taken': self.last_action_taken
             }
        return deepcopy(state)

    def next_turn(self):
        
        if self.last_round:
            print("LAST ROUND")
            self.last_round_counter += 1


        # Print game state info
        print("\n")
        print("-"*20)
        print("Player #{}'s turn.\n".format(self.current_player))

        print("Time left: {}".format(self.clock))
        print("Fuse length: {}\n".format(self.fuse))
        print("Discarded/played cards: {}\n".format(self.discard_pile))
        print("{} cards left in deck. \n".format(self.deck.cards_left()))
        
        #print("\nFireworks: {}\n".format(self.fireworks))
        self.print_fireworks()

        

        # print("\nOther players' hands:")
        # for p in self.players:
        #     if p.player_number == self.current_player:
        #         pass
        #     else:
        #         print("Player #{}: {}".format(p.player_number, self.player_hands[p.player_number]))

        print("")
        self.print_observed_hands(self.current_player)
        print("")

        #print("\nHints given:")
        #pprint(self.hints)
        self.print_hints()

        # update hint options
        #self.hint_options = self.generate_hints(self.current_player)

        player_action = self.players[self.current_player].take_turn()
        self.take_action(self.current_player, player_action)

        self.current_player = (self.current_player + 1) % self.n_players
        self.turn_number += 1

        for p in self.players:
            p.log_observed_state(self.observed_state(p.player_number))


    def take_action(self, player_number, action):
        if action['action'] == 'discard_card':
            card_num = action['action_data']
            self.discard_card(player_number, card_num)
        elif action['action'] == 'play_card':
            card_num = action['action_data']
            self.play_card(player_number, card_num)
        elif action['action'] == 'give_hint':
            # hint_num = action['num']
            # hint = self.hint_options[hint_num]
            # self.hints[hint['player']].append({'cards': hint['cards'], 'card_type': hint['card_type']})
        
            hint = action['action_data']
            if hint not in self.hint_options(player_number):
                print("Invalid Hint.")
                return -1
            else:
                self.hints[hint['player']].append({'cards': hint['cards'], 'card_type': hint['card_type']})
                self.clock -= 1
                print("Hint: {} given. 1 hour lost.".format(hint))
        
        else:
            print("Error. Invalid Action")
        self.last_action_taken = {'player': player_number,
                                  'action': action['action'],
                                  'action_data': action['action_data']}

    def hint_options(self, player_number):
        hint_options = []

        for p_num, hand in self.player_hands.items():
            if p_num == player_number:
                continue
            
            card_types = set([i[0] for i in hand] + [i[1] for i in hand])
            for t in card_types:
                card_nums = []
                if type(t) == str:
                    for card_num, card in enumerate(hand):
                        if card[0] == t:
                            card_nums.append(card_num)
                else:
                    for card_num, card in enumerate(hand):
                        if card[1] == t:
                            card_nums.append(card_num)
                hint = {'player': p_num,
                        'cards': card_nums,
                        'card_type': t}
                hint_options.append(hint)

        return hint_options


    # def give_hint(self, player_number, hint):
    #     self.hints[player_number].append(hint)
    #     self.clock -= 1



    # def discard_card(self, player, card_num):
    #     card = player.hand[card_num]
    #     self.discard_pile.append(card)
    #     print("Card {} discarded.".format(card))
    #     self.clock = min(self.clock + 1, 8)

    #     self.draw_card(player, card_num)

    def discard_card(self, player_number, card_num):
        card = self.player_hands[player_number][card_num]
        self.discard_pile.append(card)
        print("Card {} discarded.".format(card))
        self.clock = min(self.clock + 1, 8)

        self.draw_card(player_number, card_num)


    # def draw_card(self, player, card_num):
    #     # draw new card and put it in the place of the old one
    #     if self.deck.cards_left() > 0:
    #         player.hand[card_num] = self.deck.pop()
    #     else:
    #         player.hand[card_num] = None
    #         print("No more cards in deck. No card drawn")
    #         pass

    #     # remove hints relating to the old card
    #     player_hints = self.hints[player.player_number]
    #     new_hints = []
    #     for h in player_hints:
    #         try: 
    #             h[0].remove(card_num)
    #         except:
    #             pass
    #         if len(h[0]) == 0:
    #             continue
    #         else:
    #             new_hints.append(h)   
    #     self.hints[player.player_number] = new_hints

    #     #print(self.hints[player.player_number])

    def draw_card(self, player_number, card_num):
        # draw new card and put it in the place of the old one
        if self.deck.cards_left() > 0:
            self.player_hands[player_number][card_num] = self.deck.pop()
        else:
            self.player_hands[player_number][card_num] = None
            print("No more cards in deck. No card drawn")
            return 0
        
        
        # print("hints for player {}".format(player.player_number))
        # 
        # print(player_hints)

        # remove hints relating to the old card
        print("removing hints")
        print("card_num: {}".format(card_num))
        player_hints = self.hints[player_number]

        print("player_hints: {}".format(player_hints))
        new_hints = []
        for h in player_hints:
            try: 
                h['cards'].remove(card_num)
                #h[0].remove(card_num)
            except:
                continue
            if len(h['cards']) == 0:
                continue
            else:
                new_hints.append(h)   
        self.hints[player_number] = new_hints

        print(self.hints[player.player_number])



    # def play_card(self, player, card_num):
    #     # play the card
    #     card = player.hand[card_num]
    #     self.discard_pile.append(card)

    #     stack_count = self.fireworks[card[0]]
    #     if card[1] == stack_count + 1:
    #         self.fireworks[card[0]] += 1
    #         print("Card {} successfully added".format(card))
    #         print("Fireworks: {}".format(self.fireworks))
    #         # 5 - firework complete
    #         if self.fireworks[card[0]] == 5:
    #             print("{} firework complete! 1 hour has been added to the clock.".format(card[0]))
    #             self.clock = min(self.clock + 1, 8)
    #     else:
    #         print("Card {} does not match any fireworks.".format(card))
    #         print("Card discarded and fuse has been shortened. Fuse: {}".format(self.fuse))
    #         self.fuse -= 1

    #     self.draw_card(player, card_num)

    def play_card(self, player_number, card_num):
        # play the card
        card = self.player_hands[player_number][card_num]
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
            self.fuse -= 1
            print("Card discarded and fuse has been shortened. Fuse: {}".format(self.fuse))
            
        self.draw_card(player_number, card_num)

    def end_game(self):
        print("*"*20)
        final_score = reduce(lambda x,y: x+y, self.fireworks.values())
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
        return final_score

    def get_color_tag(self, color):
        if color == 'white':
            return Style.BRIGHT + Fore.WHITE
        elif color == 'yellow':
            return Style.BRIGHT + Fore.YELLOW
        elif color == 'red':
            return Style.BRIGHT + Fore.RED
        elif color == 'green':
            return Style.BRIGHT + Fore.GREEN
        elif color == 'blue':
            return Style.BRIGHT + Fore.BLUE
    
    def print_fireworks(self):
        print("Fireworks: ", end =' ')
        print(Style.BRIGHT + Fore.YELLOW + 'yellow:{}'.format(self.fireworks['yellow']) + Style.RESET_ALL, end = '  ')
        print(Style.BRIGHT + Fore.RED + 'red:{}'.format(self.fireworks['red']) + Style.RESET_ALL, end = '  ')
        print(Style.BRIGHT + Fore.WHITE + 'white:{}'.format(self.fireworks['white']) + Style.RESET_ALL, end = '  ')
        print(Style.BRIGHT + Fore.GREEN + 'green:{}'.format(self.fireworks['green']) + Style.RESET_ALL, end = '  ')
        print(Style.BRIGHT + Fore.BLUE + 'blue:{}'.format(self.fireworks['blue']) + Style.RESET_ALL)

    def print_observed_hands(self, player_number):
        print("Hands:")
        for p in self.players:
            print("  Player #{}: ".format(p.player_number), end = '')
            if p.player_number == self.current_player:
                print(list(map(lambda x: x != None, self.player_hands[player_number])), end='')
            else:
                for c in self.player_hands[p.player_number]:
                    if c != None:
                        color_tag = self.get_color_tag(c[0])
                        print(color_tag + c[0] + " " + str(c[1]) + Style.RESET_ALL, end = '  ')
                    else:
                        print("None", end = '  ')
            print("")

    def print_hints(self):
        def hint_str(hint):
            if len(hint['cards']) == 1:
                return ("Card {} is {}.".format( hint['cards'], hint['card_type']))
            else:
                return ("Cards {} are {}.".format(hint['cards'], hint['card_type']))

        print("Hints Given:")
        for p, hints in self.hints.items():
            print("  Player #{}: ".format(p), end = ' ')
            for h in hints:
                print(hint_str(h), end = ' ')
            print("")



def game_end_check(game):
    return (game.fuse == 0 
            or game.last_round_counter == game.n_players 
            or reduce(lambda x,y: x+y, game.fireworks.values()) == 25)


if __name__ == "__main__":
    colorama.init()
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

    game.end_game()

    



        
        




