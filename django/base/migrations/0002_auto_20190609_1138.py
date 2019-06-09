# Generated by Django 2.2.2 on 2019-06-09 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followed',
            field=models.ManyToManyField(related_name='_profile_followed_+', to='base.Profile', verbose_name='Seguidos'),
        ),
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='_profile_followers_+', to='base.Profile', verbose_name='Seguidores'),
        ),
    ]