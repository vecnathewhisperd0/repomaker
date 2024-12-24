import fdroidserver
import logging
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .storage import AbstractStorage
from repomaker.storage import get_identity_file_path, PrivateStorage, REPO_DIR


class RcloneStorage(AbstractStorage):
    bucket = models.CharField(max_length=128)
    rclone_config = models.CharField(max_length=32)
    endpoint = models.CharField(max_length=100)
    rclone_config_text_field = models.TextField()
    config_file = models.FileField(upload_to=get_identity_file_path,
                                   storage=PrivateStorage(),
                                   blank=True)

    add_url_name = 'storage_rclone_add'
    detail_url_name = 'storage_rclone'
    edit_url_name = 'storage_rclone_update'
    delete_url_name = 'storage_rclone_delete'

    def __str__(self):
        return str(self.endpoint) + "/" + str(self.bucket)

    @staticmethod
    def get_name():
        return _("Rclone Supported Storage")

    def get_url(self):
        return str(self.endpoint) + "/" + str(self.bucket)

    def get_repo_url(self):
        return self.get_url() + "/fdroid/" + REPO_DIR

    def create_config_file(self):
        #  use config and rclone config to create small config
        #  else create config from rclone configs above
        self.config_file.save(
            'id_%d' %
            self.pk +
            '.conf',
            ContentFile(
                self.rclone_config_text_field))

    def publish(self):
        logging.info("Publishing '%s' to %s", self.repo, self)
        rclone_config_path = os.path.join(
            settings.PRIVATE_REPO_ROOT, self.config_file.name)
        config = self.repo.get_config()
        config['rclone'] = True
        config['awsbucket'] = self.bucket
        config['rclone_config'] = self.rclone_config
        config['path_to_custom_rclone_config'] = rclone_config_path
        fdroidserver.deploy.update_remote_storage_with_rclone(REPO_DIR)
