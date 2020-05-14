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

setless_extra = [
    {'color': 'blue', 'shading': 'solid', 'range': range(0, 1),
     'number': 1, 'shape': 'diamond', 'id': 55, 'blank': False},
    {'color': 'red', 'shading': 'striped', 'range': range(0, 1),
     'number': 1, 'shape': 'diamond', 'id': 4, 'blank': False},
    {'color': 'green', 'shading': 'solid', 'range': range(0, 3),
     'number': 3, 'shape': 'rectangle', 'id': 47, 'blank': False}]

with_set = setless[:]
with_set[-1] = {'color': 'red', 'shading': 'open', 'range': range(0, 1),
                'number': 1, 'shape': 'oval', 'id': 6, 'blank': False}


def test_new_shuffled_deck():
    assert(len(Deck().new_shuffled_deck()) == 81)


def test_new_game():
    cards = Cards()
    cards.new_game()
    assert(len(cards.deck) == 69)
    assert(cards.number_sets_found == 0)
    assert(len(cards.cards_open) == 12)
    assert(not cards.hint)
    assert(not cards.end_of_game)
    assert(cards.correct_set_call)


def test_open_extra_cards():
    cards = Cards()
    nr_before = len(cards.cards_open)
    cards.open_extra_cards()
    assert(len(cards.cards_open) == nr_before + 3)


def test_check_for_set():
    cards = Cards()

    # There is no set
    cards.cards_open = setless
    assert(not cards.check_for_set()[0])

    # There is a set
    cards.cards_open = with_set
    cards.check_for_set()
    assert(cards.check_for_set()[0] == with_set[0])


def test_process_selection():
    cards = Cards()
    selection = '42,78,6'
    cards.cards_open = with_set
    cards.process_selection(selection)
    assert(cards.correct_set_call)
    assert(cards.number_sets_found == 1)


def test_indices_extra_cards():
    cards = Cards()
    assert(cards._indices_extra_cards(12) == [])
    assert(cards._indices_extra_cards(15) == [4, 9, 14])
    assert(cards._indices_extra_cards(18) == [5, 11, 17])
    assert(cards._indices_extra_cards(21) == [6, 13, 20])


def test_handling_extra_cards():
    cards = Cards()
    cards.cards_open = setless + setless_extra
    assert(len(cards.cards_open) == 15)
    cards.check_for_set()
    assert(not cards.hint)
    cards.open_extra_cards()
    assert(len(cards.cards_open) == 18)

def test_full_game():
    cards = Cards()
    cards.new_game()
    while not cards.end_of_game:
        assert(len(cards.cards_open) % 3 == 0)
        assert(len(cards.deck) % 3 == 0)
        a_set = cards.check_for_set()
        if a_set[0] != False:
            ids = ','.join(str(card['id']) for card in a_set)
            cards.process_selection(ids)
            cards.end_of_game = False
            assert(len(cards.cards_open) % 3 == 0)
        elif len(cards.deck) >= 3:
            cards.open_extra_cards()
        else:
            cards.end_game()

def test_multiple_full_games():
    for i in range(10):
        test_full_game()
