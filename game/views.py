from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .game import Game
from .models import Highscore
from .forms import HighscoreForm
from datetime import datetime

game = Game()


def play(request):
    if request.method == 'POST':
        try:
            req = request.POST['req']
        except KeyError:
            req = 'new_game'
        if req == 'new_game':
            game.new_game()
        elif req == 'find_set':
            game.hint = game.find_set()[0]
            if not game.hint:
                if len(game.deck) >= 3:
                    game.open_extra_cards()
                else:
                    game.end_game()
                    return redirect(results)
        elif req == 'refused_hint':
            game.results.hints -= 1
            game.hint = False
        elif req == 'results':
            game.results.add_time_interval()
            return redirect(results)
        else:
            game.process_selection(req)
        return HttpResponseRedirect(reverse('play'))
    elif all(card['blank'] for card in game.cards_open):
        game.end_game()
        return redirect(results)
    elif game.results.end_of_game:
        return redirect(results)
    context = {'cards_open': game.cards_open,
               'hint': game.hint,
               'row_length': len(game.cards_open)/3,
               'correct_set_call': game.correct_set_call,
               'number_sets_found': game.results.number_sets_found}
    return render(request, 'game/game.html', context)


def results(request):
    if request.method == 'POST':
        req = request.POST['req']
        if req == 'view_scores':
            return redirect(scores)
        elif req == 'back_to_game':
            game.hint = False
            game.results.start_time = datetime.now()
            return redirect(play)
    context = {'results': game.results.statistics_sets,
               'number_sets_found': game.results.number_sets_found,
               'end_of_game': game.results.end_of_game,
               'total_time': game.results.total_time,
               'average': game.results.average,
               'hints': game.results.hints,
               'wrong_sets': game.results.wrong_sets,
               'score': game.results.score,
               'stored': game.results.stored}
    return render(request, 'game/results.html', context)


def scores(request):
    score_form = HighscoreForm(request.POST or None)
    if request.method == 'POST':
        if score_form.is_valid():
            data = score_form.cleaned_data
            form_name = data['name']
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
            game.results.stored = True
        return HttpResponseRedirect(reverse('scores'))
    context = {'stored_results': Highscore.objects.order_by('score'),
               'form': score_form}
    return render(request, 'game/scores.html', context)
