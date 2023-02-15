import random

def generate_deck():
    deck = []
    colors = ['red', 'yellow', 'green', 'blue']
    special_cards = ['skip', 'reverse', 'draw2']

    for color in colors:
        for number in range(0, 10):
            deck.append(f'{color}_{number}')

    for color in colors:
        for card in special_cards:
            deck.append(f'{color}_{card}')

    deck.extend(['white_wild', 'white_draw4'])
    return deck

def shuffle_deck():
    deck = generate_deck()
    random.shuffle(deck)
    return deck


def deal_cards(deck, player_names):
    players = {player_name: [] for player_name in player_names}
    print(players, "helloooooooooooooo")

    for i in range(7 * len(player_names)):
        player_name = player_names[i % len(player_names)]
        card = random.choice(deck)
        players[player_name].append(card)
        deck.remove(card)

    return players

