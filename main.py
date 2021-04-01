from random import randint, shuffle, choice as rand_choice

SUITS = list("SHDC")

MENU = """1. View your hand.
2. Play a points card.
3. Play an effect card.
4. Scuttle an opponent's card.
5. Draw from the deck."""

SCUTTLE = "4"
EFFECT = "3"
POINTS = "2"

TESTING = True

def get_menu_choice(name):
    choice = input()
    if choice in ["1","2","3","4","5"]:
        i = int(choice) - 1
        msg = MENU.split("\n")[i][3:].lower().replace("your", "their")
        print(f"{name} chose to {msg}")
        return choice
    return None

class Card:
    def __init__(self, s, r):
        self.suit = s
        self.rank = r
        self.points_possible = False
        if self.rank < 11:
            self.points_possible = True
        self.steal = None

    def __gt__(self, other):

        if self.rank > other.rank:
            return True
        elif self.rank < other.rank:
            return False
        else:
            if self.suit > other.suit:
                return True
            return False

    def __repr__(self):
        return self.get_name()

    def get_name(self):
        r = self.rank
        suits = {"C": "Clubs", "S": "Spades", "D": "Diamonds", "H": "Hearts"}
        ranks = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King", 14:"Joker"}
        r = ranks[r] if r in ranks else r
        if r == "Joker":
            return "The {} {}!".format(self.suit, r)
        else:
            return f"The {r} of {suits[self.suit]}"


class Player:

    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.points = []
        self.perms = []

    def play_points_card(self, card):
        self.points += card

    def play_perm_card(self, card):
        self.perms += card

    def get_possible_points_cards(self):
        return [c for c in self.hand if c.points_possible]

    def total_points(self):
        return sum([int(c.rank) for c in self.points])

    def check_win(self):
        return self.total_points() >= self.calculate_points_needed_win()

    def has_goggles(self):
        return any([card.rank == "8" for card in self.perms])

    def calculate_points_needed_win(self):
        kings = len([card for card in self.perms if card.rank == "K"])
        return {0:21, 1:14, 2:10, 3:7, 4:5}[kings]


def create_deck():

    # flatten 2d list to 1d with sum(), add jokers and instantiate card objects
    deck = []
    for s in SUITS:
        [deck.append(Card(s, r)) for r in range(1, 14)]
    deck.append(Card("Red", 14))
    deck.append(Card("Black", 14))
    if not TESTING:
        shuffle(deck)
    return deck

def get_player_names():
    names = []
    while len(names) != 2:
        print("Player {}, enter your name:".format(len(names)+1))
        n = input()
        if len(n):
            names.append(n)
    return names

def draw_card(name, deck):
    card = deck.pop(0)
    print(f"{name} drew {card.get_name()}")
    return card


def deal_hands(names, deck, dealer):
    print()
    p1, p2 = [], []
    for i in range(6):
        if i < 6 or dealer:
            p1.append(draw_card(names[0], deck))

        if i < 6 or dealer:
            p2.append(draw_card(names[1], deck))
    print()

    if TESTING:
        for i in range(13):
            p1.append(draw_card(names[0], deck))
    return p1, p2

def display_card(cards, index):
    if not len(cards) or index >= len(cards):
        print("{:<30}".format(""), end="")
        return

    print("{:<30}".format(str(cards[index])), end="")




def display_hands(current_player, other_player):

    for i in range(2):
        p = [current_player, other_player][i]
        print()
        print(f"{p.name}'s cards:")
        print()
        cards_to_show = [p.hand, p.points, p.perms]
        print("{:<30}{:<30}{:<30}".format("CURRENT HAND:", "POINTS CARDS:", "PERMANENT EFFECTS:"))

        biggest_list = len(max(cards_to_show, key=len))
        for j in range(biggest_list):
            if i == 0 or current_player.has_goggles():
                display_card(p.hand, j)
            else:
                display_card(["?"], 0)

            display_card(p.points, j)
            display_card(p.perms, j)
            print()

def block_scuttle(player, discard_pile):
    tens = player.get_card_by_rank(10)
    if len(tens) == 1:
        card = tens[0]
        print("f{player.name}, do you want to use your {card} to block the scuttle? Enter any key if so.")
        if input():
            return True
    elif len(tens) > 1:
        print("f{player.name}, do you want to use one of your 10s to block the scuttle?")
        options = tens + ["to not do this."]
        card = select_card(options)  # a bit weird.

        if card == "to not do this.":
            return False
        else:
            discard_card(player.hand, card, discard_pile)
            return True

    return False


def process_scuttle(other_player, current_player, card, discard_pile):
    if len(other_player.points):
        print("Select which card to scuttle.")
        scuttled = select_card(other_player.points)
        if card > scuttled:
            print("{} scuttled {}'s {} points card with the {}!".format(current_player.name, other_player.name, scuttled, card))
            if not block_scuttle(other_player, discard_pile):
                discard_card(other_player.points, scuttled, discard_pile)
            return True
        else:
            print("{} is not greater than the {}!".format(card, scuttled))
            return False
    else:
        print(f"{other_player.name} has no points cards to scuttle!")
        return False

def process_move(card, current_player, other_player, action, discard_pile, deck):
    one_off = True
    print("I received an action it is", action)
    if action == SCUTTLE:
        return process_scuttle(other_player, current_player, card, discard_pile)

    elif action == POINTS:
        print(f"{current_player.name} played the {card} as POINTS.")
        current_player.points += [card]
        current_player.hand.remove(card)
        print(f"They now have {current_player.total_points()} points!")

    elif action == EFFECT:
        print(f"{current_player.name} played the {card} an EFFECT.")
        if card.rank == 1:
            print("SCRAP ALL POINTS!")
            for player in [current_player, other_player]:
                for card in player.points:
                    discard_card(player.points, card, discard_pile)

        elif card.rank == 2:
            pass
        elif card.rank == 3:
            print("RUMMAGE!")
            print("Select a card to pick up from the discard pile.")
            rummage = select_card(discard_pile)
            discard_pile.remove(rummage)
            current_player.hand += rummage
            print(f"{current_player.name} chose to pick up the {rummage}.")
        elif card.rank == 4:
            print("DISCARD 2.")
            print(f"Picking two of {other_player.name}'s cards to discard at random.")
            for i in range(2):
                discard = rand_choice(other_player.hand)
                discard_card(other_player.hand, discard, discard_pile)

        elif card.rank == 5:
            print("DRAW 2!")
            for i in range(2):
                current_player.hand += [draw_card(current_player.name, deck)]

        elif card.rank == 6:
            print("SCRAP ALL PERMANENT EFFECTS!")
            for player, other in zip([current_player, other_player], [other_player, current_player]):
                for perm_card in player.perms:
                    discard_card(player.perms, perm_card, discard_pile)
                    print(f"{perm_card} was returned to the deck.")
                    if perm_card.steal:
                        print(f"{other.name}'s stolen {perm_card.steal} points card was returned.")
                        other.points += perm_card.steal
                        perm_card.steal = None

        elif card.rank == 7:
            pass
        elif card.rank == 8:
            one_off = False
            print("GOGGLES!")
            print(f"{current_player.name} can now view {other_player.name}'s hand.")
            current_player.perms += [card]

        elif card.rank == 9:
            print("RETURN 1 PERMANENT EFFECT.")
            if not len(other_player.perms):
                print(f"{other_player.name} has no permanent effect cards to return!")
                return False


            print(f"{current_player.name}, choose which of {other_player.name}'s permanent effect cards to return to the deck.")
            perm_card = select_card(other_player.perms)


            print(f"{perm_card} was returned to the deck.")
            if perm_card.steal:
                print(f"{current_player.name}'s stolen {perm_card.steal} points card was returned.")
                current_player.points += perm_card.steal
                perm_card.steal = None
            deck = [perm_card] + deck

        elif card.rank == 11:
            one_off = False
            if not len(other_player.points):
                print(f"{other_player.name} has no points cards to steal!")
                return False

            print("STEAL A POINTS CARD!")
            print(f"{current_player.name}, choose which of {other_player.name}'s points cards to steal.")
            points_card = select_card(other_player.points)
            print(f"{points_card} was transferred to {current_player.name}")
            other_player.points.remove(points_card)
            card.steal = points_card
            current_player.points.append(points_card)
            current_player.perms += [card]

        elif card.rank == 12:
            print("QUEEN DEFENCE!")
            print(f"{current_player.name} is now protected against 2, 9 and J effects!")
            current_player.perms += [card]

        elif card.rank == 13:
            print("REDUCE POINTS NEEDED TO WIN.")
            current_player.perms += [card]
            print(f"{current_player.name} now only needs {current_player.calculate_points_needed_win()} points to win.")

        else:
            print("SWITCHEROO!")
            print("The joker is played - both players switch hands.")
            other_player.hand, current_player.hand = current_player.hand, other_player.hand


        if one_off:
            discard_card(current_player.hand, card, discard_pile)


    return True




def validate_choice(current_player, other_player, choice):
    if choice == "5":
        return True
    elif choice == "1":
        display_hands(current_player, other_player)
    elif not len(current_player.hand):
        print("You have no cards left!")
    elif choice == "3":
        return True
    elif choice in ["2", "4"]:
        your_points = [card.rank for card in current_player.hand if card.points_possible]
        their_points = [card.rank for card in other_player.hand if card.points_possible]
        if not len(your_points):
            print("You don't have any cards that can be played as points cards.")
            return False
        else:
            if choice == "2":
                return True
            else:
                if any([your_card > other_card for your_card, other_card in zip(sorted(current_player.hand), sorted(other_player.points))]):
                    return True
                else:
                    print("You don't have any cards in your hand higher in value than any of your opponent's points cards.")
                    return False

    else:
        print("I don't understand that.")

    return False

def select_card(hand):
    if not len(hand):
        print("You don't have any cards!")
        return None

    valid = list(map(str, range(1, len(hand)+1)))
    for i, card in enumerate(hand):
        print("Enter {} to choose {}".format(i+1, card))
    choice = input()
    while choice not in valid:
        choice = input("I didn't understand that.")

    chosen_card = hand[int(choice)-1]

    return chosen_card

def discard_card(remove_from, card, pile):
    remove_from.remove(card)
    pile += [card]
    print(f"{card} was added to the discard pile.")

def game():

    deck = create_deck()
    names = get_player_names()

    discard_pile = []

    to_win = 21

    p1_win = False
    p2_win = False
    turn = 0

    if randint(0, 1):
        print("Player 1 will be the dealer.")
        dealer = 0
    else:
        print("Player 2 will be the dealer.")
        dealer = 1

    p1_hand, p2_hand = deal_hands(names, deck, dealer)

    player1 = Player(names[0], p1_hand)
    player2 = Player(names[1], p2_hand)

    while not p1_win and not p2_win:

        if turn % 2 == 0:
            current_player, other_player = player1, player2
        else:
            current_player, other_player = player2, player1

        print("It's {0}'s turn!".format(current_player.name))

        move_complete = False
        while not move_complete:
            print("{0}, what would you like to do?".format(current_player.name))
            print(MENU)

            action = get_menu_choice(current_player.name)
            if action == None:
                print("I didn't understand that.")
            elif action == "1":
                display_hands(current_player, other_player)

            elif action == "5":
                current_player.hand.append(draw_card(current_player.name, deck))
                move_complete = True
            else:
                card_selection = current_player.hand
                if action == "2":
                    card_selection = current_player.get_possible_points_cards()

                card = select_card(card_selection)
                if card is not None:
                    move_complete = process_move(card, current_player, other_player, action, discard_pile, deck)











        p1_win = player1.check_win()
        p2_win = player2.check_win()

        turn += 1



if __name__ == "__main__":
    game()