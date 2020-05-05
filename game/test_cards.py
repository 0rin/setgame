from .cards import Deck, Cards
from random import randrange

def test_deck():
    assert(len(Deck().new_shuffled_deck()) == 81)

def test_cards():
    n = randrange(81)
    assert(len(Cards.take_n_cards(n)) == n)
