from django.urls import path  
from .views import home_view, recommendations_view, all_new_games_view, top_games_view, all_genres_view, genre_detail_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home_view, name='home'),
    path('recommendations/', recommendations_view, name='recommendations'),
    path('new/', all_new_games_view, name='all_new_games'),
    path('top/', top_games_view, name='top_games'),
    path('genres/', all_genres_view, name='all_genres'),
    path('genre/<int:genre_id>/', genre_detail_view, name='genre_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]




