import random


class Cards(object):
    """docstring for Cards"""
    # setup_cards = take_n_cards(12)


    # def __init__(self, setup_cards=[]):
    #     self.setup_cards = cls.take_n_cards(12)

    def new_shuffled_deck(self):
        print('de kaarten worden opnieuw geschudt')
        deck = [{'color': color,
                 'shading': shading,
                 'range': range(number),
                 'number': number,
                 'shape': shape} for color in ['red', 'green', 'blue']
                                 for number in [1, 2, 3]
                                 for shading in ['solid', 'striped', 'open']
                                 for shape in ['oval', 'diamond', 'rectangle']]
        random.shuffle(deck)
        return deck

    def take_n_cards(self, n):
        print('setup_cards - er worden nieuwe kaarten gekozen')
        deck = Cards.new_shuffled_deck(self)
        return [deck.pop() for i in range(n)]
