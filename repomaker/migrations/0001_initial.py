# Generated by Django 2.0.13 on 2022-05-23 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import repomaker.models.storage
import repomaker.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_id', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(storage=repomaker.storage.RepoStorage(), upload_to=repomaker.storage.get_apk_file_path)),
                ('version_name', models.CharField(blank=True, max_length=128)),
                ('version_code', models.PositiveIntegerField(default=0)),
                ('size', models.PositiveIntegerField(default=0)),
                ('signature', models.CharField(blank=True, max_length=512, null=True)),
                ('hash', models.CharField(blank=True, max_length=512)),
                ('hash_type', models.CharField(blank=True, max_length=32)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_downloading', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ApkPointer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=repomaker.storage.RepoStorage(), upload_to=repomaker.storage.get_apk_file_path)),
                ('apk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repomaker.Apk')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_id', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('summary_override', models.CharField(blank=True, max_length=255)),
                ('description_override', models.TextField(blank=True)),
                ('author_name', models.CharField(blank=True, max_length=255)),
                ('website', models.URLField(blank=True, max_length=2048)),
                ('icon', models.ImageField(upload_to=repomaker.storage.get_icon_file_path_for_app)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.CharField(blank=True, max_length=255)),
                ('summary_en_us', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_en', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_de_de', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_de', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_zh_cn', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True)),
                ('description_en_us', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('description_de_de', models.TextField(blank=True, null=True)),
                ('description_de', models.TextField(blank=True, null=True)),
                ('description_fr', models.TextField(blank=True, null=True)),
                ('description_zh_cn', models.TextField(blank=True, null=True)),
                ('available_languages', models.TextField(default='', max_length=8)),
                ('type', models.CharField(choices=[('apk', 'APK'), ('book', 'Book'), ('document', 'Document'), ('image', 'Image'), ('audio', 'Audio'), ('video', 'Video'), ('other', 'Other')], default='apk', max_length=16)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('feature_graphic', models.ImageField(blank=True, max_length=1024, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('feature_graphic_en_us', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('feature_graphic_en', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('feature_graphic_de_de', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('feature_graphic_de', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('feature_graphic_fr', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('feature_graphic_zh_cn', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('high_res_icon', models.ImageField(blank=True, max_length=1024, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('high_res_icon_en_us', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('high_res_icon_en', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('high_res_icon_de_de', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('high_res_icon_de', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('high_res_icon_fr', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('high_res_icon_zh_cn', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('tv_banner', models.ImageField(blank=True, max_length=1024, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('tv_banner_en_us', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('tv_banner_en', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('tv_banner_de_de', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('tv_banner_de', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('tv_banner_fr', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
                ('tv_banner_zh_cn', models.ImageField(blank=True, max_length=1024, null=True, upload_to=repomaker.storage.get_graphic_asset_file_path)),
            ],
            options={
                'ordering': ['added_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='GitStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=256, validators=[repomaker.models.storage.HostnameValidator()])),
                ('path', models.CharField(max_length=512, validators=[repomaker.models.storage.PathValidator()])),
                ('identity_file', models.FileField(blank=True, storage=repomaker.storage.PrivateStorage(), upload_to=repomaker.storage.get_identity_file_path)),
                ('public_key', models.TextField(blank=True, null=True)),
                ('url', models.URLField(max_length=2048)),
                ('disabled', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemoteApkPointer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2048)),
                ('apk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repomaker.Apk')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemoteApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_id', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('summary_override', models.CharField(blank=True, max_length=255)),
                ('description_override', models.TextField(blank=True)),
                ('author_name', models.CharField(blank=True, max_length=255)),
                ('website', models.URLField(blank=True, max_length=2048)),
                ('icon', models.ImageField(upload_to=repomaker.storage.get_icon_file_path_for_app)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.CharField(blank=True, max_length=255)),
                ('summary_en_us', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_en', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_de_de', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_de', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('summary_zh_cn', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True)),
                ('description_en_us', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('description_de_de', models.TextField(blank=True, null=True)),
                ('description_de', models.TextField(blank=True, null=True)),
                ('description_fr', models.TextField(blank=True, null=True)),
                ('description_zh_cn', models.TextField(blank=True, null=True)),
                ('available_languages', models.TextField(default='', max_length=8)),
                ('icon_etag', models.CharField(blank=True, max_length=128, null=True)),
                ('last_updated_date', models.DateTimeField(blank=True)),
                ('feature_graphic_url', models.URLField(blank=True, max_length=2048)),
                ('feature_graphic_url_en_us', models.URLField(blank=True, max_length=2048, null=True)),
                ('feature_graphic_url_en', models.URLField(blank=True, max_length=2048, null=True)),
                ('feature_graphic_url_de_de', models.URLField(blank=True, max_length=2048, null=True)),
                ('feature_graphic_url_de', models.URLField(blank=True, max_length=2048, null=True)),
                ('feature_graphic_url_fr', models.URLField(blank=True, max_length=2048, null=True)),
                ('feature_graphic_url_zh_cn', models.URLField(blank=True, max_length=2048, null=True)),
                ('feature_graphic_etag', models.CharField(blank=True, max_length=128, null=True)),
                ('feature_graphic_etag_en_us', models.CharField(blank=True, max_length=128, null=True)),
                ('feature_graphic_etag_en', models.CharField(blank=True, max_length=128, null=True)),
                ('feature_graphic_etag_de_de', models.CharField(blank=True, max_length=128, null=True)),
                ('feature_graphic_etag_de', models.CharField(blank=True, max_length=128, null=True)),
                ('feature_graphic_etag_fr', models.CharField(blank=True, max_length=128, null=True)),
                ('feature_graphic_etag_zh_cn', models.CharField(blank=True, max_length=128, null=True)),
                ('high_res_icon_url', models.URLField(blank=True, max_length=2048)),
                ('high_res_icon_url_en_us', models.URLField(blank=True, max_length=2048, null=True)),
                ('high_res_icon_url_en', models.URLField(blank=True, max_length=2048, null=True)),
                ('high_res_icon_url_de_de', models.URLField(blank=True, max_length=2048, null=True)),
                ('high_res_icon_url_de', models.URLField(blank=True, max_length=2048, null=True)),
                ('high_res_icon_url_fr', models.URLField(blank=True, max_length=2048, null=True)),
                ('high_res_icon_url_zh_cn', models.URLField(blank=True, max_length=2048, null=True)),
                ('high_res_icon_etag', models.CharField(blank=True, max_length=128, null=True)),
                ('high_res_icon_etag_en_us', models.CharField(blank=True, max_length=128, null=True)),
                ('high_res_icon_etag_en', models.CharField(blank=True, max_length=128, null=True)),
                ('high_res_icon_etag_de_de', models.CharField(blank=True, max_length=128, null=True)),
                ('high_res_icon_etag_de', models.CharField(blank=True, max_length=128, null=True)),
                ('high_res_icon_etag_fr', models.CharField(blank=True, max_length=128, null=True)),
                ('high_res_icon_etag_zh_cn', models.CharField(blank=True, max_length=128, null=True)),
                ('tv_banner_url', models.URLField(blank=True, max_length=2048)),
                ('tv_banner_url_en_us', models.URLField(blank=True, max_length=2048, null=True)),
                ('tv_banner_url_en', models.URLField(blank=True, max_length=2048, null=True)),
                ('tv_banner_url_de_de', models.URLField(blank=True, max_length=2048, null=True)),
                ('tv_banner_url_de', models.URLField(blank=True, max_length=2048, null=True)),
                ('tv_banner_url_fr', models.URLField(blank=True, max_length=2048, null=True)),
                ('tv_banner_url_zh_cn', models.URLField(blank=True, max_length=2048, null=True)),
                ('tv_banner_etag', models.CharField(blank=True, max_length=128, null=True)),
                ('tv_banner_etag_en_us', models.CharField(blank=True, max_length=128, null=True)),
                ('tv_banner_etag_en', models.CharField(blank=True, max_length=128, null=True)),
                ('tv_banner_etag_de_de', models.CharField(blank=True, max_length=128, null=True)),
                ('tv_banner_etag_de', models.CharField(blank=True, max_length=128, null=True)),
                ('tv_banner_etag_fr', models.CharField(blank=True, max_length=128, null=True)),
                ('tv_banner_etag_zh_cn', models.CharField(blank=True, max_length=128, null=True)),
                ('category', models.ManyToManyField(blank=True, limit_choices_to={'user': None}, to='repomaker.Category')),
            ],
            options={
                'ordering': ['added_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemoteRepository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField(blank=True, max_length=2048, null=True)),
                ('icon', models.ImageField(upload_to=repomaker.storage.get_icon_file_path)),
                ('public_key', models.TextField(blank=True)),
                ('fingerprint', models.CharField(blank=True, max_length=512)),
                ('update_scheduled', models.BooleanField(default=False)),
                ('is_updating', models.BooleanField(default=False)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('pre_installed', models.BooleanField(default=False)),
                ('index_etag', models.CharField(blank=True, max_length=128, null=True)),
                ('icon_etag', models.CharField(blank=True, max_length=128, null=True)),
                ('mirrors', models.TextField(blank=True)),
                ('disabled', models.BooleanField(default=False)),
                ('last_change_date', models.DateTimeField()),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Remote Repositories',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemoteScreenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(default='en', max_length=32)),
                ('type', models.CharField(choices=[('phoneScreenshots', 'Phone'), ('sevenInchScreenshots', "7'' Tablet"), ('tenInchScreenshots', "10'' Tablet"), ('tvScreenshots', 'TV'), ('wearScreenshots', 'Wearable')], default='phoneScreenshots', max_length=32)),
                ('url', models.URLField(max_length=2048)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.RemoteApp')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField(blank=True, max_length=2048, null=True)),
                ('icon', models.ImageField(upload_to=repomaker.storage.get_icon_file_path)),
                ('public_key', models.TextField(blank=True)),
                ('fingerprint', models.CharField(blank=True, max_length=512)),
                ('update_scheduled', models.BooleanField(default=False)),
                ('is_updating', models.BooleanField(default=False)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('qrcode', models.ImageField(blank=True, upload_to=repomaker.storage.get_repo_file_path)),
                ('key_store_pass', models.CharField(max_length=64)),
                ('key_pass', models.CharField(max_length=64)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_publication_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Repositories',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='S3Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disabled', models.BooleanField(default=False)),
                ('region', models.CharField(choices=[('s3', 'US Standard')], default='s3', max_length=32)),
                ('bucket', models.CharField(max_length=128)),
                ('accesskeyid', models.CharField(max_length=128)),
                ('secretkey', models.CharField(max_length=255)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.Repository')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(default='en', max_length=32)),
                ('type', models.CharField(choices=[('phoneScreenshots', 'Phone'), ('sevenInchScreenshots', "7'' Tablet"), ('tenInchScreenshots', "10'' Tablet"), ('tvScreenshots', 'TV'), ('wearScreenshots', 'Wearable')], default='phoneScreenshots', max_length=32)),
                ('file', models.ImageField(max_length=1024, storage=repomaker.storage.RepoStorage(), upload_to=repomaker.storage.get_screenshot_file_path)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.App')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SshStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=256, validators=[repomaker.models.storage.HostnameValidator()])),
                ('path', models.CharField(max_length=512, validators=[repomaker.models.storage.PathValidator()])),
                ('identity_file', models.FileField(blank=True, storage=repomaker.storage.PrivateStorage(), upload_to=repomaker.storage.get_identity_file_path)),
                ('public_key', models.TextField(blank=True, null=True)),
                ('url', models.URLField(max_length=2048)),
                ('disabled', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=64, validators=[repomaker.models.storage.UsernameValidator()])),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.Repository')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='remoteapp',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.RemoteRepository'),
        ),
        migrations.AddField(
            model_name='remoteapkpointer',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.RemoteApp'),
        ),
        migrations.AddField(
            model_name='gitstorage',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.Repository'),
        ),
        migrations.AddField(
            model_name='app',
            name='category',
            field=models.ManyToManyField(blank=True, limit_choices_to={'user': None}, to='repomaker.Category'),
        ),
        migrations.AddField(
            model_name='app',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.Repository'),
        ),
        migrations.AddField(
            model_name='app',
            name='tracked_remote',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repomaker.RemoteApp'),
        ),
        migrations.AddField(
            model_name='apkpointer',
            name='app',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repomaker.App'),
        ),
        migrations.AddField(
            model_name='apkpointer',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repomaker.Repository'),
        ),
        migrations.AlterUniqueTogether(
            name='remoteapp',
            unique_together={('package_id', 'repo')},
        ),
        migrations.AlterUniqueTogether(
            name='remoteapkpointer',
            unique_together={('apk', 'app')},
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('user', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='app',
            unique_together={('package_id', 'repo')},
        ),
        migrations.AlterUniqueTogether(
            name='apkpointer',
            unique_together={('apk', 'app')},
        ),
    ]
