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
        else:
            cards_in_set = action.split(',')
            for i, card in enumerate(Cards.setup_cards):
                for j, set_card_id in enumerate(cards_in_set):
                    if card['id'] == int(set_card_id):
                        Cards.setup_cards[i] = Cards.take_n_cards(1)[0]
                        del cards_in_set[j]
        return HttpResponseRedirect(reverse('new_game'))
    return render(request, 'game/home.html', {'setup_cards': Cards.setup_cards})
