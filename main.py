from random import randint, shuffle

SUITS = "SHDC"

MENU = """1. View your hand.
2. Play a points card.
3. Play an effect card.
4. Scuttle an opponent's card.
5. Draw from the deck."""

class Card:
    def __init__(self, code):
        self.code = code
        self.rank = int(code[0]) if code[0].isdigit() else 0
        self.points_possible = False
        if self.rank:
            self.points_possible = True
        self.suit = SUITS.index(code[1]) if code[1] in SUITS else None

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
        if self.code == "JR":
            return "The Red Joker!"
        elif self.code == "JB":
            return "The Black Joker!"
        r, s = self.code
        suits = {"C": "Clubs", "S": "Spades", "D": "Diamonds", "H": "Hearts"}
        ranks = {"1": "Ace", "J": "Jack", "Q": "Queen", "K": "King"}
        r = ranks[r] if r in ranks else r
        return r + " of " + suits[s]


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

    def check_win(self, to_win):
        return sum(int(c[0] for c in self.points)) >= to_win

    def has_goggles(self):
        return any([card[0] == "8" for card in self.perms])




def create_deck():
    values = "".join(map(str, range(1, 11))) + "JQK"
    # flatten 2d list to 1d with sum(), add jokers and instantiate card objects
    all_codes = sum([[r+s for s in SUITS] for r in values], []) + ["JR", "JB"]
    return [Card(code) for code in all_codes]

def get_player_names():
    names = []
    while len(names) != 2:
        print("Player {}, enter your name:".format(len(names)+1))
        n = input()
        if len(n):
            names.append(n)
    return names

def deal_hands(names, deck, dealer):
    print()
    p1, p2 = [], []
    for i in range(6):
        if i < 6 or dealer:
            card = deck.pop(0)
            p1.append(card)
            print(f"{names[0]} drew a {card.get_name()}")
        if i < 6 or dealer:
            card = deck.pop(0)
            p2.append(card)
            print(f"{names[1]} drew a {card.get_name()}")
    print()
    return p1, p2

def display_card(cards, index):
    if not len(cards) or index >= len(cards):
        return

    print("{:<30}".format(str(cards[index]), end=""))




def display_hands(current_player, other_player):

    for i in range(2):
        p = [current_player, other_player][i]
        print()
        print(f"{p.name}'s cards:")
        print()
        cards_to_show = [p.hand, p.points, p.perms]
        print("{:<30}{:<30}{:<30}".format("HAND", "POINTS CARDS:", "PERMANENT EFFECTS:"))

        biggest_list = len(max(cards_to_show, key=len))
        for j in range(biggest_list):
            if i == 0 or current_player.has_goggles():
                display_card(p.hand, j)
            else:
                display_card(["?"], 0)

            display_card(p.points, j)
            display_card(p.perms, j)








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

def validate_card(other_player, choice):
    return True


def select_card(hand, choice):
    valid = list(map(str, range(1, len(hand))))
    for i, card in enumerate(hand):
        print("Enter 1 to choose the", card.get_name())
    choice = input()
    while choice not in valid:
        choice = input("I didn't understand that.")

    chosen_card = hand.pop(int(choice)-1)

    return chosen_card, hand

def game():

    deck = create_deck()
    names = get_player_names()


    p1_points = 0
    p2_points = 0
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

            choice = input()
            if validate_choice(current_player, other_player, choice):
                card, hand = select_card(current_player, choice)
                if validate_card(other_player, choice):
                    process_move(card, current_player, other_player, choice)
                move_complete = True





        p1_win = player1.check_win(to_win)
        p2_win = player2.check_win(to_win)





if __name__ == "__main__":
    game()