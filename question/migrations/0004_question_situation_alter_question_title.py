# Generated by Django 4.2.4 on 2024-02-21 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_remove_questioninstance_instance_pj_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='situation',
            field=models.CharField(default='Situação geradora', max_length=355, verbose_name='Situation'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=355, verbose_name='Title'),
        ),
    ]