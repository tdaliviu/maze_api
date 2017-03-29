from django.db import models


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    language = models.CharField(default='python', max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
