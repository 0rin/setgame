from django.db import models

class Highscore(models.Model):
    """docstring for List"""
    name = models.CharField(max_length=25)
    total_time = models.FloatField()
    average = models.FloatField()
    hints = models.PositiveIntegerField()
    wrong_sets = models.PositiveIntegerField()
    score = models.FloatField()

    def __str__(self):
        return self.name + ' ' + str(self.score)
