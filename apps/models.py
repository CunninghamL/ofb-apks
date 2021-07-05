from django.db import models


class Application(models.Model):
    bundle_id = models.CharField(max_length=256, null=True, blank=True)
    app_name = models.CharField(max_length=512, null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.app_name
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class VersionApp(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    file_ipa = models.FileField(upload_to='files/', null=True, blank=True)
    file_plist = models.FileField(upload_to='file_plist/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
