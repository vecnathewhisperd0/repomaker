from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Repository, RemoteRepository, App, RemoteApp, Apk, ApkPointer, \
    RemoteApkPointer, Category, Screenshot, RemoteScreenshot
from .models.storage import StorageManager

admin.site.register(Repository)
admin.site.register(RemoteRepository)
admin.site.register(App, TranslationAdmin)  # hides untranslated apps which should not exist
admin.site.register(RemoteApp, TranslationAdmin)  # hides untranslated apps which should not exist
admin.site.register(Apk)
admin.site.register(ApkPointer)
admin.site.register(RemoteApkPointer)
admin.site.register(Category)
admin.site.register(Screenshot)
admin.site.register(RemoteScreenshot)

for storage in StorageManager.storage_models:
    admin.site.register(storage)
