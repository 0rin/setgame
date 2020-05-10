from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
import random

cards = Cards()

def new_game(request):
    if request.method == 'POST' or not cards.cards_open:
        try:
            req = request.POST['req']
        except:
            req = 'new_game'
        if req == 'new_game':
            cards.new_game()
        elif req == 'check_set':
            cards.check_for_set()
            if not cards.a_set:
                if len(cards.deck) >= 3:
                    cards.open_extra_cards()
                else:
                    cards.end_of_game = True
        else:
            cards.end_of_game = False
            cards.a_set = False
            cards.handle_found_set(req)
        return HttpResponseRedirect(reverse('new_game'))
    context = {'cards_open': cards.cards_open,
               'number_sets_found': cards.number_sets_found,
               'a_set': cards.a_set,
               'end_of_game': cards.end_of_game,
               'row_length': len(cards.cards_open)/3}
    return render(request, 'game/home.html', context)
