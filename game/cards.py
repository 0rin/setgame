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
        replace = True if len(Cards.cards_open) == 12 else False
        print('replace', replace)
        Cards.number_sets_found += 1
        cards_in_set = set_found.split(',')
        to_replace = []
        extra_cards = [4, 9, 14]
        for i, card in enumerate(Cards.cards_open):
            for j, set_card_id in enumerate(cards_in_set):
                print('nr cards open:', len(Cards.cards_open))
                print('i', i)
                print('id of card', card['id'])
                print('set', cards_in_set)
                print('***************************\n')
                if card['id'] == int(set_card_id):
                    if replace:
                        Cards.cards_open[i] = Cards.take_n_cards(1)[0]
                    else:
                        if not i in extra_cards:
                            print('to replace:', i)
                            to_replace.append(i)
                        else:
                            extra_cards = list(set(extra_cards) - set([i]))


                    del cards_in_set[j]

        if not replace:
            print('...............')
            print('...............')
            print('to_replace', to_replace)
            print('extra_cards', extra_cards)
            for index in to_replace:
                print('\t', Cards.cards_open)
                print('\t....')
                print('\t', Cards.cards_open[-1], '\nshould go to index', index)
                print('\t------\n')
                Cards.cards_open[index] = Cards.cards_open[extra_cards[-1]]
                del extra_cards[-1]
            del Cards.cards_open[14]
            del Cards.cards_open[9]
            del Cards.cards_open[4]
        print('einde: nr cards open:', len(Cards.cards_open))

    @classmethod
    def extra_cards_open(cls):
        """
        Inserts three cards into the open cards, such that the current lay-out
        does not change.
        """
        nr_cards_per_row = int(len(Cards.cards_open)/3)
        for i in range(3):
            print(len(Cards.cards_open))
            index = (i + 1) * nr_cards_per_row + i
            Cards.cards_open.insert(index, Cards.take_n_cards(1)[0])



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



