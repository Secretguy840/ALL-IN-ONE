import random
from collections import Counter

suits = ['♠', '♥', '♦', '♣']
ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
rank_values = {r:i for i,r in enumerate(ranks, 2)}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for s in suits for r in ranks]
        random.shuffle(self.cards)
    
    def deal(self, n):
        return [self.cards.pop() for _ in range(n)]

def evaluate_hand(hand):
    values = sorted([rank_values[c.rank] for c in hand], reverse=True)
    suits = [c.suit for c in hand]
    value_counts = Counter(values)
    is_flush = len(set(suits)) == 1
    is_straight = (values == list(range(values[0], values[0]-5, -1)))
    
    if is_straight and is_flush and values[0] == 14:
        return (10, "Royal Flush")
    elif is_straight and is_flush:
        return (9, f"Straight Flush {ranks[values[0]-2]} high")
    elif 4 in value_counts.values():
        quad = [k for k,v in value_counts.items() if v == 4][0]
        return (8, f"Four of a Kind {ranks[quad-2]}s")
    elif sorted(value_counts.values()) == [2,3]:
        trio = [k for k,v in value_counts.items() if v == 3][0]
        pair = [k for k,v in value_counts.items() if v == 2][0]
        return (7, f"Full House {ranks[trio-2]}s over {ranks[pair-2]}s")
    elif is_flush:
        return (6, f"Flush {ranks[values[0]-2]} high")
    elif is_straight:
        return (5, f"Straight {ranks[values[0]-2]} high")
    elif 3 in value_counts.values():
        trio = [k for k,v in value_counts.items() if v == 3][0]
        return (4, f"Three of a Kind {ranks[trio-2]}s")
    elif list(value_counts.values()).count(2) == 2:
        pairs = sorted([k for k,v in value_counts.items() if v == 2], reverse=True)
        return (3, f"Two Pair {ranks[pairs[0]-2]}s and {ranks[pairs[1]-2]}s")
    elif 2 in value_counts.values():
        pair = [k for k,v in value_counts.items() if v == 2][0]
        return (2, f"Pair of {ranks[pair-2]}s")
    else:
        return (1, f"{ranks[values[0]-2]} high")

def play_poker():
    deck = Deck()
    players = 4
    hands = [deck.deal(5) for _ in range(players)]
    
    print("Poker Hands:\n")
    for i, hand in enumerate(hands, 1):
        hand_str = ' '.join(str(c) for c in hand)
        score, description = evaluate_hand(hand)
        print(f"Player {i}: {hand_str} → {description}")
    
    winner = max((evaluate_hand(h), i) for i,h in enumerate(hands, 1))
    print(f"\nPlayer {winner[1]} wins with {winner[0][1]}!")

play_poker()
