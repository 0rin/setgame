from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .game import Game
from .models import Highscore
from .forms import HighscoreForm

game = Game()


def play(request):
    """Handle logic related to playing the game."""
    url_direction = ''
    if request.method == 'POST':
        url_direction = _play_post(request.POST['req'])
    elif game.no_cards_left() or url_direction == 'results':
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


def _play_post(req):
    """Handle logic of POST request to play-view"""
    url_direction = ''
    if req == 'new_game':
        game.new_game()
    elif req == 'try_find_set':
        url_direction = game.process_set_existence_doubt()
    elif req == 'refused_hint':
        game.refused_hint()
    elif req == 'results':
        game.results.add_time_interval()
        url_direction = 'result'
    else:
        game.process_selection(req)
    return url_direction


def results(request):
    """Handle user requests on results page, like fetching data."""
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
    """Handle user requests about scores."""
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
