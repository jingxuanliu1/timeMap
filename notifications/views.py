
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import NotificationSetting
from tasks.forms import TaskForm


@login_required
def notification_settings(request):
    try:
        setting = NotificationSetting.objects.get(user=request.user)
    except NotificationSetting.DoesNotExist:
        setting = NotificationSetting(user=request.user)

    if request.method == 'POST':
        form = NotificationSettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('notifications:notification_settings')
    else:
        form = NotificationSettingForm(instance=setting)

    return render(request, 'notifications/notification_settings.html', {
        'form': form,
        'title': 'Notification Settings'
    })
