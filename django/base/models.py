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
    bio = models.TextField(verbose_name=u'Biografía', max_length=144, blank=True)
    followers = models.ManyToManyField('self', verbose_name=u'Seguidores', related_name='Seguidores')
    followed = models.ManyToManyField('self', verbose_name=u'Seguidos', related_name='Seguidos')
    image = models.ImageField(upload_to='media_files/profile_image', default='media_files/profile_image/no-image.png')

    def __str__(self):
        return('Perfil de ' + self.user.username)

# RECETAS
class Recipe(models.Model):
    class Meta:
        verbose_name = u'Receta'
        verbose_name_plural = u'Recetas'

    author = models.ForeignKey(Profile, verbose_name=u'Autor', on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='media_files/recipe_images', default='media_files/recipe_images/no-image.png')
    name = models.CharField(verbose_name=u'Nombre', max_length=20)
    description = models.TextField(verbose_name=u'Descripción', max_length=144, blank=True)
    # CATEGORÍA DE LA RECETA
    # TIEMPO QUE SE TARDA EN COCINAR

    instructions = models.TextField(verbose_name=u'Instrucciones')
    score = models.IntegerField(verbose_name=u'Puntuación', default=0)

    def __str__(self):
        return(self.name + ' (' + self.author.user.username + ')')