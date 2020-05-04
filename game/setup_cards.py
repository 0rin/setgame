from .cards import Cards


class SetupCards(object):
    """docstring for SetupCards"""

    cards = Cards()
    setup_cards = cards.take_n_cards(12)
