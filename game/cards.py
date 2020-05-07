import random
from itertools import combinations


class Deck(object):
    """Creates a deck of set cards and provides shuffled copies of it. """
    original_deck = [{'color': color,
             'shading': shading,
             'range': range(number),
             'number': number,
             'shape': shape} for color in ['red', 'green', 'blue']
                             for number in [1, 2, 3]
                             for shading in ['solid', 'striped', 'open']
                             for shape in ['oval', 'diamond', 'rectangle']]
    for i in range(len(original_deck)):
        original_deck[i]['id'] = i

    def new_shuffled_deck(self):
        """Gives a new, shuffled deck."""
        deck_copy = self.original_deck[:]
        random.shuffle(deck_copy)
        return deck_copy

class Cards(object):
    """
    This class takes care of distributing new cards, while keeping track
    of the remainder in the deck.
    """
    deck = Deck().new_shuffled_deck()
    number_sets_found = 0
    cards_open = []
    a_set = False
    set_existence_requested = False

    @classmethod
    def take_n_cards(cls, n):
        """Draws n cards from the deck."""
        drawn_cards = []
        for i in range(n):
            try:
                drawn_cards.append(cls.deck.pop())
            except:
                drawn_cards.append({'blank': 'blank', 'id': '_'})
        return drawn_cards


    @classmethod
    def replace_set(cls, set_found):
        """
        Replaces the set that was found with new cards. Preserves the other
        cards and positions.
        """
        Cards.number_sets_found += 1
        cards_in_set = set_found.split(',')
        for i, card in enumerate(Cards.cards_open):
            for j, set_card_id in enumerate(cards_in_set):
                print(i, card, j, set_card_id)
                if card['id'] == int(set_card_id):
                    Cards.cards_open[i] = Cards.take_n_cards(1)[0]
                    del cards_in_set[j]

    @classmethod
    def check_set(cls):
        """
        Checks if there is a set in the current open cards.
        Returns a list with id's if there is a set, otherwise returns false.
        """
        for combo in combinations(Cards.cards_open, 3):
            if Cards.validate_set(combo):
                print('found set', combo)
                return combo

    @classmethod
    def validate_set(cls, combo):
        colors = []
        numbers = []
        shadings = []
        shapes = []

        for card in combo:
            colors.append(card['color'])
            numbers.append(card['number'])
            shadings.append(card['shading'])
            shapes.append(card['shape'])
        properties = [colors, numbers, shadings, shapes]

        for prop in properties:
            uniq = list(dict.fromkeys(prop))
            if len(uniq) == 2:
                return False
        return True



