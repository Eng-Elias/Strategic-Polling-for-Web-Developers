from __future__ import absolute_import, unicode_literals

import time

from celery.utils.log import get_task_logger

from celery import shared_task


@shared_task
def print_message(delay):
    time.sleep(delay)
    print("Message printed after {} seconds".format(delay))


@shared_task
def time_consuming_task():
    # Simulate a time-consuming task
    time.sleep(10)
    return "Task completed successfully"


logger = get_task_logger(__name__)


def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@shared_task(bind=True)
def calculate_fibonacci(self, n):
    logger.info('Task {0} started for Fibonacci number {1}'.format(self.request.id, n))
    result = fibonacci(n)
    logger.info('Task {0} finished for Fibonacci number {1}: {2}'.format(self.request.id, n, result))
    return result
