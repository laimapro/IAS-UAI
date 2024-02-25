# Generated by Django 4.2.4 on 2024-02-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_manager_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('pt-br', 'Portuguese (Brazil)')], default='pt-br', max_length=10),
        ),
    ]
