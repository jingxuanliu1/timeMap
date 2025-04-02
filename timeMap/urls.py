from django.contrib import admin
from django.urls import path, include

def get_urlpatterns():
    return [
        path('admin/', admin.site.urls),
        path('', include('home.urls')),
        path('tasks/', include('tasks.urls')),
        path('accounts/', include('django.contrib.auth.urls')),
    ]

urlpatterns = get_urlpatterns()