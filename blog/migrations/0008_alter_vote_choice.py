# Generated by Django 5.0.2 on 2024-02-27 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_choice_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.choice'),
        ),
    ]
