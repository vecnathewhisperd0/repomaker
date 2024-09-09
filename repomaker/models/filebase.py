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

FILEBASE_CONFIG_NAME = "filebase-config.conf"


class FilebaseStorage(AbstractStorage):
    type = models.CharField(max_length=32, default='s3', editable=False)
    provider = models.CharField(max_length=32, default='Other', editable=False)
    access_key_id = models.CharField(max_length=255)
    secret_access_key = models.CharField(max_length=255)
    region = models.CharField(
        max_length=32,
        default='us-east-1',
        editable=False)
    endpoint = models.CharField(
        max_length=32,
        default='https://s3.filebase.com',
        editable=False)

    bucket = models.CharField(max_length=128)
    config_file = models.FileField(upload_to=get_identity_file_path,
                                   storage=PrivateStorage(),
                                   blank=True)

    add_url_name = 'storage_filebase_add'
    detail_url_name = 'storage_filebase'
    edit_url_name = 'storage_filebase_update'
    delete_url_name = 'storage_filebase_delete'

    def __str__(self):
        return str(self.endpoint) + "/" + str(self.bucket)

    @staticmethod
    def get_name():
        return _("Filebase Storage")

    def get_url(self):
        return str(self.endpoint) + "/" + str(self.bucket)

    def get_repo_url(self):
        return self.get_url() + "/fdroid/" + REPO_DIR

    def create_config_file(self):
        #  create config file from model fields
        config_type = "filebase-remote"
        config = configparser.ConfigParser()
        config.add_section(config_type)
        config.set(config_type, "type", self.type)
        config.set(config_type, "provider", self.provider)
        config.set(config_type, "access_key_id", self.access_key_id)
        config.set(config_type, "secret_access_key", self.secret_access_key)
        config.set(config_type, "region", self.region)
        config.set(config_type, "endpoint", self.endpoint)

        #  write to rclone config
        config_path = os.path.join(settings.DATA_DIR, FILEBASE_CONFIG_NAME)
        with open(config_path, "w", encoding="utf-8") as file_pointer:
            config.write(file_pointer)

        #  read config path and write to private config
        config_content = open(config_path, encoding="utf-8")
        self.config_file.save(
            FILEBASE_CONFIG_NAME, ContentFile(
                config_content.read()))
        os.remove(config_path)

    def publish(self):
        rclone_config_path = os.path.join(
            settings.PRIVATE_REPO_ROOT, self.config_file.name)
        logging.info("Publishing '%s' to %s", self.repo, self)
        config = self.repo.get_config()
        config['rclone'] = True
        config['awsbucket'] = self.bucket
        config['rclone_config'] = "filebase-remote"
        config['path_to_custom_rclone_config'] = rclone_config_path
        fdroidserver.deploy.update_remote_storage_with_rclone(REPO_DIR)
