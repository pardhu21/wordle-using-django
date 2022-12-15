from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.word