import random


class Deck(object):
    """docstring for Deck"""

    original_deck = [{'color': color,
             'shading': shading,
             'range': range(number),
             'number': number,
             'shape': shape} for color in ['red', 'green', 'blue']
                             for number in [1, 2, 3]
                             for shading in ['solid', 'striped', 'open']
                             for shape in ['oval', 'diamond', 'rectangle']]

    def new_shuffled_deck(self):
        deck_copy = self.original_deck[:]
        random.shuffle(deck_copy)
        return deck_copy

class Cards(object):
    """
    docstring for Cards
    This class should be able to return a number of drawn cards,
    as well as keeping track of the remainder in the deck.
    Should this be a singleton class?
    """
    deck = Deck().new_shuffled_deck()
    setup_cards = []
    for i in range(12):
        setup_cards.append(deck.pop())

    @classmethod
    def take_n_cards(cls, n):
        drawn_cards = []
        for i in range(n):
            drawn_cards.append(cls.deck.pop())
        return drawn_cards
