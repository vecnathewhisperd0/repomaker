from django.forms import PasswordInput
from django.utils.translation import ugettext_lazy as _

from ..models.filebase import FilebaseStorage
from .storage import StorageForm, MainStorageMixin, StorageCreateView, \
    StorageDetailView, StorageUpdateView, StorageDeleteView


class FilebaseStorageForm(StorageForm):

    class Meta(StorageForm.Meta):
        model = FilebaseStorage
        fields = ["bucket", "access_key_id", "secret_access_key"]
        labels = {
            "bucket": _("Bucket Name"),
            "access_key_id": _("Access Key ID"),
            "secret_access_key": _("Secret Access Key"),
        }

        widgets = {
            "secret_access_key": PasswordInput(),
        }


class FilebaseConfigMixin(MainStorageMixin):
    def form_valid(self, form):
        if not form.instance.config_file:
            result = super(FilebaseConfigMixin, self).form_valid(form)
            form.instance.create_config_file()
            return result
        return super(FilebaseConfigMixin, self).form_valid(form)


class FilebaseStorageCreate(FilebaseConfigMixin, StorageCreateView):
    model = FilebaseStorage
    form_class = FilebaseStorageForm


class FilebaseStorageUpdate(FilebaseConfigMixin, StorageUpdateView):
    model = FilebaseStorage
    form_class = FilebaseStorageForm


class FilebaseStorageDetail(StorageDetailView):
    model = FilebaseStorage
    template_name = 'repomaker/storage/detail_filebase.html'


class FilebaseStorageDelete(StorageDeleteView):
    model = FilebaseStorage
