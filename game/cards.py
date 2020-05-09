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
        original_deck[i]['blank'] = False


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
    end_of_game = False
    indices_of_extra_cards = []
    # For testing purposes
    setless = [{'color': 'green', 'shading': 'open', 'range': range(0, 2), 'number': 2, 'shape': 'oval', 'id': 42, 'blank': False},
            {'color': 'blue', 'shading': 'open', 'range': range(0, 3), 'number': 3, 'shape': 'oval', 'id': 78, 'blank': False},
            {'color': 'blue', 'shading': 'open', 'range': range(0, 1), 'number': 1, 'shape': 'oval', 'id': 60, 'blank': False},
            {'color': 'red', 'shading': 'striped', 'range': range(0, 1), 'number': 1, 'shape': 'rectangle', 'id': 5, 'blank': False},
            {'color': 'red', 'shading': 'striped', 'range': range(0, 3), 'number': 3, 'shape': 'oval', 'id': 21, 'blank': False},
            {'color': 'blue', 'shading': 'solid', 'range': range(0, 3), 'number': 3, 'shape': 'oval', 'id': 72, 'blank': False},
            {'color': 'green', 'shading': 'solid', 'range': range(0, 1), 'number': 1, 'shape': 'oval', 'id': 27, 'blank': False},
            {'color': 'blue', 'shading': 'open', 'range': range(0, 3), 'number': 3, 'shape': 'rectangle', 'id': 80, 'blank': False},
            {'color': 'red', 'shading': 'solid', 'range': range(0, 3), 'number': 3, 'shape': 'oval', 'id': 18, 'blank': False},
            {'color': 'green', 'shading': 'open', 'range': range(0, 3), 'number': 3, 'shape': 'diamond', 'id': 52, 'blank': False},
            {'color': 'green', 'shading': 'striped', 'range': range(0, 3), 'number': 3, 'shape': 'rectangle', 'id': 50, 'blank': False},
            {'color': 'red', 'shading': 'solid', 'range': range(0, 2), 'number': 2, 'shape': 'rectangle', 'id': 11, 'blank': False}]

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
    def handle_found_set(cls, set_found):
        """
        Handles the correct procedure after a set was found. Either replaces
        those cards, or removes them.
        """
        extra_cards_open = len(Cards.cards_open) > 12
        Cards.number_sets_found += 1
        cards_in_set = set_found.split(',')
        to_replace = []
        extra_cards = Cards.indices_of_extra_cards

        for i, card in enumerate(Cards.cards_open):
            for j, set_card_id in enumerate(cards_in_set):
                if card['id'] == int(set_card_id):
                    if extra_cards_open and i in extra_cards:
                        # Remove from extra cards
                        extra_cards = list(set(extra_cards) - set([i]))
                    elif extra_cards_open:
                        # This card needs to be replaced by one of the extra cards
                        to_replace.append(i)
                    else:
                        Cards.cards_open[i] = Cards.take_n_cards(1)[0]
                    del cards_in_set[j]

        if extra_cards_open:
            # Copy extra cards to the positions where cards need to be replaced
            # Note, the extra cards are not part of the set, those cards are
            # already removed.
            for index in to_replace:
                Cards.cards_open[index] = Cards.cards_open[extra_cards[-1]]
                del extra_cards[-1]
            # Remove all the extra cards
            Cards.indices_of_extra_cards.reverse()
            for i in Cards.indices_of_extra_cards:
                del Cards.cards_open[i]
            Cards.indices_of_extra_cards = []


    @classmethod
    def open_extra_cards(cls):
        """
        Inserts three cards into the open cards, such that the current lay-out
        does not change.
        """
        Cards.indices_of_extra_cards = Cards.find_indices_of_extra_cards()
        for i in Cards.indices_of_extra_cards:
            Cards.cards_open.insert(i, Cards.take_n_cards(1)[0])


    @classmethod
    def find_indices_of_extra_cards(cls):
        result = []
        nr_cards_per_row = int(len(Cards.cards_open)/3)
        for i in range(3):
            result.append((i + 1) * nr_cards_per_row + i)
        return result


    @classmethod
    def check_set(cls):
        """
        Checks if there is a set in the current open cards.
        Returns the first card of a set, or false.
        """
        for combo in combinations(Cards.cards_open, 3):
            blank = False
            for card in combo:
                # Check if there is a blank card in the combo
                if card['blank']:
                    blank = True
                    break
            # Skip validation of set if combo contains a blank card
            if blank:
                continue
            elif Cards.validate_set(combo):
                return combo[0]


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



