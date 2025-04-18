from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Task
from .forms import TaskForm
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse

# View to display all tasks
@login_required
def index(request):
    # Get both selected_date and start_date from parameters
    selected_date_str = request.GET.get('selected_date')
    start_date_str = request.GET.get('start_date')  # Remove fallback to selected_date_str

    # Parse selected_date with timezone awareness
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        selected_date = timezone.make_aware(datetime.combine(selected_date, datetime.min.time())).date()
    except (ValueError, TypeError):
        selected_date = timezone.localdate()
    tasks = Task.objects.filter(user=request.user).order_by('start_time')  # Get tasks for the logged-in user
    completed_count = Task.objects.filter(user=request.user).filter(completed=True).count()

    # Parse start_date, default to today
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time())).date()
    except (ValueError, TypeError):
        start_date = timezone.localdate()  # Default to today, not selected_date

    # Generate 7 days from start_date
    days = [{
        'day_name': (start_date + timedelta(days=i)).strftime('%a'),
        'day_number': (start_date + timedelta(days=i)).day,
        'date_str': (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
    } for i in range(7)]

    # Filter tasks
    tasks = Task.objects.filter(
        user=request.user,
        start_time__date=selected_date
    ).order_by('start_time')

    return render(request, 'tasks/index.html', {
        'tasks': tasks,
        'days': days,
        'selected_date': selected_date.strftime('%Y-%m-%d'),
        'start_date': start_date.strftime('%Y-%m-%d'),
        'display_date': f"{selected_date.strftime('%B')} {selected_date.day}, {selected_date.year}",
        'completed_count': completed_count
    })

# View to create a new task
@login_required
@login_required
@login_required
def create_task(request):
    selected_date = request.GET.get('selected_date', '')
    start_date = request.GET.get('start_date', timezone.localdate().strftime('%Y-%m-%d'))

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.latitude = form.cleaned_data.get('latitude')
            task.longitude = form.cleaned_data.get('longitude')
            task.latitude2 = form.cleaned_data.get('latitude2')
            task.longitude2 = form.cleaned_data.get('longitude2')
            task.notify_before = int(form.cleaned_data['notify_before']) if form.cleaned_data['notify_before'] else None
            task.save()

            # 🔁 사용자 지정 반복 횟수 적용
            repeat_count = form.cleaned_data.get('repeat_count') or 0
            if task.recur in ['daily', 'weekly', 'monthly'] and repeat_count > 0:
                generate_recurring_tasks(task, count=repeat_count)

            return redirect(
                f"{reverse('tasks:index')}?selected_date={request.POST.get('selected_date', '')}&start_date={start_date}"
            )
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'selected_date': selected_date,
        'start_date': start_date
    })


def generate_recurring_tasks(task, count=5):
    occurrences = {
        'daily': lambda n: task.start_time + timedelta(days=n),
        'weekly': lambda n: task.start_time + timedelta(weeks=n),
        'monthly': lambda n: task.start_time + timedelta(days=30 * n),
    }

    recur_type = task.recur
    if recur_type not in occurrences:
        return

    for i in range(1, count + 1):
        Task.objects.create(
            user=task.user,
            title=task.title,
            description=task.description,
            location=task.location,
            start_location=task.start_location,
            start_time=occurrences[recur_type](i),
            end_time=occurrences[recur_type](i) + (task.end_time - task.start_time),
            completed=False,
            notify_before=task.notify_before,
            latitude=task.latitude,
            longitude=task.longitude,
            latitude2=task.latitude2,
            longitude2=task.longitude2,
            recur='none',  # 생성된 task는 반복하지 않음
        )


@login_required
@login_required
def update_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    selected_date = request.GET.get('selected_date', timezone.localdate().strftime('%Y-%m-%d'))
    start_date = request.GET.get('start_date', timezone.localdate().strftime('%Y-%m-%d'))

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.notify_before = int(form.cleaned_data['notify_before']) if form.cleaned_data['notify_before'] else None

            task.latitude = form.cleaned_data.get('latitude')
            task.longitude = form.cleaned_data.get('longitude')
            task.latitude2 = form.cleaned_data.get('latitude2')
            task.longitude2 = form.cleaned_data.get('longitude2')

            task.save()

            # ✅ 기존 반복 task 삭제 (recur='none' && title+timespan이 같은 future task)
            Task.objects.filter(
                user=task.user,
                title=task.title,
                recur='none',
                start_time__gt=task.start_time
            ).delete()

            # ✅ 새로운 반복 task 생성
            repeat_count = form.cleaned_data.get('repeat_count') or 0
            if task.recur in ['daily', 'weekly', 'monthly'] and repeat_count > 0:
                generate_recurring_tasks(task, count=repeat_count)

            return redirect(f"{reverse('tasks:index')}?selected_date={selected_date}&start_date={start_date}")
        else:
            print(form.errors)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/update_task.html', {
        'form': form,
        'task': task,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'selected_date': selected_date,
        'start_date': start_date
    })


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    selected_date = request.GET.get('selected_date', '')
    start_date = request.GET.get('start_date', timezone.localdate().strftime('%Y-%m-%d'))
    task.delete()
    return redirect(f"{reverse('tasks:index')}?selected_date={selected_date}&start_date={start_date}")
