from django.shortcuts import render
# from django.http import HttpResponse
import random


def home(request):
    deck = [{'color': color,
             'shading': shading,
             'range': range(number),
             'number': number,
             'shape': shape} for color in ['red', 'green', 'blue']
                             for number in [1, 2, 3]
                             for shading in ['solid', 'striped', 'open']
                             for shape in ['oval', 'diamond', 'rectangle']]
    random.shuffle(deck)
    setup_cards = [deck.pop() for i in range(12)]
    # return HttpResponse(f"{setup_cards} {len(deck)}")
    return render(request, 'game/home.html', {'setup_cards': setup_cards})
