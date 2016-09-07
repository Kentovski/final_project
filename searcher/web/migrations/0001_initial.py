# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('image_source', models.URLField()),
                ('source', models.CharField(max_length=128)),
                ('number', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SpiderTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.CharField(max_length=512)),
                ('is_google_done', models.BooleanField(default=False)),
                ('is_yandex_done', models.BooleanField(default=False)),
                ('is_instagram_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='task',
            field=models.ForeignKey(to='web.SpiderTask'),
        ),
    ]
