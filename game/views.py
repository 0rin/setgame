from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
import random



def new_game(request):
    print('begin new_game method')
    if request.method == 'POST':
        # KNOP IS INGEDRUKT DUS NIEUWE KAARTEN NEERLEGGEN
        print('POST, ik wil nieuwe kaarten')
        new_cards = Deck()
        Cards.setup_cards = new_cards.take_n_cards(12)
        return HttpResponseRedirect(reverse('new_game'))
    return render(request, 'game/home.html', {'setup_cards': Cards.setup_cards})
