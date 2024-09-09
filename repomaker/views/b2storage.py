from django.forms import PasswordInput
from django.utils.translation import ugettext_lazy as _

from ..models.backblaze import B2Storage
from .storage import StorageForm, MainStorageMixin, StorageCreateView, \
    StorageDetailView, StorageUpdateView, StorageDeleteView


class B2StorageForm(StorageForm):

    class Meta(StorageForm.Meta):
        model = B2Storage
        fields = ['bucket', 'account', 'key']
        labels = {
            'bucket': _('Bucket Name'),
            'account': _('Account ID'),
            'key': _('Application Key ID'),
        }

        widgets = {
            'key': PasswordInput(),
        }


class B2ConfigMixin(MainStorageMixin):
    def form_valid(self, form):
        if not form.instance.config_file:
            result = super(B2ConfigMixin, self).form_valid(form)
            form.instance.create_config_file()
            return result
        return super(B2ConfigMixin, self).form_valid(form)


class B2StorageCreate(B2ConfigMixin, StorageCreateView):
    model = B2Storage
    form_class = B2StorageForm


class B2StorageUpdate(B2ConfigMixin, StorageUpdateView):
    model = B2Storage
    form_class = B2StorageForm


class B2StorageDetail(StorageDetailView):
    model = B2Storage
    template_name = 'repomaker/storage/detail_b2.html'


class B2StorageDelete(StorageDeleteView):
    model = B2Storage
