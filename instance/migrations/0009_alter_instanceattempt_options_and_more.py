# Generated by Django 4.2.4 on 2024-02-18 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0008_alter_instanceattemptanswer_likert_scale'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instanceattempt',
            options={'verbose_name': 'Instance Attempt', 'verbose_name_plural': 'Instance Attempts'},
        ),
        migrations.AlterModelOptions(
            name='instanceattemptanswer',
            options={'verbose_name': 'Instance Attempt Answer', 'verbose_name_plural': 'Instance Attempt Answers'},
        ),
        migrations.AlterModelOptions(
            name='questioninstance',
            options={'verbose_name': 'Question Instance', 'verbose_name_plural': 'Question Instances'},
        ),
    ]
