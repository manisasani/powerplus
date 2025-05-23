# Generated by Django 5.1.5 on 2025-01-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activity_level',
            field=models.CharField(choices=[('very active', 'Very Active'), ('active', 'Active'), ('moderately active', 'Moderately Active'), ('lightly active', 'Lightly Active')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='diet_goal',
            field=models.CharField(choices=[('lose weight', 'Lose Weight'), ('gain weight', 'Gain Weight'), ('maintain weight', 'Maintain Weight'), ('muscle_building', 'Muscle Building')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='experience_level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='plan_goal',
            field=models.CharField(choices=[('muscle gain', 'Muscle Gain'), ('fat loss', 'Fat Loss'), ('fitness', 'Fitness')], max_length=20, null=True),
        ),
    ]
