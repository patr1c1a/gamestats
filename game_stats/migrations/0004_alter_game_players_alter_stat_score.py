# Generated by Django 4.2.8 on 2023-12-08 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_stats", "0003_alter_stat_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="players",
            field=models.ManyToManyField(
                related_name="players", to="game_stats.player"
            ),
        ),
        migrations.AlterField(
            model_name="stat",
            name="score",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
