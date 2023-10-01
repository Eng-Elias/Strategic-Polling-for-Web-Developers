from django.urls import path
from .views import run_simple_task, get_simple_task_result, long_polling_view, run_celery_task, check_task_result


urlpatterns = [
    path('run_simple_task/', run_simple_task, name='run_simple_task'),
    path('simple_task_result/<str:task_id>/', get_simple_task_result, name='get_simple_task_result'),
    path('long_polling/', long_polling_view, name='long_polling'),
    path('run_celery_task/', run_celery_task, name='run_celery_task'),
    path('check_task_result/<str:task_id>/', check_task_result, name='check_task_result'),
]
