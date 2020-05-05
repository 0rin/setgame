from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
import random



def new_game(request):
    if request.method == 'POST':
        new_shuffled_deck = Deck().new_shuffled_deck()
        Cards.deck = new_shuffled_deck
        print('\t\tNew deck with:', len(Cards.deck), 'cards')
        Cards.setup_cards = Cards.take_n_cards(12)
        print('\t\t', len(Cards.deck), 'cards left after setting game up')
        Cards.take_n_cards(3)
        print('\t\t', len(Cards.deck), 'cards left after taking another 3.')

        return HttpResponseRedirect(reverse('new_game'))
    return render(request, 'game/home.html', {'setup_cards': Cards.setup_cards})
