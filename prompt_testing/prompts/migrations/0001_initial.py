# Generated by Django 5.0.1 on 2024-01-18 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('prompt1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations_as_first', to='prompts.prompt')),
                ('prompt2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations_as_second', to='prompts.prompt')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluations_won', to='prompts.prompt')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo_rating', models.IntegerField(default=1500)),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prompts.prompt')),
            ],
        ),
    ]
