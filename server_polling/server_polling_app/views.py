from django.shortcuts import render
from django_celery_results.models import TaskResult
from rest_framework.decorators import api_view
from rest_framework.response import Response
from server_polling_app.tasks import (
    print_message,
    run_n_queen_task,
    time_consuming_task,
)
from django.http import JsonResponse


@api_view(["POST"])
def run_simple_task(request):
    delay = int(request.data.get("delay", 5))  # Default delay is 5 seconds
    task = print_message.apply_async(args=[delay])
    return Response({"task_id": task.id}, status=202)


@api_view(["POST"])
def long_polling_view(request):
    try:
        # Initiate the time-consuming Celery task
        task = time_consuming_task.apply_async()
        # Hold the response until the task is completed
        task_result = task.get()
        return Response(task_result)
    except Exception as e:
        return JsonResponse({"error": str(e)})


@api_view(["POST"])
def run_celery_task(request):
    n = int(request.data.get("n", 8))  # Default number of queens is 8

    # Run Celery task
    task = run_n_queen_task.apply_async(args=[n])
    task_id = task.id

    return Response({"task_id": task_id})


@api_view(["GET"])
def check_task_result(request, task_id):
    task_result = TaskResult.objects.filter(task_id=task_id).first()
    if task_result:
        status = task_result.status
        result = task_result.result
    else:
        status = "PENDING"
        result = None
    return Response({"task_id": task_id, "status": status, "result": result})


def render_home_page(request):
    return render(request, "home.html")
