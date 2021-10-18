from builtins import super

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DetailView
from django.views.generic import ListView, DeleteView

from .form import CreateAppForm, UploadFileForm
from .models import *


@method_decorator(login_required, name='dispatch')
class AppsVersionView(ListView):
    model = VersionApp
    template_name = 'app_versions.html'
    context_object_name = 'versions_app'

    def get_queryset(self):
        queryset = super(AppsVersionView, self).get_queryset()
        queryset = queryset.filter(application=self.kwargs.get('pk')).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AppsVersionView, self).get_context_data(**kwargs)
        context['application'] = self.kwargs.get('pk')
        return context


@method_decorator(login_required, name='dispatch')
class AppsView(ListView, FormView):
    model = Application
    form_class = CreateAppForm
    template_name = 'app.html'
    context_object_name = 'apps'
    success_url = '/'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.save()
        self.kwargs['instance'] = form.instance
        return super(AppsView, self).post(request, args, kwargs)

    def get_queryset(self):
        key = self.request.GET.get('key')
        user = self.request.user
        query_set = Application.objects.all().order_by('-updated_at')
        if key:
            query_set = query_set.filter(app_name__icontains=key)
        if user.is_superuser is False:
            query_set = query_set.filter(user_id=user.id)
        return query_set

    def get_success_url(self):
        return reverse_lazy('versions', kwargs={'pk': self.kwargs['instance'].application.id})

    def get_form_kwargs(self):
        kwargs = super(AppsView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AppsView, self).get_context_data(**kwargs)
        context['key_search'] = self.request.GET.get('key', '')
        return context


class AppsDeleteView(DeleteView):
    model = Application
    success_url = '/'

    def get(self, request, *arg, **kwargs):
        return self.post(request, *arg, **kwargs)


class VersionDeleteView(DeleteView):
    model = VersionApp

    def get_success_url(self, **kwargs):
        return reverse_lazy('versions', kwargs={'pk': self.object.application_id})

    def get(self, request, *arg, **kwargs):
        return self.post(request, *arg, **kwargs)


class InstallView(DetailView):
    model = VersionApp
    template_name = 'install.html'
    context_object_name = 'version'

    def get_context_data(self, **kwargs):
        context = super(InstallView, self).get_context_data(**kwargs)
        link_file = None
        file = context['version'].file
        if file and hasattr(file, 'url'):
            link_file = self.request.build_absolute_uri(context['version'].file.url)
        context['link_file'] = link_file
        context['is_login'] = False
        return context


def ios_app_plist(request, version_id):
    version_app = VersionApp.objects.filter(id=version_id).first()
    if version_app:
        f = open("templates/auto_file.plist", "r")
        plist = f.read()
        plist = plist.format(
            request.build_absolute_uri(version_app.file.url),
            version_app.application.bundle_id,
            version_app.version_name,
            version_app.name or version_app.application.app_name
        )
        return HttpResponse(
            plist,
            content_type='text/xml'
        )


class UploadFileView(FormView, ListView):
    model = UploadFiles
    form_class = UploadFileForm
    template_name = 'upload_file.html'
    context_object_name = 'files'
    success_url = '/upload-file'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.save()
        return super().post(request, args, kwargs)

    def get_queryset(self):
        key = self.request.GET.get('key')
        user = self.request.user
        query_set = UploadFiles.objects.all().order_by('-created_at')
        if key:
            query_set = query_set.filter(name__icontains=key)
        if user.is_superuser is False:
            query_set = query_set.filter(user_id=user.id)
        return query_set

    def get_form_kwargs(self):
        kwargs = super(UploadFileView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UploadFileView, self).get_context_data(**kwargs)
        context['key_search'] = self.request.GET.get('key', '')
        return context


class UploadFileDeleteView(DeleteView):
    model = UploadFiles

    def get_success_url(self, **kwargs):
        return reverse_lazy('upload-file')

    def get(self, request, *arg, **kwargs):
        return self.post(request, *arg, **kwargs)


class DownloadByQRCodeView(DetailView):
    model = UploadFiles
    template_name = 'upload_qrcode.html'
    context_object_name = 'file_qrcode'

    def get_context_data(self, **kwargs):
        context = super(DownloadByQRCodeView, self).get_context_data(**kwargs)
        link_file = None
        file = context['file_qrcode'].file
        if file and hasattr(file, 'url'):
            link_file = self.request.build_absolute_uri(context['file_qrcode'].file.url)
        context['link_file'] = link_file
        context['is_login'] = False
        return context
