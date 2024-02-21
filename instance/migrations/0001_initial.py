# Generated by Django 4.2.4 on 2024-01-25 15:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('question', '0003_remove_questioninstance_instance_pj_and_more'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('instance_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='project.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Instance',
                'verbose_name_plural': 'Instances',
            },
        ),
        migrations.CreateModel(
            name='QuestionInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_pj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='instance.instance')),
                ('question_pj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_pj', to='question.question')),
            ],
        ),
    ]