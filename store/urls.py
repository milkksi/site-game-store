from django.urls import path  
from .views import (
    home_view,
    recommendations_view,
    favorite_games_view,   
    profile_view,          
    all_new_games_view,
    top_games_view,
    all_genres_view,
    genre_detail_view,
    add_to_favorites,
    remove_from_favorites,
    add_to_cart,
    remove_from_cart,
    buy_cart,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home_view, name='home'),
    path('recommendations/', recommendations_view, name='recommendations'),
    path('favorites/', favorite_games_view, name='favorite_games'),
    path('profile/', profile_view, name='profile'),
    path('new/', all_new_games_view, name='all_new_games'),
    path('top/', top_games_view, name='top_games'),
    path('genres/', all_genres_view, name='all_genres'),
    path('genre/<int:genre_id>/', genre_detail_view, name='genre_detail'),
    path('favorite/add/<int:game_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorite/remove/<int:game_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('cart/add/<int:game_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:game_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/buy/', buy_cart, name='buy_cart'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]




