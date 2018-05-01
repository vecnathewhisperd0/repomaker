from __future__ import unicode_literals

from django.db import migrations

DEFAULT_CATEGORIES = [
    [ 'Connectivity', 'CBEFEC' ],
    [ 'Development', 'E2D6BC' ],
    [ 'Games', 'F3B569' ],
    [ 'Graphics', 'F65A5A' ],
    [ 'Internet', '73EABC' ],
    [ 'Money', 'DDDDD0' ],
    [ 'Multimedia', 'FF7F66' ],
    [ 'Navigation', '94D6FD' ],
    [ 'Phone & SMS', 'F3CFC0' ],
    [ 'Reading', 'D6A07A' ],
    [ 'Science & Education', 'FFAD08' ],
    [ 'Security', 'FFD15F' ],
    [ 'Sports & Health', 'ADCEDE' ],
    [ 'System', 'D3DB77' ],
    [ 'Theming', 'DEEFE9' ],
    [ 'Time', 'FF7043' ],
    [ 'Writing', 'F2E9CE' ],
]


def forwards_func(apps, schema_editor):
    # noinspection PyPep8Naming
    Category = apps.get_model("repomaker", "Category")
    db_alias = schema_editor.connection.alias
    Category.objects.using(db_alias).bulk_create(
        [Category(user=None, name=category[0]) for category in DEFAULT_CATEGORIES])


def reverse_func(apps, schema_editor):
    # noinspection PyPep8Naming
    Category = apps.get_model("repomaker", "Category")
    db_alias = schema_editor.connection.alias
    for category in DEFAULT_CATEGORIES:
        Category.objects.using(db_alias).filter(user=None, name=category[0]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('repomaker', 'default_user'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
