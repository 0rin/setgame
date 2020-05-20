from .game import Cards, Game
import logging

logging.basicConfig(level=logging.WARN, filename='test_game.log')

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
    assert(len(Cards().new_shuffled_deck()) == 81)


def test_new_game():
    game = Game()
    game.new_game()
    assert(len(game.deck) == 69)
    assert(game.results.number_sets_found == 0)
    assert(len(game.cards_open) == 12)
    assert(not game.hint)
    assert(not game.results.end_of_game)
    assert(game.correct_set_call)


def test_open_extra_cards():
    game = Game()
    nr_before = len(game.cards_open)
    game.open_extra_cards()
    assert(len(game.cards_open) == nr_before + 3)


def test__try_find_set():
    game = Game()

    # There is no set
    game.cards_open = setless
    assert(not game._try_find_set()[0])

    # There is a set
    game.cards_open = with_set
    assert(game._try_find_set()[0] == with_set[0])


def test_process_selection():
    game = Game()
    selection = '42,78,6'
    game.cards_open = with_set
    game.process_selection(selection)
    assert(game.correct_set_call)
    assert(game.results.number_sets_found == 1)


def test_indices_extra_cards():
    game = Game()
    assert(game._indices_extra_cards(12) == [])
    assert(game._indices_extra_cards(15) == [4, 9, 14])
    assert(game._indices_extra_cards(18) == [5, 11, 17])
    assert(game._indices_extra_cards(21) == [6, 13, 20])


def test_handling_extra_cards():
    game = Game()
    game.cards_open = setless + setless_extra
    assert(len(game.cards_open) == 15)
    game._try_find_set()
    assert(not game.hint)
    game.open_extra_cards()
    assert(len(game.cards_open) == 18)


def test_full_game():
    logging.info('------------Start new game')
    game = Game()
    game.new_game()
    while not game.results.end_of_game:
        assert(len(game.cards_open) % 3 == 0)
        assert(len(game.deck) % 3 == 0)
        a_set = game._try_find_set()
        if a_set[0]:
            ids = ','.join(str(card['id']) for card in a_set)
            game.process_selection(ids)
            game.results.end_of_game = False
            assert(len(game.cards_open) % 3 == 0)
            logging.info('Found set nr {}'
                         .format(game.results.number_sets_found))
        elif len(game.deck) >= 3:
            game.open_extra_cards()
            assert(len(game.cards_open) <= 21)  # 20 cards garantees a set
            logging.info('No set, nr cards open goes to {}'
                         .format(len(game.cards_open)))
            if len(game.cards_open) > 18:
                logging.warning('This should be really exceptional')
        else:
            game.end_game()


def test_multiple_full_games():
    for i in range(100):
        test_full_game()
