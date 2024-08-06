import time
from celery.utils.log import get_task_logger
from celery import shared_task


logger = get_task_logger(__name__)


@shared_task
def time_consuming_task(*args, **kwargs):
    # Simulate a time-consuming task
    time.sleep(5)
    return "Task completed successfully"


@shared_task
def print_message(delay, *args, **kwargs):
    time.sleep(delay)
    result = "Message printed after {} seconds".format(delay)
    print(result)
    return result


def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@shared_task(bind=True)
def calculate_fibonacci(self, n, *args, **kwargs):
    logger.info("Task started for Fibonacci number {0}".format(n))
    result = fibonacci(n)
    logger.info("Task finished for Fibonacci number {0}: {1}".format(n, result))
    return result
