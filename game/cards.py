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
        self.correct_set_call = True
        self.results = []
        self.start_time = datetime.now()
        self.start_time_game = datetime.now()
        self.total_time = ' - Game not ended yet - '

    def open_extra_cards(self):
        """
        Inserts three cards into the open cards, such that the current lay-out
        does not change.
        """
        # Add 3 because it is not the current situation but desired.
        indices_for_extra_cards =\
            self._indices_extra_cards(len(self.cards_open) + 3)
        for i in indices_for_extra_cards:
            self.cards_open.insert(i, self._take_n_cards(1)[0])

    def check_for_set(self):
        """
        Determines if there is a set in the current open cards. Returns an
        array with, either the combination of cards that is a set, or False.
        """
        self.correct_set_call = True
        for combo in combinations(self.cards_open, 3):
            if self._validate_set(combo):
                return combo
        return [False]

    def process_selection(self, selected_ids):
        """
        Processes the selected combination of cards. Either they form a set, or
        they don't. Determines the current case and handles it.
        """
        selected_ids = selected_ids.split(',')
        selected_cards = self._selected_cards(selected_ids)
        if self._validate_set(selected_cards):
            self.number_sets_found += 1
            duration =\
                round((datetime.now() - self.start_time).total_seconds(), 2)
            result = {'set': selected_cards[:],
                      'time': duration,
                      'hint': self.hint}
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
            for set_card in selected_cards:
                if card['id'] == set_card['id']:
                    if i in indices_extra_cards:
                        # Extra card and part of set, will be removed later.
                        self.cards_open[i] = None
                        indices_extra_cards.remove(i)
                    elif indices_extra_cards:
                        # This set card is not extra, will be replaced by one
                        # of the extra cards.
                        to_replace.append(i)
                    else:
                        # There are no extra cards.
                        self.cards_open[i] = self._take_n_cards(1)[0]
                    selected_cards.remove(set_card)
        # Move extra cards if any.
        if indices_extra_cards:
            self._move_extra_cards(indices_extra_cards, to_replace)

        # Remove the extra cards that were part of the set.
        self.cards_open = list(filter(None, self.cards_open))

    def end_game(self):
        """Ensure end of game settings are handled."""
        self.total_time =\
            round((datetime.now() - self.start_time_game).total_seconds(), 2)
        self.end_of_game = True

    def _move_extra_cards(self, indices_extra_cards, to_replace):
        # Copy extra cards to the positions where cards need to be replaced.
        # Note, the extra cards are not part of the set, those cards are
        # already removed.
        for index in to_replace:
            index_extra_card = indices_extra_cards[-1]
            self.cards_open[index] = self.cards_open[index_extra_card]
            self.cards_open[index_extra_card] = None
            indices_extra_cards.remove(index_extra_card)

    def _take_n_cards(self, n):
        """Take n cards from the deck."""
        cards_taken = []
        for i in range(n):
            try:
                cards_taken.append(self.deck.pop())
            except IndexError:
                cards_taken.append({'blank': 'blank', 'id': '_'})
        return cards_taken

    def _indices_extra_cards(self, nr_cards):
        """Determines which indices extra cards have."""
        if nr_cards > 12:
            nr_cards_per_row = int(nr_cards / 3)
            return [(i + 1) * (nr_cards_per_row - 1) + i for i in range(3)]
        else:
            return []

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
