# Generated by Django 5.0.2 on 2024-02-26 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_poll_question_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polls', to='blog.poll'),
        ),
    ]
