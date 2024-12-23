# Generated by Django 5.1.3 on 2024-11-29 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafter', '0010_alter_modulequestion_course_module_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortname', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionskill_question', to='crafter.modulequestion')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionskill_skill', to='crafter.skill')),
            ],
        ),
        migrations.CreateModel(
            name='LearningOutcomeSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning_outcome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loskill_lo', to='crafter.coursemodulelearningoutcome')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loskill_skill', to='crafter.skill')),
            ],
        ),
    ]
