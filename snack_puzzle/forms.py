from braces.forms import UserKwargModelFormMixin
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from .models import Ingredient, Recipe, IngredientRecipe
from .validators import validate_login


class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=64)
    password = forms.CharField(label='hasło', max_length=64, widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    login = forms.EmailField(label='Login(email)', validators=[EmailValidator, validate_login])
    password = forms.CharField(max_length=64, label='Hasło', widget=forms.PasswordInput)
    password_repeat = forms.CharField(max_length=64, label='Powtórz hasło', widget=forms.PasswordInput)

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
            raise ValidationError('Niepoprawne hasło')


class ResetPasswordForm(forms.Form):
    new_pass = forms.CharField(label='Wprowadź nowe hasło', max_length=64, widget=forms.PasswordInput)
    new_pass_confirm = forms.CharField(label='Ponownie wprowadź nowe hasło', max_length=64, widget=forms.PasswordInput)

    def clean(self):
        if self.cleaned_data['new_pass'] != self.cleaned_data['new_pass_confirm']:
            raise ValidationError('Niepoprawne hasło')


class AddRecipeForm(UserKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'time', 'user']
        widgets = {'user': forms.HiddenInput}

    def save(self, commit=False):
        obj = super().save(commit=False)
        obj.user = self.user
        obj.save()
        return obj
#
#
# class AddAmountForm(forms.ModelForm):
#     class Meta:
#         model = IngredientRecipe
#         fields = forms.ALL_FIELDS

# class AddRecipeForm(forms.Form):
#     name = forms.CharField(max_length=100, label='Nazwa')
#     description = forms.CharField(widget=forms.Textarea, label='Sposób przygotowania', required=False)
#     url = forms.URLField(max_length=100, label="Link", required=False)
#     time = forms.IntegerField(label='Czas przygotowania (w min.)')
#     ingredient = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), label="Składniki")
#
#
# class AddAmountForm(forms.Form):
#     ingredient = forms.ModelChoiceField(queryset=Recipe.objects.latest('id').ingredientrecipe_set.all(), label='Składniki')
#     amount = forms.FloatField(label="Ilość")
#     measure = forms.ChoiceField(choices=IngredientRecipe.MEASURES, label="Miara")


# class AddRecipeForm(forms.Form):
#     name = forms.CharField(max_length=100, label='Nazwa')
#     description = forms.CharField(widget=forms.Textarea, label='Sposób przygotowania', required=False)
#     url = forms.URLField(max_length=100, label="Link", required=False)
#     time = forms.IntegerField(label='Czas przygotowania (w min.)')
#
#
# class AddAmountForm(forms.Form):
#     ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), label='Składniki')
#     amount = forms.FloatField(label="Ilość")
#     measure = forms.ChoiceField(choices=IngredientRecipe.MEASURES, label="Miara")

