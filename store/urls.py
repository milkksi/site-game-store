from django.urls import path
from .views import home_view, recommendations_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'),
    path('recommendations/', recommendations_view, name='recommendations'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]



