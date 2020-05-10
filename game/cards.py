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
    def __init__(self):
        self.deck = Deck().new_shuffled_deck()
        self.number_sets_found = 0
        self.cards_open = []
        self.a_set = False
        self.end_of_game = False
        self.indices_of_extra_cards = []

    # For testing purposes only
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

    cards_18 = [{'color': 'green', 'shading': 'open', 'range': range(0, 2), 'number': 2, 'shape': 'oval', 'id': 42, 'blank': False},
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
            {'color': 'red', 'shading': 'solid', 'range': range(0, 2), 'number': 2, 'shape': 'rectangle', 'id': 11, 'blank': False},
            {'color': 'green', 'shading': 'open', 'range': range(0, 2), 'number': 2, 'shape': 'oval', 'id': 42, 'blank': False},
            {'color': 'blue', 'shading': 'open', 'range': range(0, 3), 'number': 3, 'shape': 'oval', 'id': 78, 'blank': False},
            {'color': 'blue', 'shading': 'open', 'range': range(0, 1), 'number': 1, 'shape': 'oval', 'id': 60, 'blank': False},
            {'color': 'red', 'shading': 'striped', 'range': range(0, 1), 'number': 1, 'shape': 'rectangle', 'id': 5, 'blank': False},
            {'color': 'red', 'shading': 'striped', 'range': range(0, 3), 'number': 3, 'shape': 'oval', 'id': 21, 'blank': False},
            {'color': 'blue', 'shading': 'solid', 'range': range(0, 3), 'number': 3, 'shape': 'oval', 'id': 72, 'blank': False}]

    def new_game(self):
        self.deck = Deck().new_shuffled_deck()
        self.number_sets_found = 0
        self.cards_open = self._take_n_cards(12)
        # self.cards_open = self.setless
        # self.cards_open = self.cards_18
        self.a_set = False
        self.end_of_game = False
        self.indices_of_extra_cards = []


    def open_extra_cards(self):
        """
        Inserts three cards into the open cards, such that the current lay-out
        does not change.
        """
        self.indices_of_extra_cards = self._find_indices_of_extra_cards()
        for i in self.indices_of_extra_cards:
            self.cards_open.insert(i, self._take_n_cards(1)[0])


    def check_for_set(self):
        """
        Checks if there is a set in the current open cards.
        Returns the first card of a set, or false.
        """
        for combo in combinations(self.cards_open, 3):
            blank = False
            for card in combo:
                # Check if there is a blank card in the combo
                if card['blank']:
                    blank = True
                    break
            # Skip validation of set if combo contains a blank card
            if blank:
                continue
            elif self._validate_set(combo):
                self.a_set = combo[0]


    def handle_found_set(self, set_found):
        """
        Handles the correct procedure after a set was found. Either replaces
        the cards from the set with new cards, or with the extra cards that
        were previously laid down.
        """
        extra_cards_open = len(self.cards_open) > 12
        self.number_sets_found += 1
        cards_in_set = set_found.split(',')
        to_replace = []
        extra_cards = self.indices_of_extra_cards

        for i, card in enumerate(self.cards_open):
            for j, set_card_id in enumerate(cards_in_set):
                if card['id'] == int(set_card_id):
                    if extra_cards_open and i in extra_cards:
                        # Remove from extra cards
                        extra_cards = list(set(extra_cards) - set([i]))
                    elif extra_cards_open:
                        # This one should be replaced by one of the extra cards
                        to_replace.append(i)
                    else:
                        self.cards_open[i] = self._take_n_cards(1)[0]
                    del cards_in_set[j]

        if extra_cards_open:
            self._handle_extra_open_cards(extra_cards, to_replace)


    def _handle_extra_open_cards(self, extra_cards, to_replace):
        # Copy extra cards to the positions where cards need to be replaced
        # Note, the extra cards are not part of the set, those cards are
        # already removed.
        for index in to_replace:
            self.cards_open[index] = self.cards_open[extra_cards[-1]]
            del extra_cards[-1]
        # Remove all the extra cards
        self.indices_of_extra_cards.reverse()
        for i in self.indices_of_extra_cards:
            del self.cards_open[i]
        self.indices_of_extra_cards = []


    def _take_n_cards(self, n):
        """Draws n cards from the deck."""
        drawn_cards = []
        for i in range(n):
            try:
                drawn_cards.append(self.deck.pop())
            except:
                drawn_cards.append({'blank': 'blank', 'id': '_'})
        return drawn_cards


    def _find_indices_of_extra_cards(self):
        result = []
        nr_cards_per_row = int(len(self.cards_open)/3)
        for i in range(3):
            result.append((i + 1) * nr_cards_per_row + i)
        return result


    def _validate_set(self, combo):
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



