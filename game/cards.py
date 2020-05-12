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

    def new_game(self):
        self.deck = Deck().new_shuffled_deck()
        self.end_of_game = False
        self.number_sets_found = 0
        self.cards_open = self._take_n_cards(12)
        self.hint = False
        self.indices_of_extra_cards = []
        self.correct_set_call = True
        self.results = []
        self.start_time = datetime.now()

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
        extra_cards_open = len(self.cards_open) > 12
        to_replace = []
        extra_cards = self.indices_of_extra_cards
        for i, card in enumerate(self.cards_open):
            for j, set_card in enumerate(selected_cards):
                if card['id'] == set_card['id']:
                    if extra_cards_open and i in extra_cards:
                        # Remove from extra cards
                        extra_cards = list(set(extra_cards) - set([i]))
                    elif extra_cards_open:
                        # This one should be replaced by one of the extra cards
                        to_replace.append(i)
                    else:
                        self.cards_open[i] = self._take_n_cards(1)[0]
                    del selected_cards[j]
        if extra_cards_open:
            self._handle_extra_open_cards(extra_cards, to_replace)
        else:
            blanks = (card['blank'] for card in self.cards_open)
            if all(blanks):
                self.end_of_game = True

    def _handle_extra_open_cards(self, extra_cards, to_replace):
        # Copy extra cards to the positions where cards need to be replaced.
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
            except IndexError:
                drawn_cards.append({'blank': 'blank', 'id': '_'})
        return drawn_cards

    def _find_indices_of_extra_cards(self):
        """Determines which indices extra cards should get."""
        nr_cards_per_row = int(len(self.cards_open)/3)
        return [(i + 1) * nr_cards_per_row + i for i in range(3)]

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
