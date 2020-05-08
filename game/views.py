from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
import random


def new_game(request):
    if request.method == 'POST' or not Cards.cards_open:
        try:
            req = request.POST['req']
        except:
            req = 'new_game'
        if req == 'new_game':
            new_shuffled_deck = Deck().new_shuffled_deck()
            Cards.deck = new_shuffled_deck
            Cards.cards_open = Cards.take_n_cards(12)
            Cards.number_sets_found = 0
            Cards.a_set = False
            Cards.end_of_game = False
        elif req == 'check_set':
            Cards.a_set = Cards.check_set()
            if not Cards.a_set:
                if len(Cards.deck) >= 3:
                    Cards.cards_open = Cards.cards_open + Cards.take_n_cards(3)
                else:
                    Cards.end_of_game = True
        else:
            Cards.end_of_game = False
            Cards.a_set = False
            Cards.replace_set(req)
        return HttpResponseRedirect(reverse('new_game'))
    context = {'cards_open': Cards.cards_open,
               'number_sets_found': Cards.number_sets_found,
               'a_set': Cards.a_set,
               'end_of_game': Cards.end_of_game}
    return render(request, 'game/home.html', context)
