import random
from itertools import combinations
from datetime import datetime


class Cards(object):
    """Creates a deck of SET cards and provides shuffled copies of it. """
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


class Game(object):
    """
    This class takes care of all the handling of cards. Like distributing
    (possibly extra) cards and validating sets. Also takes care of preserving
    the positions of the open cards.
    """

    def __init__(self):
        self.new_game()

    def new_game(self):
        self.results = Results()
        self.deck = Cards().new_shuffled_deck()
        self.cards_open = self._take_n_cards(12)
        self.correct_set_call = True
        self.hint = False

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

    def find_set(self):
        """
        Determines if there is a set in the current open cards. Returns an
        array with, either the combination of cards that is a set, or False.
        """
        self.results.correct_set_call = True
        self.results.hints += 1
        for combo in combinations(self.cards_open, 3):
            if self._validate_set(combo, False):
                return combo
        return [False]

    def process_selection(self, selected_ids):
        """
        Processes the selected combination of cards. Either they form a set, or
        they don't. Determines the current case and handles it.
        """
        selected_ids = selected_ids.split(',')
        selected = self._selected_cards(selected_ids)
        selected_cards = [item['card'] for item in selected]
        if self._validate_set(selected_cards):
            self._administration_of_set(selected_cards)
            indices_of_set = [item['index'] for item in selected]
            self._handle_found_set(indices_of_set)
        else:
            self.correct_set_call = False
            self.results.wrong_sets += 1
        self.results.start_time = datetime.now()
        self.results.end_of_game = False
        self.hint = False

    def _administration_of_set(self, selected_cards):
        """
        Take care of administration after a set was found, thus updating the
        neccessary variables.
        """
        self.results.number_sets_found += 1
        self.results.add_time_interval()
        search_time = round(sum(self.results.search_times), 2)
        result = {'set': selected_cards[:],
                  'time': search_time,
                  'length_bar':  int(2 * search_time),
                  'hint': self.hint}
        self.results.statistics_sets.append(result)
        self.results.search_times = []
        self.correct_set_call = True

    def _selected_cards(self, selected_ids):
        """Figure out which cards have been selected and their indices."""
        result = []
        for i, card in enumerate(self.cards_open):
            for card_id in selected_ids:
                if card['id'] == int(card_id):
                    result.append({'card': card, 'index': i})
                    selected_ids.remove(card_id)
        return result

    def _handle_found_set(self, indices_of_set):
        """
        Handles the correct procedure after a set was found. Either replaces
        the cards from the set with new cards, or with the extra cards that
        were previously laid down.
        """
        to_replace = []
        indices_extra_cards = self._indices_extra_cards(len(self.cards_open))
        for index in indices_of_set:
            if index in indices_extra_cards:
                # Extra card and part of set, nominate position for removal.
                self.cards_open[index] = None
                indices_extra_cards.remove(index)
                continue
            elif indices_extra_cards:
                # This set card is not extra and will be replaced by one
                # of the extra cards.
                to_replace.append(index)
            else:
                self.cards_open[index] = self._take_n_cards(1)[0]
        if indices_extra_cards:
            self._handle_extra_cards(indices_extra_cards, to_replace)
        self.cards_open = list(filter(None, self.cards_open))

    def end_game(self):
        """Ensure end of game settings are handled."""
        self.results.total_time =\
            round((datetime.now() - self.results.start_time_game)
                  .total_seconds(), 2)
        self.results.average =\
            round(self.results.total_time / self.results.number_sets_found, 2)

        self.results.score =\
            int((27 + self.results.hints + self.results.wrong_sets) *
                self.results.average)
        self.results.end_of_game = True

    def _handle_extra_cards(self, indices_extra_cards, to_replace):
        # Copy extra cards to the positions where cards need to be replaced.
        # Then turn the extra card to None, to nominate this position for
        # removal.
        # NOTE: The extra cards are not part of the set, those cards are
        # already removed.
        for index in to_replace:
            index_extra_card = indices_extra_cards[0]
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

    def _validate_set(self, combo, users_claim=True):
        """Determines if a combination of three cards is a set."""
        property_types = ['color', 'number', 'shading', 'shape']
        properties = []
        for prop_type in property_types:
            properties.append([card[prop_type] for card in combo
                              if not card['blank']])

        for prop in properties:
            uniq = list(dict.fromkeys(prop))
            if len(prop) < 3 or len(uniq) == 2:
                return False
        return True


class Results(object):
    """This class keeps track of all results and statistics."""

    def __init__(self):
        self.end_of_game = False
        self.average = 0
        self.number_sets_found = 0
        self.hints = 0
        self.wrong_sets = 0
        self.score = 0
        self.statistics_sets = []
        self.start_time = datetime.now()
        self.start_time_game = datetime.now()
        self.total_time = 0
        self.stored = False
        self.search_times = []

    def add_time_interval(self):
        """
        Adds the time spent so far on searching for a set to a list.
        Used to pause the timer when leaving the game page.
        """
        interval = (datetime.now() - self.start_time).total_seconds()
        self.search_times.append(interval)
        return
