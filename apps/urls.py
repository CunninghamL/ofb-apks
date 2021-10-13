from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', AppsView.as_view(), name='home'),
    path('app-delete/<int:pk>', AppsDeleteView.as_view(), name='app-delete'),
    path('versions/<int:pk>', AppsVersionView.as_view(), name='versions'),
    path('version-delete/<int:pk>', VersionDeleteView.as_view(), name='version-delete'),
    path('install/<int:pk>', InstallView.as_view(), name='install'),
    path('plist/<int:version_id>', ios_app_plist, name='ios_app_plist'),
    path('upload-file', UploadFileView.as_view(), name='upload-file'),
    path('upload-file/<int:pk>', UploadFileDeleteView.as_view(), name='file-upload-delete'),
    path('upload-file-qrcode/<int:pk>', DownloadByQRCodeView.as_view(), name='file-upload-qrcode'),

    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
