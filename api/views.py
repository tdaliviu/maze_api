import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Max, Case, When, Value, IntegerField, F
from django.utils import timezone
from requests.exceptions import Timeout
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_expiring_authtoken import authentication

from api.models import EvaluationResult, Maze, EvaluationRunLog, Snippet
from api.serializers import UserSerializer, SnippetSerializer, OverallScoreboardSerializer


class UserList(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetList(APIView):
    authentication_classes = (authentication.ExpiringTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            snippet = request.user.snippets.first()
        except User.DoesNotExist:
            snippet = None

        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.snippets.all().count() > 0:
            return Response('User already has a submitted code snippet. Use PUT to update', status=status.HTTP_400_BAD_REQUEST)

        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            # Find last evaluation run
            try:
                last_eval_run_log_date = EvaluationRunLog.objects.latest('ended').ended
            except EvaluationRunLog.DoesNotExist:
                last_eval_run_log_date = None

            # Select all new snippets since last evaluation
            snippets = Snippet.objects.filter(
                created__gte=last_eval_run_log_date) if last_eval_run_log_date is not None else Snippet.objects.all()

            # Select all mazes
            mazes = Maze.objects.all()

            # Set evaluation run started
            started = timezone.now()

            # Set evaluated mazes counter
            mazes_evaluated = 0

            # Iterate through selected snippets
            for snippet in snippets:
                # Delete snippet evaluation results
                snippet.evaluation_results.all().delete()

                # Iterate through selected mazes
                for maze in mazes:
                    try:
                        # Run user snippet code against maze
                        response = requests.post(settings.MAZE_EVALUATION_API_ENDPOINT, json={'maze': maze, 'snippet': snippet.code})
                        steps = response.json()['steps']
                    except (Timeout, KeyError):  # HTTP request has timed out or the result JSON does not contain 'steps'
                        steps = 0

                    # Store evaluation results
                    EvaluationResult.objects.create(maze=maze, snippet=snippet, steps=steps)

                    # Increment evaluated mazes counter
                    mazes_evaluated = mazes_evaluated + 1

            # Set evaluation run ended
            ended = timezone.now()

            # Store evaluation run results
            EvaluationRunLog.objects.create(started=started, ended=ended, mazes_evaluated=mazes_evaluated)

            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            snippet = request.user.snippets.first()
        except User.DoesNotExist:
            return Response('User has no code snippet submitted. Use POST to submit', status=status.HTTP_400_BAD_REQUEST)

        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScoreList(APIView):
    def get(self, request, format=None):
        maze_scoreboard = []
        maze_list = Maze.objects.values('id')

        for maze in maze_list:
            queryset = EvaluationResult.objects.filter(maze_id=maze['id']) \
                .annotate(username=F('snippet__owner__username')) \
                .values('username', 'steps')
            max_steps = queryset.aggregate(Max('steps'))['steps__max']
            evaluation_results = queryset \
                .annotate(steps_replace=Case(When(steps=0, then=Value(max_steps + 1)), default=F('steps'),
                                             output_field=IntegerField())) \
                .order_by('steps_replace')

            maze_rank = 1
            for i in range(0, len(evaluation_results)):
                maze_rank_record = {'username': evaluation_results[i]['username'],
                                    'maze_rank': maze_rank,
                                    'maze_id': maze['id']}
                maze_scoreboard.append(maze_rank_record)
                if i + 1 < len(evaluation_results) and evaluation_results[i + 1]['steps_replace'] != \
                        evaluation_results[i]['steps_replace']:
                    maze_rank = maze_rank + 1

        users = list(set(map(lambda scoreboard_record: scoreboard_record['username'], maze_scoreboard)))
        user_maze_rank_sums = sorted(map(lambda user: {'username': user, 'maze_rank_sum': reduce(lambda accum_value, x: accum_value + x['maze_rank'], filter(lambda scoreboard_record: scoreboard_record['username'] == user, maze_scoreboard), 0)}, users), key=lambda sum_: sum_['maze_rank_sum'])

        overall_scoreboard = []
        overall_rank = 1
        for i in range(0, len(user_maze_rank_sums)):
            user = User.objects.get(username=user_maze_rank_sums[i]['username'])
            overall_rank_record = {'username': user_maze_rank_sums[i]['username'],
                                   'first_name': user.first_name,
                                   'last_name': user.last_name,
                                   'rank': overall_rank}
            overall_scoreboard.append(overall_rank_record)
            if i + 1 < len(user_maze_rank_sums) and user_maze_rank_sums[i + 1]['maze_rank_sum'] != user_maze_rank_sums[i]['maze_rank_sum']:
                overall_rank = overall_rank + 1

        serializer = OverallScoreboardSerializer(data=overall_scoreboard, many=True)

        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)