from random import randint, shuffle

SUITS = "SHDC"

MENU = """1. Play a points card.
2. Play an effect card.
3. View your hand.
4. Draw from the deck."""


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





def create_deck():
    values = "".join(range(1, 11)) + "JQK"
    return sum([[r+s for s in SUITS] for r in values], []) + ["JR", "JB"]

def get_card_name(card):
    if card == "JR":    return "The Red Joker!"
    elif card == "JB":    return "The Black Joker!"
    r, s = card
    suits = {"C":"Clubs", "S":"Spades", "D":"Diamonds", "H":"Hearts"}
    ranks = {"1":"Ace", "J":"Jack", "Q":"Queen", "K":"King"}
    return ranks[r] if r in ranks else r + " of " + suits[s]

def display_hand(player, perms):


    print()

def get_player_names():
    names = []
    while len(names) != 2:
        print("Player {}, enter your name:".format(len(names)+1))
        n = input()
        if len(n):
            names.append(n)
    return names

def deal_hands(deck, dealer):
    print()
    p1, p2 = [], []
    for i in range(6):
        if i < 6 or dealer:
            p1.append(deck.pop(0))
            print("Player 1 drew a ", get_card_name(p1[-1]))
        if i < 6 or dealer:
            p2.append(deck.pop(0))
            print("Player 1 drew a ", get_card_name(p2[-1]))
    print()
    return p1, p2

def display_card(cards, index):
    try:
        print("{:<30}".format(cards[index], end=""))
    except IndexError:
        


def display_hands(current_player, other_player):
    p = current_player
    cards_to_show = [p.hand, p.points, p.perms]
    print("{:<30}{:<30}{:<30}".format("HAND", "POINTS CARDS:", "PERMANENT EFFECTS:"))
    biggest_list = max(cards_to_show, key=len)
    for i in range(biggest_list):
        display_card(p.hand, i)
        display_card(p.points, i)
        display_card(p.perms, i)







def validate_choice(current_player, other_player, choice):
    if choice == "4":
        return True
    elif choice == "3":
        display_hands([current_player, other_player])
    elif not len(current_player.hand):
        print("You have no cards left!")
    elif choice == "1":
        return any([card[0].isdigit() for card in current_player.hand]) # any card with a digit rank is points.
    elif choice == "2":
        return True
    else:
        print("I don't understand that.")

    return False

def select_card(hand, choice):
    valid = list(map(str, range(1, len(hand))))
    for i, card in enumerate(hand):
        print("Enter 1 to choose the", get_card_name(card))
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

    p1_hand, p2_hand = deal_hands(deck, dealer)

    player1 = Player(names[0], p1_hand)
    player2 = Player(names[0], p2_hand)

    while p1_win and not p2_win:

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
            if validate_choice(current_player, other_player):
                card, hand = select_card(current_player, other_player, choice)
                p1_points, p2_points, p1_perms, p2_perms = process_move(card, choice, perms)
                move_complete = True





        p1_win = player1.check_win(to_win)
        p2_win = player2.check_win(to_win)





