import colorama
from colorama import Fore, Back, Style


class Player:
    def __init__(self, n):
        self.hand_info = []
        self.hints = []
        self.player_number = n
        self.observed_states = []

        colorama.init()

    def log_observed_state(self, state):
        self.observed_states.append(state)

 
    
    # def draw_card(self, deck):
    #     if deck.cards_left() > 0:
    #         self.hand.append(deck.pop())
    #     else:
    #         print("No more cards in deck. No card drawn")
    #         pass

    # def get_hints(self, game):
    #     hints = {}

    #     for p in game.players:
    #         if p.player_number == self.player_number:
    #             pass
    #         else:
    #             hints[p.player_number] = []
    #             card_types = set([i[0] for i in p.hand] + [i[1] for i in p.hand])
    #             for t in card_types:
    #                 card_nums = []
    #                 if type(t) == str:
    #                     for card_num, card in enumerate(p.hand):
    #                         if card[0] == t:
    #                             card_nums.append(card_num)
    #                 else:
    #                     for card_num, card in enumerate(p.hand):
    #                         if card[1] == t:
    #                             card_nums.append(card_num)
    #                 hint = [card_nums, t]
    #                 hints[p.player_number].append(hint)

    #     return hints

    def hint_options(self, hands):
        hint_options = []

        for player_number, hand in hands.items():
            if player_number == self.player_number:
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
                hint = {'player': player_number,
                        'cards': card_nums,
                        'card_type': t}
                hint_options.append(hint)

        #print(hint_options)

        return hint_options



    def take_turn(self):
        state = self.observed_states[-1]

        def hint_str(hint):
            #print(hint)
            if len(hint['cards']) == 1:
                return ("Player #{}: Card {} is {}".format(hint['player'], hint['cards'], hint['card_type']))
            else:
                return ("Player #{}: Cards {} are {}".format(hint['player'], hint['cards'], hint['card_type']))

        def print_actions():
            print("1. Give information")
            print("2. Disard a card")
            print("3. Play a card")

        while True:
            print("\nSelect action (press ESC to exit):")
            print_actions()    
            try:      
                action = int(input("Action: "))
            except:
                print(action)
                if action[0] == chr(27):
                    print("Exiting.")
                    exit(0)
                action = None
            if action not in (1,2,3):
                print("Invalid action")
                continue

            if action == 1:
                print("Select hint to give: ")

                hints = self.hint_options(state['player_hands'])
                for hint_num, h in enumerate(hints):
                    print("  #{}: {}".format(hint_num, hint_str(h)))
                try:
                    hint_num = int(input("Hint #: "))
                    hint = hints[hint_num]
                    #print(hint)                       
                except:
                    print("Invalid hint #.")
                    continue

                return {'action': 'give_hint', 'action_data': hint}  

            elif action == 2:
                try:
                    card_num = int(input("Select card # to discard: "))#.format(state['player_hands'][self.player_number])))
                except:
                    card_num = None
                if card_num not in range(len(state['player_hands'][self.player_number])):
                    print("Invalid card #")
                    continue

                return {'action': 'discard_card', 'action_data': card_num}

            elif action == 3:
                try:
                    card_num = int(input("Select card # to play: "))
                except:
                    card_num = None
                if card_num not in range(len(state['player_hands'][self.player_number])):
                    print("Invalid card #")
                    continue

                return {'action': 'play_card', 'action_data': card_num}

            else:
                continue







                
            
                        

            








