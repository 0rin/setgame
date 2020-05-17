from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
from .models import Highscore
from .forms import HighscoreForm

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
            cards.reset_timer = False
            cards.hint = cards.check_for_set()[0]
            if not cards.hint:
                if len(cards.deck) >= 3:
                    cards.open_extra_cards()
                else:
                    cards.end_game()
                    return redirect(results)
        elif req == 'results':
            cards.reset_timer = False
            return redirect(results)
        elif req == 'back_to_game':
            cards.reset_timer = False
            cards.hint = False
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
               'correct_set_call': cards.correct_set_call,
               'reset_timer': cards.reset_timer}
    return render(request, 'game/game.html', context)


def results(request):
    if request.method == 'POST':
        req = request.POST['req']
        if req == 'view_scores':
            cards.reset_timer = False
            return redirect(scores)

    context = {'results': cards.results.statistics_sets,
               'number_sets_found': cards.results.number_sets_found,
               'end_of_game': cards.results.end_of_game,
               'total_time': cards.results.total_time,
               'average': cards.results.average,
               'hints': cards.results.hints,
               'wrong_sets': cards.results.wrong_sets,
               'score': cards.results.score,
               'stored': cards.results.stored}
    return render(request, 'game/results.html', context)


def scores(request):
    print('scores, stored:', cards.results.stored)
    score_form = HighscoreForm(request.POST or None)
    if request.method == 'POST':
        if score_form.is_valid():
            data = score_form.cleaned_data
            form_name = data['name']
            form_total_time = data['total_time']
            form_total_time = data['total_time']
            form_average = data['average']
            form_hints = data['hints']
            form_wrong_sets = data['wrong_sets']
            form_score = data['score']
            Highscore.objects.create(name=form_name,
                                     total_time=form_total_time,
                                     average=form_average,
                                     hints=form_hints,
                                     wrong_sets=form_wrong_sets,
                                     score=form_score)
            cards.results.stored = True
        else:
            print(score_form.errors)
    context = {'stored_results': Highscore.objects.order_by('score'),
               'form': score_form}
    return render(request, 'game/scores.html', context)
