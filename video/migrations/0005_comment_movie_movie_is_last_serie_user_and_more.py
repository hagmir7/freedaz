# Generated by Django 4.1.9 on 2023-06-24 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import video.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0004_playlist_season_playlist_serie_remove_movie_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='movie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='video.movie'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='is_last',
            field=models.BooleanField(default=False, null=True, verbose_name='الحلقة الأخيرة'),
        ),
        migrations.AddField(
            model_name='serie',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to=video.models.filename, verbose_name='صورة '),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, verbose_name='إسم الصنف'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='movie_category', to='video.category', verbose_name='صنف'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(default='', verbose_name='الوصف'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='episode',
            field=models.IntegerField(blank=True, null=True, verbose_name='لاحلقة'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=video.models.filename, verbose_name='صورة'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='video.playlist', verbose_name='إختيار الموسم'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='video.subscription', verbose_name='الشركة المنتجة'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='tags',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='علامات'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='play_list_category', to='video.category', verbose_name='صنف'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.TextField(default='', verbose_name='وصف'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=video.models.filename, verbose_name='صورة'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='season',
            field=models.IntegerField(blank=True, null=True, verbose_name='موسم'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='serie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='video.serie', verbose_name='تحديد المسلسل'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='video.subscription', verbose_name='الشركة المنتجة '),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='title',
            field=models.CharField(max_length=255, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='serie_category', to='video.category', verbose_name='صنف'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='description',
            field=models.TextField(default='', verbose_name='وصف'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=video.models.filename, verbose_name='صورة'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='video.subscription', verbose_name='الشركة المنتجة '),
        ),
        migrations.AlterField(
            model_name='serie',
            name='title',
            field=models.CharField(max_length=255, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='description',
            field=models.TextField(verbose_name='وصف '),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='image',
            field=models.ImageField(upload_to=video.models.filename, verbose_name='صورة '),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='name',
            field=models.CharField(max_length=150, verbose_name='إسم الشركة '),
        ),
        migrations.AlterField(
            model_name='video',
            name='quality',
            field=models.CharField(max_length=100, verbose_name='الجودة'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.FileField(upload_to=video.models.filename, verbose_name='تحميل الفيديو '),
        ),
    ]
