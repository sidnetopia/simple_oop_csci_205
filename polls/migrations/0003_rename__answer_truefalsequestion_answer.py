# Generated by Django 5.1.6 on 2025-02-07 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_answer_truefalsequestion__answer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='truefalsequestion',
            old_name='_answer',
            new_name='answer',
        ),
    ]
