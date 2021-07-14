from django import forms
from ipa import IPAFile
from pyaxmlparser import APK

from apps.constants import TypeApp
from apps.models import Application, VersionApp, UploadFiles


class CreateAppForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = VersionApp
        fields = ['file']

    def save(self, commit=True):
        try:
            file = self.files['file']
            if file.content_type == 'application/vnd.android.package-archive':
                apk = APK(file)
                bundle_id = apk.packagename
                bundle_name = apk.get_app_name()
                version = apk.version_name
                type = TypeApp.ANDROID.value
            else:
                ipa = IPAFile(file)
                bundle_id = ipa.app_info.get('CFBundleIdentifier')
                bundle_name = ipa.get_app_name()
                version = ipa.get_app_version()
                type = TypeApp.IOS.value
            app, is_create = Application.objects.get_or_create(
                bundle_id=bundle_id,
                type=type,
            )
            if is_create:
                app.app_name = bundle_name
                app.save()

            self.instance.application = app
            self.instance.name = bundle_name
            self.instance.version_name = version
            self.instance.file = file
            self.instance.save()
        except:
            pass


class UploadFileForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = UploadFiles
        fields = ['file']

    def save(self, commit=True):
        try:
            file = self.files['file']
            self.instance.file = file
            self.instance.name = file.name
            self.instance.save()
        except:
            pass