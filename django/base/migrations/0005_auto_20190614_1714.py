# Generated by Django 2.2.2 on 2019-06-14 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20190612_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(default=60, verbose_name='Tiempo de elaboración (minutos)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=256, verbose_name='Biografía'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='followed',
            field=models.ManyToManyField(blank=True, related_name='Seguidos', to='base.Profile', verbose_name='Seguidos'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='Seguidores', to='base.Profile', verbose_name='Seguidores'),
        ),
    ]