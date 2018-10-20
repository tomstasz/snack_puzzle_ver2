from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)

# Create your models here.
User = get_user_model()


class Category(models.Model):
    CATEGORIES = (
        ('Pie', 'Pieczywo'),
        ('Nab', 'Nabiał i jaja'),
        ('Mię', 'Mięso'),
        ('Syp', 'Sypkie'),
        ('Tłu', 'Tłuszcze'),
        ('Owo', 'Owoce'),
        ('Warz', 'Warzywa'),
        ('Sło', 'Słodycze'),
        ('Dod', 'Dodatki'),
        ('Zio', 'Zioła i przyprawy'),
        ('Nap', 'Napoje'),
        ('Grz', 'Grzyby'),
        ('Ryby', 'Ryby'),

    )
    name = models.CharField(choices=CATEGORIES, default='brak', max_length=100, verbose_name="Kategoria")

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.get_name_display()


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='Składnik')
    price = models.FloatField(null=True, blank=True)
    path = models.ImageField(upload_to='ingredient_photo', verbose_name='Zdjęcie')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoria')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredient_detail', kwargs={'pk': self.id})


class Recipe(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nazwa przepisu')
    path = models.ImageField(upload_to='recipe_photo', verbose_name='Zdjęcie', null=True, blank=True)
    description = models.TextField(verbose_name='Sposób przygotowania (opc.)', blank=True)
    url = models.URLField(max_length=100, verbose_name="Link do przepisu", blank=True)
    time = models.IntegerField(verbose_name='Czas przygotowania ( w min.)', null=True, blank=True)
    ingredient = models.ManyToManyField(Ingredient, through='IngredientRecipe', verbose_name='Składniki')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik", null=True, blank=True)
    date_add = models.DateField(auto_now_add=True)
    date_modify = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    MEALS = (
        (0, 'brak'),
        (1, 'śniadanie'),
        (2, 'drugie śniadanie'),
        (3, 'obiad'),
        (4, 'podwieczorek'),
        (5, 'kolacja'),
    )
    name = models.IntegerField(choices=MEALS, default=0, verbose_name="Rodzaj posiłku")
    recipe = models.ManyToManyField(Recipe, verbose_name='Dania')

    def __str__(self):
        return self.get_name_display()


class IngredientRecipe(models.Model):
    MEASURES = (
        ('g', 'g'),
        ('dag', 'dag'),
        ('szt.', 'szt.'),
        ('szklan.', 'szklan.'),
        ('łyż.', 'łyż.'),
        ('łyżecz.', 'łyżecz.'),
        ('szczypt.', 'szczypt.'),
        ('pęcz.', 'pęcz.'),
        ('opak.', 'opak.'),
        ('l', 'l'),
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Składnik")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name="Ilość")
    measure = models.CharField(choices=MEASURES, default='dag', max_length=32, verbose_name="Miara", null=True)

    def __str__(self):
        return 'Przepis: {}, Składnik: {}'.format(self.recipe, self.ingredient)
