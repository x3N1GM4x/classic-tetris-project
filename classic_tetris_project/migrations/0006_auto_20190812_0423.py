# Generated by Django 2.2.2 on 2019-08-12 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic_tetris_project', '0005_auto_20190810_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ntsc_pb_updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='pal_pb_updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
