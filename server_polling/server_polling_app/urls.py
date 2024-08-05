from django.urls import path
import server_polling_app.views as views


urlpatterns = [
    path('run_simple_task/', views.run_simple_task, name='run_simple_task'),
    path('long_polling/', views.long_polling_view, name='long_polling'),
    path('run_celery_task/', views.run_celery_task, name='run_celery_task'),
    path('check_task_result/<str:task_id>/', views.check_task_result, name='check_task_result'),
]
