# Generated by Django 4.0.1 on 2022-09-03 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0009_rename_user_annotation_user_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='root_png',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='name_video',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='root_ann',
            field=models.TextField(blank=True, null=True),
        ),
    ]
