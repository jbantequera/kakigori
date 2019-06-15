from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# PERFIL 'PÚBLICO' DE CADA CUENTA (Nombre, Bio, Seguidores...)
class Profile(models.Model):
    class Meta:
        verbose_name = u'Perfil de Usuario'
        verbose_name_plural = u'Perfiles de Usuarios'

    user = models.OneToOneField(User, verbose_name=u'Usuario asociado', on_delete=models.CASCADE)
    display_name = models.CharField(verbose_name=u'Nombre', max_length=15)
    bio = models.TextField(verbose_name=u'Biografía', max_length=256, blank=True)
    followers = models.ManyToManyField('self', verbose_name=u'Seguidores', related_name='Seguidores', blank=True, symmetrical=False)
    followed = models.ManyToManyField('self', verbose_name=u'Seguidos', related_name='Seguidos', blank=True, symmetrical=False)
    image = models.ImageField(upload_to='media_files/profile_image', default='media_files/profile_image/no-image.png')

    def __str__(self):
        return('Perfil de ' + self.user.username)

# RECETAS
class Recipe(models.Model):
    class Meta:
        verbose_name = u'Receta'
        verbose_name_plural = u'Recetas'
        ordering = ['-created_at']

    author = models.ForeignKey(Profile, verbose_name=u'Autor', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=u'Fecha de creación', auto_now_add=True)

    image = models.ImageField(upload_to='media_files/recipe_images', default='media_files/recipe_images/no-image.png')
    name = models.CharField(verbose_name=u'Nombre', max_length=20)
    description = models.TextField(verbose_name=u'Descripción', max_length=256)
    # CATEGORÍA DE LA RECETA
    cooking_time = models.PositiveIntegerField(verbose_name=u'Tiempo de elaboración (minutos)')
    # RATING
    votes_up = models.PositiveIntegerField(verbose_name=u'Votos positivos', default=0)
    votes_down = models.PositiveIntegerField(verbose_name=u'Votos negativos', default=0)
    voters = models.ManyToManyField('Profile', verbose_name=u'Usuarios que han votado', related_name='Usuarios_que_han_votado', blank=True)

    instructions = models.TextField(verbose_name=u'Instrucciones')

    def __str__(self):
        return(self.name + ' (' + self.author.user.username + ')')

    def get_rating(self):
        total_votes = self.votes_up + self.votes_down

        if total_votes != 0:
            rating = round((self.votes_up / total_votes) * 5)
        else:
            rating = 0

        return rating