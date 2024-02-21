# Generated by Django 4.2.4 on 2024-01-28 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': 'Candidate'},
        ),
        migrations.AlterField(
            model_name='participant',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='participant'),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('COMPANY', 'Company'), ('COORDINATOR', 'Coordinator'), ('PARTICIPANT', 'Participant'), ('STAFF', 'Staff')], default='PARTICIPANT', max_length=50, verbose_name='Type'),
        ),
    ]