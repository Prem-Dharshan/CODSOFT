from django.utils import timezone
from .models import Task
from django.db.models import Q, Case, When, Value, CharField
from django.contrib.auth import get_user_model
User = get_user_model()

class OverdueTaskMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.now()
        if request.user.is_authenticated is False:
            return self.get_response(request)
        tasks_queryset = Task.objects.filter(user=request.user).filter(Q(status='Pending') | Q(status='Overdue') | Q(status='Completed'))

        tasks_queryset = tasks_queryset.annotate(
            task_status=Case(
                When(dueDate__lt=now, then=Value('Overdue')),
                When(completedDate__isnull=False, then=Value('Completed')),
                default=Value('Pending'),
                output_field=CharField(),
            ),
        )
        for task in tasks_queryset:
            if task.dueDate <= now and task.status != 'Completed':
                task.status = 'Overdue'
                task.save()
            elif task.completedDate is not None:
                task.status = 'Completed'
                task.save()
            else:
                task.status = 'Pending'
                task.save()

        response = self.get_response(request)
        return response