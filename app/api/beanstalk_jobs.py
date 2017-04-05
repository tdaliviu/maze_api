import json

import django_beanstalkd
import logging
import requests
from django.conf import settings
from django.utils import timezone

from api.models import EvaluationRunLog, Snippet, Maze, EvaluationResult

logger = logging.getLogger(__name__)


@django_beanstalkd.beanstalk_job
def evaluate(arg):
    # Find last evaluation run
    try:
        last_eval_run_log_date = EvaluationRunLog.objects.latest('started').started
    except EvaluationRunLog.DoesNotExist:
        last_eval_run_log_date = None

    logger.info('Last evaluation started at: {}'.format(last_eval_run_log_date))

    # Set evaluation run started
    started = timezone.now()

    # Select all new snippets since last evaluation
    snippets = Snippet.objects.filter(
        created__gte=last_eval_run_log_date) if last_eval_run_log_date is not None else Snippet.objects.all()

    logger.info('User code snippets found since last evaluation: {}'.format(snippets.count()))

    # Set evaluated mazes counter
    mazes_evaluated = 0

    # Iterate through selected snippets
    for snippet in snippets:
        # Delete snippet evaluation results
        snippet.evaluation_results.all().delete()

        # Iterate through selected mazes
        for maze in Maze.objects.all():
            try:
                # Run user snippet code against maze
                response = requests.post(settings.MAZE_EVALUATION_API_ENDPOINT, json={'maze': json.loads(maze.maze), 'snippet': snippet.code})
                steps = response.json()['steps']
            except Exception as e:
                print(e)
                steps = 0

            # Store evaluation results
            EvaluationResult.objects.create(maze=maze, snippet=snippet, steps=steps)

            # Increment evaluated mazes counter
            mazes_evaluated = mazes_evaluated + 1

    # Set evaluation run ended
    ended = timezone.now()

    # Store evaluation run results
    EvaluationRunLog.objects.create(started=started, ended=ended, mazes_evaluated=mazes_evaluated)
