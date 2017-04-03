import os
import sys

import django

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'maze_eval.settings'

parent_dir = os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), os.pardir))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

django.setup()

import json
import signal
from contextlib import contextmanager
from django.utils import timezone

from pymaze import Maze

from api.models import Snippet, EvaluationRunLog, Maze as Maze_, EvaluationResult


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise (TimeoutException("Timed out!"))

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def evaluate_snippets():
    # Find last evaluation run
    try:
        last_eval_run_log_date = EvaluationRunLog.objects.latest('ended').ended
    except EvaluationRunLog.DoesNotExist:
        last_eval_run_log_date = None

    # Select all new snippets since last evaluation
    snippets = Snippet.objects.filter(created__gte=last_eval_run_log_date) if last_eval_run_log_date is not None else Snippet.objects.all()

    # Select all mazes
    mazes = Maze_.objects.all()

    # Set evaluation run started
    started = timezone.now()

    # Set evaluated mazes counter
    mazes_evaluated = 0

    # Iterate through selected snippets
    for snippet in snippets:
        # Iterate through selected mazes
        for maze_ in mazes:
            try:
                with time_limit(60):
                    # Run snippet code against maze
                    maze = Maze(json.loads(maze_.maze))

                    exec snippet.code

                    # Get step count
                    steps = len(maze.get_history()) - 1 if maze.is_maze_solved() else 0
            except TimeoutException, msg:
                steps = 0

            # Store evaluation results
            EvaluationResult.objects.create(maze=maze_, snippet=snippet, steps=steps)

            # Increment evaluated mazes counter
            mazes_evaluated = mazes_evaluated + 1

    # Set evaluation run ended
    ended = timezone.now()

    # Store evaluation run results
    EvaluationRunLog.objects.create(started=started, ended=ended, mazes_evaluated=mazes_evaluated)


if __name__ == '__main__':
    evaluate_snippets()
