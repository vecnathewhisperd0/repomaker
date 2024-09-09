import configparser
import io
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _

from ..models.rclonesupportedstorage import RcloneStorage
from .storage import StorageForm, MainStorageMixin, StorageCreateView, \
    StorageDetailView, StorageUpdateView, StorageDeleteView


class RcloneStorageForm(StorageForm):
    class Meta(StorageForm.Meta):
        model = RcloneStorage
        fields = [
            "bucket",
            "endpoint",
            "rclone_config",
            "rclone_config_text_field"]
        labels = {
            "bucket": _("Bucket Name / Folder Name"),
            "endpoint": _("Endpoint / host url"),
            "rclone_config": _("Rclone Config to use in uploaded config"),
            "rclone_config_text_field": _("Rclone config text field"),
        }

        widgets = {
            "rclone_config_text_field": Textarea(),
        }


class RcloneStorageMixin(MainStorageMixin):
    def form_valid(self, form):
        #  Add validation logic here to parse config string
        #  check that rclone_config_text_field is a config
        config = configparser.ConfigParser()
        buff_str = io.StringIO(form.cleaned_data['rclone_config_text_field'])
        try:
            config.read_file(buff_str)
        except Exception:
            form.add_error(
                'rclone_config_text_field',
                _("Incorrect rclone configuration. Try again.")
            )
            return self.form_invalid(form)

        #  remove last slash in endpoint url
        if form.cleaned_data['endpoint'].endswith("/"):
            form.add_error('endpoint', _("Remove slash at the end."))
            return self.form_invalid(form)

        #  check if config is in rclone config
        if form.cleaned_data['rclone_config'] not in config:
            form.add_error(
                'rclone_config',
                _("Your rclone config does not exist in the pasted config."))
            return self.form_invalid(form)

        #  create rclone config file
        if not form.instance.config_file:
            result = super(RcloneStorageMixin, self).form_valid(form)
            form.instance.create_config_file()
            return result
        return super(RcloneStorageMixin, self).form_valid(form)


class RcloneStorageCreate(RcloneStorageMixin, StorageCreateView):
    model = RcloneStorage
    form_class = RcloneStorageForm


class RcloneStorageUpdate(RcloneStorageMixin, StorageUpdateView):
    model = RcloneStorage
    form_class = RcloneStorageForm


class RcloneStorageDetail(StorageDetailView):
    model = RcloneStorage
    template_name = 'repomaker/storage/detail_rclone_service.html'


class RcloneStorageDelete(StorageDeleteView):
    model = RcloneStorage
