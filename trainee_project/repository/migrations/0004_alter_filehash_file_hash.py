# Generated by Django 3.2.3 on 2021-05-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_alter_file_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filehash',
            name='file_hash',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
