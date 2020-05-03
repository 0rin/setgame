from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

# deck = [{'color': color,
#          'shading': shading,
#          'range': range(number),
#          'number': number,
#          'shape': shape} for color in ['red', 'green', 'blue']
#                          for number in [1, 2, 3]
#                          for shading in ['solid', 'striped', 'open']
#                          for shape in ['oval', 'diamond', 'rectangle']]
# random.shuffle(deck)
# setup_cards = [deck.pop() for i in range(12)]


def new_game(request, setup_cards=[]):
    if request.method == 'POST':
        # KNOP IS INGEDRUKT DUS NIEUWE KAARTEN NEERLEGGEN
        deck = [{'color': color,
                 'shading': shading,
                 'range': range(number),
                 'number': number,
                 'shape': shape} for color in ['red', 'green', 'blue']
                                 for number in [1, 2, 3]
                                 for shading in ['solid', 'striped', 'open']
                                 for shape in ['oval', 'diamond', 'rectangle']]
        random.shuffle(deck)
        setup_cards = [deck.pop() for i in range(12)]
    return render(request, 'game/home.html', {'setup_cards': setup_cards})
        # return HttpResponseRedirect(reverse('new_game'))
    # else:
    #     # REFRESH, DUS GEEN KAARTEN NOG, OF DE KAARTEN DIE ER AL WAREN
    #     return render(request, 'game/home.html', {'setup_cards': setup_cards})
