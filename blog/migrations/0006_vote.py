# Generated by Django 5.0.2 on 2024-02-27 14:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_choice_poll'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.user')),
            ],
        ),
    ]