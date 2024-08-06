from django.shortcuts import render
from django_celery_results.models import TaskResult
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import print_message, time_consuming_task, calculate_fibonacci
from django.http import JsonResponse


@api_view(['POST'])
def run_simple_task(request):
    delay = request.data.get('delay', 5)  # Default delay is 5 seconds
    task = print_message.apply_async(args=[delay])
    return Response({'task_id': task.id}, status=202)


@api_view(['POST'])
def long_polling_view(request):
    try:
        # Initiate the time-consuming Celery task
        task = time_consuming_task.apply_async()
        # Hold the response until the task is completed
        task_result = task.get()
        print(type(task_result))
        return Response(task_result)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@api_view(['POST'])
def run_celery_task(request):
    n = int(request.POST.get('n', 10))  # Default Fibonacci number is 10

    # Run the Celery task
    task = calculate_fibonacci.apply_async(args=[n])
    task_id = task.id

    return Response({'task_id': task_id})


@api_view(['GET'])
def check_task_result(request, task_id):
    task_result = TaskResult.objects.filter(task_id=task_id).first()
    if task_result:
        status = task_result.status
        result = task_result.result
    else:
        status = 'PENDING'
        result = None
    return Response({'task_id': task_id, 'status': status, 'result': result})


def render_home_page(request):
    return render(request, 'home.html')
