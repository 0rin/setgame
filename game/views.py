from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
import random


def new_game(request):
    set_existence = Cards.check_set()
    if request.method == 'POST' or not Cards.cards_open:
        print(request.POST)
        try:
            req = request.POST['req']
        except:
            req = 'new_game'
        print('req', req)
        if req == 'new_game':
            new_shuffled_deck = Deck().new_shuffled_deck()
            Cards.deck = new_shuffled_deck
            Cards.cards_open = Cards.take_n_cards(12)
            Cards.number_sets_found = 0
            Cards.set_existence_requested = False
            Cards.a_set = False
        elif req == 'check_set':
            Cards.set_existence_requested = True
            Cards.a_set = Cards.check_set()
        elif req == 'no_set':
            print('there was no set, give more cards')
            Cards.cards_open = Cards.cards_open + Cards.take_n_cards(3)
            print('cards now:', len(Cards.cards_open))
        else:
            Cards.set_existence_requested = False
            Cards.a_set = False
            Cards.replace_set(req)
        return HttpResponseRedirect(reverse('new_game'))
    context = {'cards_open': Cards.cards_open,
               'number_sets_found': Cards.number_sets_found,
               'set_existence_requested': Cards.set_existence_requested,
               'a_set': Cards.a_set}
    return render(request, 'game/home.html', context)
