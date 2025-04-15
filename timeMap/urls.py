from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def get_urlpatterns():
    return [
        path('admin/', admin.site.urls),
        path('', include('home.urls')),
        path('tasks/', include('tasks.urls')),
        path('accounts/', include('django.contrib.auth.urls')),
        path('notifications/', include('notifications.urls')),

    ]

urlpatterns = get_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])