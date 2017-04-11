from django.contrib import admin
from api.models import Snippet, EvaluationResult, EvaluationRunLog, Maze


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'code', 'language', 'get_owner_username')

    def get_owner_username(self, obj):
        return obj.owner.username

    get_owner_username.short_description = 'Owner'
    get_owner_username.admin_order_field = 'owner__username'


@admin.register(EvaluationResult)
class EvaluationResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_snippet_code', 'get_maze', 'steps')

    def get_maze(self, obj):
        return obj.maze.maze

    get_maze.short_description = 'Maze'
    get_maze.admin_order_field = 'maze__maze'

    def get_snippet_code(self, obj):
        return obj.snippet.code

    get_snippet_code.short_description = 'Snippet'
    get_snippet_code.admin_order_field = 'snippet__code'


@admin.register(EvaluationRunLog)
class EvaluationRunLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'started', 'ended', 'mazes_evaluated')


@admin.register(Maze)
class MazeAdmin(admin.ModelAdmin):
    list_display = ('id', 'maze')
