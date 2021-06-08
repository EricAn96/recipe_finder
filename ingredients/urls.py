from django.urls import path
from .views import Ingredient_Delete, ListAndCreate, CustomLoginView, RegisterView, RecipeView, RecipeDetail
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', ListAndCreate.as_view(), name='list-and-create'),
    path('delete/<int:pk>', Ingredient_Delete.as_view(), name='ingredient-delete'),
    path('login/', CustomLoginView.as_view(), name='login-user'),
    path('logout/', LogoutView.as_view(next_page='login-user'), name='logout-user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recipes/', RecipeView, name='recipes'),
    path('recipes/<int:id>', RecipeDetail, name='recipe-detail'),
]