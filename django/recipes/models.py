from django.db import models

# RECETAS
class Recipe(models.Model):
    class Meta:
        verbose_name = u'Receta'
        verbose_name_plural = u'Recetas'
        ordering = ['created_at']

    author = models.ForeignKey('kakigori_users.Profile', verbose_name=u'Autor', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=u'Fecha de creación', auto_now_add=True)

    image = models.ImageField(upload_to='media_files/recipe_images', default='media_files/recipe_images/no-image.png')
    name = models.CharField(verbose_name=u'Nombre', max_length=20)
    description = models.TextField(verbose_name=u'Descripción', max_length=512)
    # CATEGORÍA DE LA RECETA
    cooking_time = models.PositiveIntegerField(verbose_name=u'Tiempo de elaboración (minutos)')
    # RATING
    votes_up = models.PositiveIntegerField(verbose_name=u'Votos positivos', default=0)
    votes_down = models.PositiveIntegerField(verbose_name=u'Votos negativos', default=0)
    voters = models.ManyToManyField('kakigori_users.Profile', verbose_name=u'Usuarios que han votado', related_name='Usuarios_que_han_votado', blank=True)

    ingredients = models.TextField(verbose_name=u'Ingredientes')
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