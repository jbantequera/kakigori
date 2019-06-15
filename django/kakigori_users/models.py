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