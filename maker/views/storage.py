from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .repository import RepositoryAuthorizationMixin


class StorageCreateView(RepositoryAuthorizationMixin, CreateView):
    template_name = 'maker/storage/form.html'

    def get_context_data(self, **kwargs):
        context = super(StorageCreateView, self).get_context_data(**kwargs)
        context['storage_name'] = self.model.get_name()
        return context

    def form_valid(self, form):
        form.instance.repo = self.get_repo()
        return super(StorageCreateView, self).form_valid(form)

    def get_success_url(self):
        self.get_repo().update_async()
        return get_success_url(self)


class StorageUpdateView(RepositoryAuthorizationMixin, UpdateView):
    template_name = 'maker/storage/form.html'

    def get_context_data(self, **kwargs):
        context = super(StorageUpdateView, self).get_context_data(**kwargs)
        context['storage_name'] = self.model.get_name()
        return context

    def get_success_url(self):
        self.get_repo().update_async()
        return get_success_url(self)


class StorageDeleteView(RepositoryAuthorizationMixin, DeleteView):
    template_name = 'maker/storage/delete.html'

    def get_success_url(self):
        return get_success_url(self)


def get_success_url(view):
    return reverse_lazy('repo', kwargs={'repo_id': view.kwargs['repo_id']})
