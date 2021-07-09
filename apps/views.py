from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DetailView
from django.views.generic import ListView, DeleteView

from .form import CreateAppForm
from .models import *


@method_decorator(login_required, name='dispatch')
class AppsVersionView(ListView):
    model = VersionApp
    template_name = 'app_versions.html'
    context_object_name = 'versions_app'

    def get_queryset(self):
        queryset = super(AppsVersionView, self).get_queryset()
        queryset = queryset.filter(application=self.kwargs.get('pk'))
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.save()
        return super(AppsView, self).post(request, args, kwargs)


class AppsDeleteView(DeleteView):
    model = Application
    success_url = '/'

    def get(self, request, *arg, **kwargs):
        return self.post(request, *arg, **kwargs)


class VersionDeleteView(DeleteView):
    model = VersionApp

    def get_success_url(self, **kwargs):
        return reverse_lazy('versions', kwargs={'pk': self.kwargs.get('pk')})

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
        print(context)
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
            version_app.application.app_name
        )
        return HttpResponse(
            plist,
            content_type='text/xml'
        )
