from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
import random



def new_game(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'new_game':
            new_shuffled_deck = Deck().new_shuffled_deck()
            Cards.deck = new_shuffled_deck
            Cards.setup_cards = Cards.take_n_cards(12)
            Cards.take_n_cards(3)
        else:
            Cards.setup_cards = []
            print('a card was clicked')
        return HttpResponseRedirect(reverse('new_game'))
    return render(request, 'game/home.html', {'setup_cards': Cards.setup_cards})
