from django.db import models


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    language = models.CharField(default='python', max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)


class Maze(models.Model):
    maze = models.TextField()


class EvaluationResult(models.Model):
    snippet = models.ForeignKey('api.Snippet', on_delete=models.CASCADE)
    maze = models.ForeignKey('api.Maze', on_delete=models.CASCADE)
    steps = models.IntegerField(default=0)  # 0 stands for 'did not finish maze' (i.e. timeout)


class EvaluationRunLog(models.Model):
    started = models.DateTimeField()
    ended = models.DateTimeField(null=True)
    mazes_evaluated = models.IntegerField(default=0)
