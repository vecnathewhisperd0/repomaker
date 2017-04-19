from django.db.models import Q
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from maker.models import RemoteRepository, App, RemoteApp, ApkPointer
from maker.models.category import Category
from . import BaseModelForm
from .repository import RepositoryAuthorizationMixin


class ApkForm(ModelForm):
    class Meta:
        model = ApkPointer
        fields = ['file']
        labels = {
            'file': _('Select APK file for upload'),
        }


class AppCreateView(RepositoryAuthorizationMixin, CreateView):
    model = ApkPointer
    form_class = ApkForm
    template_name = "maker/app/add.html"

    def get_context_data(self, **kwargs):
        context = super(AppCreateView, self).get_context_data(**kwargs)
        context['repo_id'] = self.kwargs['repo_id']
        context['repos'] = RemoteRepository.objects.filter(users__id=self.request.user.id)
        if 'remote_repo_id' in self.kwargs:
            context['apps'] = RemoteApp.objects.filter(repo__pk=self.kwargs['remote_repo_id'])
        else:
            context['apps'] = RemoteApp.objects.filter(repo__in=context['repos'])
        return context

    def form_valid(self, form):
        form.instance.repo = self.get_repo()
        pointer = form.save()  # needed to save file to disk for scanning
        try:
            pointer.initialize()
        except Exception as e:
            pointer.delete()
            raise e

        if pointer.app.summary != '':  # app did exist already, show it
            return HttpResponseRedirect(reverse('app', args=[pointer.repo.pk, pointer.app.pk]))
        return super(AppCreateView, self).form_valid(form)

    def get_success_url(self):
        # edit new app
        return reverse_lazy('edit_app', kwargs={'repo_id': self.object.repo.pk,
                                                'app_id': self.object.app.pk})


class AppDetailView(RepositoryAuthorizationMixin, DetailView):
    model = App
    pk_url_kwarg = 'app_id'
    context_object_name = 'app'
    template_name = 'maker/app/index.html'

    def get_repo(self):
        return self.get_object().repo

    def get_context_data(self, **kwargs):
        context = super(AppDetailView, self).get_context_data(**kwargs)
        app = context['app']
        if app.name is None or app.name == '':
            raise RuntimeError("App has not been created properly.")
        context['apks'] = ApkPointer.objects.filter(app=app).order_by('-apk__version_code')
        return context


class AppForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        super(AppForm, self).__init__(*args, **kwargs)
        if self.instance.category:
            # Show only own and default categories
            self.fields['category'].queryset = Category.objects.filter(
                Q(user=None) | Q(user=self.instance.repo.user))

    class Meta:
        model = App
        fields = ['summary', 'description', 'website', 'category']


class AppUpdateView(RepositoryAuthorizationMixin, UpdateView):
    model = App
    form_class = AppForm
    pk_url_kwarg = 'app_id'
    template_name = 'maker/app/edit.html'

    def get_repo(self):
        return self.get_object().repo

    def form_valid(self, form):
        result = super(AppUpdateView, self).form_valid(form)
        form.instance.repo.update_async()  # schedule repository update
        return result


class AppDeleteView(RepositoryAuthorizationMixin, DeleteView):
    model = App
    pk_url_kwarg = 'app_id'
    template_name = 'maker/app/delete.html'

    def get_repo(self):
        return self.get_object().repo

    def get_success_url(self):
        return reverse_lazy('repo', kwargs={'repo_id': self.kwargs['repo_id']})
