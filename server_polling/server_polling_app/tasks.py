from __future__ import absolute_import, unicode_literals

import time

from celery.utils.log import get_task_logger

from celery import shared_task


@shared_task
def print_message(delay):
    time.sleep(delay)
    print("Message printed after {} seconds".format(delay))
    return "Message printed after {} seconds".format(delay)


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
def calculate_fibonacci(n):
    logger.info('Task started for Fibonacci number {0}'.format(n))
    result = fibonacci(n)
    print("Fibonacci({0}) = {1}".format(n, result))
    logger.info('Task finished for Fibonacci number {0}: {1}'.format(n, result))
    return result
