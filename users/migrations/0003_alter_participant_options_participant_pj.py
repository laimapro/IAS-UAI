# Generated by Django 4.2.4 on 2024-01-28 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('users', '0002_alter_participant_options_alter_participant_picture_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': 'Participant', 'verbose_name_plural': 'Participants'},
        ),
        migrations.AddField(
            model_name='participant',
            name='pj',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_project', to='project.project'),
            preserve_default=False,
        ),
    ]