import random
from itertools import combinations
from datetime import datetime


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
        # print(original_deck[i]['color'],
        #       original_deck[i]['shading'],
        #       original_deck[i]['number'],
        #       original_deck[i]['shape'],
        #       original_deck[i]['id'])

    def new_shuffled_deck(self):
        """Gives a new, shuffled deck."""
        deck_copy = self.original_deck[:]
        random.shuffle(deck_copy)
        return deck_copy


class Cards(object):
    """
    This class takes care of all the handling of cards. Like distributing
    (possibly extra) cards and validating sets. Also takes care of preserving
    the positions of the open cards.
    """

    def __init__(self):
        self.new_game()

    setless = [
        {'color': 'green', 'shading': 'open', 'range': range(0, 2),
         'number': 2, 'shape': 'oval', 'id': 42, 'blank': False},
        {'color': 'blue', 'shading': 'open', 'range': range(0, 3),
         'number': 3, 'shape': 'oval', 'id': 78, 'blank': False},
        {'color': 'blue', 'shading': 'open', 'range': range(0, 1),
         'number': 1, 'shape': 'oval', 'id': 60, 'blank': False},
        {'color': 'red', 'shading': 'striped', 'range': range(0, 1),
         'number': 1, 'shape': 'rectangle', 'id': 5, 'blank': False},
        {'color': 'red', 'shading': 'striped', 'range': range(0, 3),
         'number': 3, 'shape': 'oval', 'id': 21, 'blank': False},
        {'color': 'blue', 'shading': 'solid', 'range': range(0, 3),
         'number': 3, 'shape': 'oval', 'id': 72, 'blank': False},
        {'color': 'green', 'shading': 'solid', 'range': range(0, 1),
         'number': 1, 'shape': 'oval', 'id': 27, 'blank': False},
        {'color': 'blue', 'shading': 'open', 'range': range(0, 3),
         'number': 3, 'shape': 'rectangle', 'id': 80, 'blank': False},
        {'color': 'red', 'shading': 'solid', 'range': range(0, 3),
         'number': 3, 'shape': 'oval', 'id': 18, 'blank': False},
        {'color': 'green', 'shading': 'open', 'range': range(0, 3),
         'number': 3, 'shape': 'diamond', 'id': 52, 'blank': False},
        {'color': 'green', 'shading': 'striped', 'range': range(0, 3),
         'number': 3, 'shape': 'rectangle', 'id': 50, 'blank': False},
        {'color': 'red', 'shading': 'solid', 'range': range(0, 2),
         'number': 2, 'shape': 'rectangle', 'id': 11, 'blank': False}]

    setless_extra = [
        {'color': 'blue', 'shading': 'solid', 'range': range(0, 1),
         'number': 1, 'shape': 'diamond', 'id': 55, 'blank': False},
        {'color': 'red', 'shading': 'striped', 'range': range(0, 1),
         'number': 1, 'shape': 'diamond', 'id': 4, 'blank': False},
        {'color': 'green', 'shading': 'solid', 'range': range(0, 3),
         'number': 3, 'shape': 'rectangle', 'id': 47, 'blank': False}]

    def new_game(self):
        self.deck = Deck().new_shuffled_deck()
        self.end_of_game = False
        self.number_sets_found = 0
        # self.cards_open = self._take_n_cards(12)
        self.cards_open = self.setless[:] + self.setless_extra[:]
        self.hint = False
        self.correct_set_call = True
        self.results = []
        self.start_time = datetime.now()

    def open_extra_cards(self):
        """
        Inserts three cards into the open cards, such that the current lay-out
        does not change.
        """
        # Add 3 because it is not the current situation but desired.
        indices_for_extra_cards = self._indices_extra_cards(len(self.cards_open) + 3)
        for i in indices_for_extra_cards:
            self.cards_open.insert(i, self._take_n_cards(1)[0])

    def check_for_set(self):
        """
        Determines if there is a set in the current open cards.
        Sets the 'a_set' property of this class to the id of the first card of
        a set.
        """
        self.correct_set_call = True
        for combo in combinations(self.cards_open, 3):
            if self._validate_set(combo):
                self.hint = combo[0]

    def process_selection(self, selected_ids):
        """
        Processes the selected combination of cards. Either they form a set, or
        they don't. Determines the current case and handles it.
        """
        selected_ids = selected_ids.split(',')
        selected_cards = self._selected_cards(selected_ids)
        if self._validate_set(selected_cards):
            self.number_sets_found += 1
            duration = (datetime.now() - self.start_time).total_seconds
            result = {'set': selected_cards[:],
                      'time': duration}
            self.results.append(result)
            self.correct_set_call = True
            self._handle_found_set(selected_cards)
        else:
            self.correct_set_call = False
        self.start_time = datetime.now()  # Reset start time

    def _selected_cards(self, selected_ids):
        """Figure out which cards have been selected."""
        result = []
        for card in self.cards_open:
            for card_id in selected_ids:
                if card['id'] == int(card_id):
                    result.append(card)
        return result

    def _handle_found_set(self, selected_cards):
        """
        Handles the correct procedure after a set was found. Either replaces
        the cards from the set with new cards, or with the extra cards that
        were previously laid down.
        """
        to_replace = []
        indices_extra_cards = self._indices_extra_cards(len(self.cards_open))
        for i, card in enumerate(self.cards_open):
            for j, set_card in enumerate(selected_cards):
                if card['id'] == set_card['id']:
                    if i in indices_extra_cards:
                        self.cards_open[i] = None
                        indices_extra_cards.remove(i)
                    elif indices_extra_cards:
                        # This one should be replaced by one of the extra cards
                        to_replace.append(i)
                    else:
                        self.cards_open[i] = self._take_n_cards(1)[0]
                    del selected_cards[j]
        if indices_extra_cards:
            self._move_extra_cards(indices_extra_cards, to_replace)
        self.cards_open = list(filter(None, self.cards_open))
        blanks = (card['blank'] for card in self.cards_open)
        if all(blanks):
            self.end_of_game = True

    def _move_extra_cards(self, indices_extra_cards, to_replace):
        # Copy extra cards to the positions where cards need to be replaced.
        # Note, the extra cards are not part of the set, those cards are
        # already removed.
        print('_move_extra_cards')
        print('indices_extra_cards', indices_extra_cards)
        print('to_replace', to_replace)
        for index in to_replace:

            self.cards_open[index] = self.cards_open[indices_extra_cards[-1]]
            del self.cards_open[indices_extra_cards[-1]]
            del indices_extra_cards[-1]

    def _take_n_cards(self, n):
        """Draws n cards from the deck."""
        drawn_cards = []
        for i in range(n):
            try:
                drawn_cards.append(self.deck.pop())
            except IndexError:
                drawn_cards.append({'blank': 'blank', 'id': '_'})
        return drawn_cards

    def _indices_extra_cards(self, nr_cards):
        """Determines which indices extra cards have."""
        nr_cards_per_row = int(nr_cards / 3)
        return [(i + 1) * (nr_cards_per_row - 1) + i for i in range(3)]


    def _validate_set(self, combo):
        """Determines if a combination of three cards is a set."""
        colors = []
        numbers = []
        shadings = []
        shapes = []

        for card in combo:
            if card['blank']:
                return False
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
