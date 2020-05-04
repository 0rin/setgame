from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .setup_cards import SetupCards
from .cards import Cards
import random



def new_game(request):
    print('begin new_game method')
    if request.method == 'POST':
        # KNOP IS INGEDRUKT DUS NIEUWE KAARTEN NEERLEGGEN
        print('POST, ik wil nieuwe kaarten')
        new_cards = Cards()
        SetupCards.setup_cards = new_cards.take_n_cards(12)
        print(SetupCards.setup_cards)
        return HttpResponseRedirect(reverse('new_game'))
    return render(request, 'game/home.html', {'setup_cards': SetupCards.setup_cards})
