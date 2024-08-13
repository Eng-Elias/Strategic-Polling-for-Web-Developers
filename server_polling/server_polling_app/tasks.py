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


def solve_n_queens(n):
    def is_safe(board, row, col):
        for i in range(row):
            if (
                board[i] == col
                or board[i] - i == col - row
                or board[i] + i == col + row
            ):
                return False
        return True

    def solve(board, row):
        if row == n:
            result.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve(board, row + 1)

    result = []
    solve([-1] * n, 0)
    return result


@shared_task(bind=True)
def run_n_queen_task(task, n, *args, **kwargs):
    logger.info("Task started for {0} queens".format(n))
    results = solve_n_queens(n)
    # text_result = "\n".join([str(result) for result in results])
    # logger.info("Task finished for {0} queens: {1}".format(n, text_result))
    return results
