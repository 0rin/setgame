from .cards import Deck, Cards

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

with_set = setless[:]
with_set[-1] = {'color': 'red',
                'shading': 'open',
                'range': range(0, 1),
                'number': 1,
                'shape': 'oval',
                'id': 1,
                'blank': False}

def test_new_shuffled_deck():
    assert(len(Deck().new_shuffled_deck()) == 81)

def test_new_game():
    cards = Cards()
    cards.new_game()
    assert(len(cards.deck) == 69)
    assert(cards.number_sets_found == 0)
    assert(len(cards.cards_open) == 12)
    assert(cards.hint == False)
    assert(cards.end_of_game == False)
    assert(cards.indices_of_extra_cards == [])
    assert(cards.correct_set_call == True)

def test_open_extra_cards():
    cards = Cards()
    nr_before = len(cards.cards_open)
    cards.open_extra_cards()
    assert(len(cards.cards_open) == nr_before + 3)

def test_check_for_set():
    cards = Cards()

    # There is no set
    cards.cards_open = setless
    cards.check_for_set()
    assert(cards.hint == False)

    # There is a set
    cards.cards_open = with_set
    cards.check_for_set()
    assert(cards.hint == setless[0])

def test_process_selection():
    cards = Cards()
    selection = '[42, 78, 1]'
    cards.process_selection(selection)
    assert(cards.number_sets_found == 1)
    assert(cards.correct_set_call == True)


