from django.contrib.auth.models import User
from django.db import models


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    language = models.CharField(default='python', max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')

    class Meta:
        ordering = ('created',)


class Maze(models.Model):
    maze = models.TextField()


class EvaluationResult(models.Model):
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='snippets')
    maze = models.ForeignKey(Maze, on_delete=models.CASCADE, related_name='mazes')
    steps = models.IntegerField(default=0)  # 0 stands for 'did not finish maze' (i.e. timeout)


class EvaluationRunLog(models.Model):
    started = models.DateTimeField()
    ended = models.DateTimeField(null=True)
    mazes_evaluated = models.IntegerField(default=0)
