# Generated by Django 4.1.9 on 2023-06-30 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_movie_scraping_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='tags',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='علامات'),
        ),
    ]
