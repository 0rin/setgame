from django import forms
from .models import Highscore


class HighscoreForm(forms.ModelForm):
    """docstring for ScoreForm"""
    class Meta:
        model = Highscore
        fields = ['name',
                  'total_time',
                  'average',
                  'hints',
                  'wrong_sets',
                  'score']
