# Generated by Django 2.0.4 on 2018-09-21 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_quiz_time_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('i', 'In Progress'), ('r', 'In Review'), ('p', 'published')], default='i', max_length=1),
        ),
    ]
