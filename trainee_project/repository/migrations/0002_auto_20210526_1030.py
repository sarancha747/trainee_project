# Generated by Django 3.2.3 on 2021-05-26 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileHash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_hash', models.CharField(max_length=256)),
                ('real_file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.RemoveField(
            model_name='file',
            name='file',
        ),
        migrations.RemoveField(
            model_name='file',
            name='slug',
        ),
        migrations.AddField(
            model_name='file',
            name='user_file_title',
            field=models.CharField(default='s', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='upload',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.filehash'),
        ),
    ]
