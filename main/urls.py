"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from snack_puzzle import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.AddUserView.as_view(), name='register'),
    path('ingredient_detail/<pk>', views.IngredientDetailView.as_view(), name='ingredient_detail'),
    path('add_recipe', views.RecipeCreateView.as_view(), name='add_recipe'),
    path('add_amount', views.IngredientRecipeCreateView.as_view(), name='add_amount'),
] + staticfiles_urlpatterns() + \
  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
