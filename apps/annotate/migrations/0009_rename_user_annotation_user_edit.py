# Generated by Django 4.0.1 on 2022-09-01 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0008_annotation_label_pk_annotation_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annotation',
            old_name='user',
            new_name='user_edit',
        ),
    ]
