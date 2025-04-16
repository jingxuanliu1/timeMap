from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Home app URLs
    #path('tasks/', include('tasks.urls', namespace='tasks')),  # This line is crucial
    path('tasks/', include('tasks.urls')),  # Tasks app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('profiles/', include('profiles.urls')),  # Profiles app URLs
]

# Static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)