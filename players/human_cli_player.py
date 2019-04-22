

class Player:
    def __init__(self, n):
        self.hand = []
        self.hints = []
        self.player_number = n
        
    def give_info(self, player, info):
        pass

    def receive_info(self, info):
        pass

    # def discard_card(self, card):
    #     self.hand.remove(card)
    #     return card
    
    def draw_card(self, deck):
        if deck.cards_left() > 0:
            self.hand.append(deck.pop())
        else:
            print("No more cards in deck. No card drawn")
            pass

    def get_hints(self, game):
        hints = {}

        for p in game.players:
            if p.player_number == self.player_number:
                pass
            else:
                hints[p.player_number] = []
                card_types = set([i[0] for i in p.hand] + [i[1] for i in p.hand])
                for t in card_types:
                    card_nums = []
                    if type(t) == str:
                        for card_num, card in enumerate(p.hand):
                            if card[0] == t:
                                card_nums.append(card_num)
                    else:
                        for card_num, card in enumerate(p.hand):
                            if card[1] == t:
                                card_nums.append(card_num)
                    hint = [card_nums, t]
                    hints[p.player_number].append(hint)

        return hints


    def take_turn(self, game):
        def hint_str(hint):
            return ("Card(s) {} is {}".format(hint[0], hint[1]))


        def print_actions():
            print("1. Give information")
            print("2. Disard a card")
            print("3. Play a card")

        turn_complete = False

        while not turn_complete:
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
                hints = self.get_hints(game)
                try:
                    p = int(input("Select player to give hint to: "))
                except:
                    p = None
                if hints.get(p) == None:
                    print("Invalid player number.")
                    continue
                
                #p_hints = all_hints.get(p)
                print("Select hint to give player {}:".format(p))
                for hint_num, h in enumerate(hints[p]):
                    print("#{}: {}".format(hint_num, hint_str(h)))
                try:
                    hint_num = int(input("Hint #: "))
                    hint = hints[p][hint_num]
                    print(hint)
                    game.give_hint(p,hint)
                    print("Hint: Player {}, {} given. 1 hour lost.".format(p, hint_str(hint)))
                except:
                    print("Invalid hint #.")
                    continue


            elif action == 2:
                try:
                    card_num = int(input("Select card # to discard (0-{}): ".format(len(self.hand) - 1)))
                except:
                    card_num = None
                if card_num not in range(len(self.hand)):
                    print("Invalid card #")
                    continue

                #### discard actions
                game.discard_card(self, card_num)

                # # discard the card
                # card = self.hand[card_num]
                # game.discard_card(card)

                # # draw new card and put it in the place of the old one
                # if game.deck.cards_left() > 0:
                #     self.hand[card_num] = game.deck.pop()
                # else:
                #     self.hand[card_num] = None
                #     print("No more cards in deck. No card drawn")
                #     pass

                # # remove hints relating to the old card
                # player_hints = game.hints[self.player_number]
                # new_hints = []
                # for h in player_hints:
                #     try: 
                #         h[0].remove(card_num)
                #     except:
                #         pass
                #     if len(h[0]) == 0:
                #         continue
                #     else:
                #         new_hints.append(h)   
                # game.hints[self.player_number] = new_hints

            elif action == 3:
                try:
                    card_num = int(input("Select card # to play (0-{}): ".format(len(self.hand) - 1)))
                except:
                    card_num = None
                if card_num not in range(len(self.hand)):
                    print("Invalid card #")
                    continue

                game.play_card(self, card_num)

            else:
                continue

            turn_complete = True
        
        input("Press any key to finish turn.")






                
            
                        

            








