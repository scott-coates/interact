# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-02 16:41
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveTaTopicOption',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('option_name', models.CharField(max_length=2400)),
                ('option_type', models.CharField(max_length=2400)),
                ('option_attrs', jsonfield.fields.JSONField()),
                ('ta_topic_id', models.CharField(max_length=8)),
                ('ta_topic_relevance', models.PositiveSmallIntegerField()),
                ('topic_id', models.CharField(max_length=8)),
                ('client_id', models.CharField(max_length=8)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientLookupForEa',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('ta_attrs', jsonfield.fields.JSONField()),
                ('ta_topics', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EoLookupByProvider',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('external_id', models.CharField(max_length=2400)),
                ('provider_type', models.CharField(max_length=2400)),
                ('prospect_id', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='EOLookupForEa',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('eo_attrs', jsonfield.fields.JSONField()),
                ('topic_ids', jsonfield.fields.JSONField()),
                ('provider_type', models.CharField(max_length=2400)),
                ('profile_id', models.CharField(max_length=8)),
                ('prospect_id', models.CharField(max_length=8)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileLookupByProvider',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('external_id', models.CharField(max_length=2400)),
                ('provider_type', models.CharField(max_length=2400)),
                ('prospect_id', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileLookupForEa',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('profile_attrs', jsonfield.fields.JSONField()),
                ('prospect_id', models.CharField(max_length=8)),
                ('provider_type', models.CharField(max_length=2400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProspectLookupForEa',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('attrs', jsonfield.fields.JSONField()),
                ('topic_ids', jsonfield.fields.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopicLookup',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('name', models.CharField(max_length=2400)),
                ('stem', models.CharField(max_length=2400)),
                ('collapsed_stem', models.CharField(max_length=2400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='profilelookupbyprovider',
            unique_together=set([('external_id', 'provider_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='eolookupbyprovider',
            unique_together=set([('external_id', 'provider_type', 'prospect_id')]),
        ),
    ]
