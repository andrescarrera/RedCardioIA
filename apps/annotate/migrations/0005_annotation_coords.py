# Generated by Django 4.0.3 on 2022-03-30 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0004_rename_title_annotation_frame_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='coords',
            field=models.TextField(blank=True, null=True),
        ),
    ]
