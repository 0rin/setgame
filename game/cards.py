import random


class Deck(object):
    """docstring for Cards"""

    original_deck = [{'color': color,
             'shading': shading,
             'range': range(number),
             'number': number,
             'shape': shape} for color in ['red', 'green', 'blue']
                             for number in [1, 2, 3]
                             for shading in ['solid', 'striped', 'open']
                             for shape in ['oval', 'diamond', 'rectangle']]

    def new_shuffled_deck(self):
        print('de kaarten worden opnieuw geschudt')
        deck_copy = self.original_deck[:]
        random.shuffle(deck_copy)
        return deck_copy

    def take_n_cards(self, n):
        print('setup_cards - er worden nieuwe kaarten gekozen')
        deck = Deck.new_shuffled_deck(self)
        return [deck.pop() for i in range(n)]

class Cards(object):
    """
    docstring for Cards
    This class should be able to return a number of drawn cards,
    as well as keeping track of the remainder in the deck
    """

    setup_cards = Deck().take_n_cards(12)
