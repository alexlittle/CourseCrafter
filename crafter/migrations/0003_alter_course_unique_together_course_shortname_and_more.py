# Generated by Django 5.1.3 on 2024-11-21 14:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafter', '0002_alter_course_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='course',
            name='shortname',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('user', 'shortname')},
        ),
    ]
