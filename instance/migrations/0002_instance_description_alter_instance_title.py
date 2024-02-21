# Generated by Django 4.2.4 on 2024-02-02 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='description',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
    ]