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
        (-1, 'brak'),
        (0, 'Pieczywo'),
        (1, 'Nabiał i jaja'),
        (2, 'Mięso i ryby'),
        (3, 'Sypkie'),
        (4, 'Tłuszcze'),
        (5, 'Owoce'),
        (6, 'Warzywa'),
        (7, 'Słodycze'),
        (8, 'Dodatki'),
        (9, 'Zioła i przyprawy'),
        (10, 'Napoje'),
        (11, 'Grzyby'),

    )
    name = models.IntegerField(choices=CATEGORIES, default=-1, verbose_name="Kategoria")

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.get_name_display()


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='Składnik')
    price = models.FloatField(null=True, blank=True)
    path = models.ImageField(upload_to='ingredient_photo', verbose_name='Zdjęcie')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoria')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredient_detail', kwargs={'pk': self.id})


class Type(models.Model):
    type = models.CharField(max_length=100, verbose_name="Rodzaj")
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name="Rodzaj składnika",
                                   null=True,
                                   blank=True)

    def __str__(self):
        return self.type


class Recipe(models.Model):
    name = models.CharField(max_length=100, verbose_name='Przepis')
    path = models.ImageField(upload_to='recipe_photo', verbose_name='Zdjęcie', null=True, blank=True)
    description = models.TextField(verbose_name='Sposób przygotowania', blank=True)
    url = models.URLField(max_length=100, verbose_name="Link", blank=True)
    time = models.IntegerField(verbose_name='Czas przygotowania', help_text='Czas w minutach', null=True, blank=True)
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
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField()
