import random
from collections import deque

SUITS = ['H', 'D', 'C', 'S']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_TO_NUM = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.val = RANK_TO_NUM[rank]
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    
    def __eq__(self, other):
        return self.val == other.val

    def __lt__(self, other):
        if self.val == 2 and other.val == 14:
            return False
        elif self.val == 14 and other.val == 2:
            return True
        return self.val < other.val

    def __gt__(self, other):
        if self.val == 2 and other.val == 14:
            return True
        elif self.val == 14 and other.val == 2:
            return False
        return self.val > other.val

    def __hash__(self) -> int:
        return hash((self.suit, self.rank))



def simulate_game(shuffle_supply):
    deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    player1 = deque(deck[:26])
    player2 = deque(deck[26:])
    player1_supply = []
    player2_supply = []
    turn_count = 0
    seen = set()
    while len(player1) > 0 and len(player2) > 0:
        if shuffle_supply == False:
            if (tuple(player1), tuple(player2), tuple(player1_supply), tuple(player2_supply)) in seen:
                return -1, len(player1), len(player2)
            seen.add((tuple(player1), tuple(player2), tuple(player1_supply), tuple(player2_supply)))
        card1 = player1.popleft()
        card2 = player2.popleft()
        if card1 > card2:
            player1_supply.extend([card1, card2])
        elif card2 > card1:
            player2_supply.extend([card1, card2])
        elif len(player1) != 0 and len(player2) != 0:
            war_cards = min(4, len(player1), len(player2))
            temp = [player1.popleft() for _ in range(war_cards-1)]
            temp += [player2.popleft() for _ in range(war_cards-1)]
            war_card1 = player1.popleft()
            war_card2 = player2.popleft()
            if war_card1 > war_card2:
                player1_supply.extend(temp + [card1, card2, war_card1, war_card2])
            elif war_card2 > war_card1:
                player2_supply.extend(temp + [card1, card2, war_card1, war_card2])
            else:
                player1_supply.extend([card1, card2] + temp[0::2])
                player2_supply.extend([card1, card2] + temp[1::2])

        if len(player1) == 0:
            if shuffle_supply:
                random.shuffle(player1_supply)
            player1.extend(player1_supply)
            player1_supply = []
        if len(player2) == 0:
            if shuffle_supply:
                random.shuffle(player2_supply)
            player2.extend(player2_supply)
            player2_supply = []

        turn_count += 1

    return turn_count, len(player1), len(player2)

def main():
    print('Shuffle Supply? (y/n)')
    shuffle_supply = input() == 'y'
    print('Number of Games?')
    num_games = int(input())
    print('Shuffle Supply:', shuffle_supply)
    print('Number of Games:', num_games)
    total_turns = 0
    total_player1 = 0
    total_player2 = 0
    game_infinite = 0
    for _ in range(num_games):
        print('Playing Game:', _+1, end='\r')
        turns, player1, player2 = simulate_game(shuffle_supply)
        if turns == -1:
            game_infinite += 1
        else:
            total_turns += turns
    print('Average Turns (Completed Games):', total_turns/(num_games-game_infinite))
    print('Games that ended in a loop:', game_infinite)

if __name__ == '__main__':
    main()


        

        

