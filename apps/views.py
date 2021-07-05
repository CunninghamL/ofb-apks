from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .models import *


class AppsVersionView(CreateView, ListView):
    model = VersionApp
    fields = ('file_ipa',)
    template_name = 'app_versions.html'
    context_object_name = 'versions_app'

    def get_success_url(self, **kwargs):
        return reverse_lazy('versions', kwargs={'pk': self.kwargs.get('pk')})
        
    def get_object(self, queryset=None):
        return VersionApp.objects.filter(application=self.request.GET.get('pk'))

    def form_valid(self, form):
        form.instance.application_id = self.kwargs.get('pk')
        return super(AppsVersionView, self).form_valid(form)
    
    def post(self, request, *args, **kwargs):
        return super(AppsVersionView, self).post(request, **kwargs)
        # return VersionApp.objects.create(
        #     application_id=self.kwargs.get('pk'),
        #     file_ipa=request.POST.get("file_ipa"),
        # )

    def get_context_data(self, **kwargs):
        context = super(AppsVersionView, self).get_context_data(**kwargs)
        
        context['application'] = self.kwargs.get('pk')
        # context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
        return context


class AppsView(CreateView, ListView):
    model = Application
    fields = ('bundle_id', 'app_name')
    template_name = 'app.html'
    context_object_name = 'apps'
    success_url = '/'


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
    
    
class InstallView(ListView):
    model = VersionApp
    template_name = 'install.html'
    context_object_name = 'version'

    def get_object(self, queryset=None):
        return VersionApp.objects.get(application=self.request.GET.get('pk'))