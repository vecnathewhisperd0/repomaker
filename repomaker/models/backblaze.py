import configparser
import fdroidserver
import logging
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .storage import AbstractStorage
from repomaker.storage import get_identity_file_path, PrivateStorage, REPO_DIR

B2_CONFIG_NAME = "b2-config.conf"


class B2Storage(AbstractStorage):
    type = models.CharField(max_length=32, default='b2', editable=False)
    account = models.CharField(max_length=128)
    key = models.CharField(max_length=255)
    bucket = models.CharField(max_length=128)
    config_file = models.FileField(upload_to=get_identity_file_path,
                                   storage=PrivateStorage(),
                                   blank=True)
    add_url_name = 'storage_b2_add'
    detail_url_name = 'storage_b2'
    edit_url_name = 'storage_b2_update'
    delete_url_name = 'storage_b2_delete'

    def __str__(self):
        return 'b2://' + str(self.bucket)

    @staticmethod
    def get_name():
        return _("Backblaze B2 Storage")

    def get_url(self):
        return "https://f004.backblazeb2.com/file/" + str(self.bucket)

    def get_repo_url(self):
        return self.get_url() + "/fdroid/" + REPO_DIR

    def create_config_file(self):
        # create config file from model fields
        config = configparser.ConfigParser()
        config.add_section("b2-remote")
        config.set("b2-remote", "type", self.type)
        config.set("b2-remote", "account", self.account)
        config.set("b2-remote", "key", self.key)

        # write to rclone config
        config_path = os.path.join(settings.DATA_DIR, B2_CONFIG_NAME)
        with open(config_path, "w", encoding="utf-8") as file_pointer:
            config.write(file_pointer)

        #  read config path and write to private config
        config_content = open(config_path, encoding="utf-8")
        self.config_file.save(
            B2_CONFIG_NAME, ContentFile(
                config_content.read()))
        os.remove(config_path)

    def publish(self):
        logging.info("Publishing '%s' to %s", self.repo, self)
        config = self.repo.get_config()
        config['rclone'] = True
        config['awsbucket'] = self.bucket
        config['rclone_config'] = "b2-remote"
        config['path_to_custom_rclone_config'] = os.path.join(
            settings.PRIVATE_REPO_ROOT, self.config_file.name)
        fdroidserver.deploy.update_remote_storage_with_rclone(REPO_DIR)
