# Generated by Django 5.1.3 on 2024-11-15 07:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crafter', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('user', 'title')},
        ),
    ]
