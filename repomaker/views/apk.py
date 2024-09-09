from django.forms import FileField, ClearableFileInput, ImageField
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

from repomaker.models import Apk, ApkPointer
from . import BaseModelForm
from .repository import RepositoryAuthorizationMixin, ApkUploadMixin


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultipleImageField(ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ApkForm(BaseModelForm):
    #  apks = FileField(required=False, widget=ClearableFileInput(attrs={'multiple': True}))
    apks = MultipleFileField(required=False)

    class Meta:
        model = Apk
        fields = ['apks']


class ApkUploadView(ApkUploadMixin, UpdateView):
    object = None
    form_class = ApkForm
    template_name = "repomaker/error.html"

    def get(self, request, *args, **kwargs):
        # don't answer GET requests
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if not form.is_valid():
            return self.form_invalid(form)

        # add posted APKs
        added_apks = self.add_apks()
        if len(added_apks['failed']) > 0:
            form.add_error('apks', self.get_error_msg(added_apks['failed']))
            return super(ApkUploadView, self).form_invalid(form)

        # don't let the View create anything as we already did
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('repo', args=[self.get_repo().pk])


class ApkPointerDeleteView(RepositoryAuthorizationMixin, DeleteView):
    model = ApkPointer
    template_name = 'repomaker/app/apk_delete.html'
    pk_url_kwarg = 'pk'

    def get_repo(self):
        return self.get_object().app.repo

    def get_success_url(self):
        self.get_repo().update_async()
        return self.get_object().app.get_edit_url()
