from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', AppsView.as_view(), name='home'),
    path('app-delete/<int:pk>', AppsDeleteView.as_view(), name='app-delete'),
    path('versions/<int:pk>', AppsVersionView.as_view(), name='versions'),
    path('version-delete/<int:pk>', VersionDeleteView.as_view(), name='version-delete'),
    path('install/<int:pk>', InstallView.as_view(), name='install'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
