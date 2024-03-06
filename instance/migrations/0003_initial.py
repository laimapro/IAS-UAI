# Generated by Django 4.2.4 on 2024-02-27 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instance', '0002_initial'),
        ('project', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instanceattempt',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_answer', to='users.participant', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='instance',
            name='instance_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='project.project', verbose_name='Project'),
        ),
    ]