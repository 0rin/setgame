from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
from .models import Highscore

cards = Cards()


def game(request):
    if request.method == 'POST':
        try:
            req = request.POST['req']
        except KeyError:
            req = 'new_game'
        if req == 'new_game':
            cards.new_game()
        elif req == 'check_set':
            cards.hint = cards.check_for_set()[0]
            if not cards.hint:
                if len(cards.deck) >= 3:
                    cards.open_extra_cards()
                else:
                    cards.end_game()
                    return redirect(results)
        elif req == 'results':
            return redirect(results)
        elif req == 'back_to_game':
            cards.hint = False
        elif req == 'view_scores':
            return redirect(scores)
        else:
            cards.process_selection(req)
        return HttpResponseRedirect(reverse('game'))
    elif all(card['blank'] for card in cards.cards_open):
        cards.end_game()
        return redirect(results)
    elif cards.results.end_of_game:
        return redirect(results)
    context = {'cards_open': cards.cards_open,
               'hint': cards.hint,
               'row_length': len(cards.cards_open)/3,
               'correct_set_call': cards.correct_set_call}
    return render(request, 'game/game.html', context)


def results(request):
    context = {'results': cards.results.statistics_sets,
               'number_sets_found': cards.results.number_sets_found,
               'end_of_game': cards.results.end_of_game,
               'total_time': cards.results.total_time,
               'average': cards.results.average,
               'hints': cards.results.hints,
               'wrong_sets': cards.results.wrong_sets,
               'score': cards.results.score,
               'status': cards.results.status}
    return render(request, 'game/results.html', context)


def scores(request):
    context = {'stored_results': Highscore.objects.all}
    return render(request, 'game/scores.html', context)
