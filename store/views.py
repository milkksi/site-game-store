from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from .models import Game, Genre, Purchase, User

def home_view(request):
    query = request.GET.get('q')
    search_results = None

    if query:
        search_results = Game.objects.filter(title__icontains=query)

    popular_games = Game.objects.annotate(
        purchase_count=Count('purchase')
    ).order_by('-purchase_count')[:5]

    new_releases = Game.objects.order_by('-release_date')[:5]

    top_genres = Genre.objects.annotate(
        game_count=Count('game')
    ).order_by('-game_count')[:5]

    context = {
        'popular_games': popular_games,
        'new_releases': new_releases,
        'top_genres': top_genres,
        'search_results': search_results,
        'request': request  # чтобы получить `request.GET.q` в шаблоне
    }

    return render(request, 'home.html', context)

@login_required
def recommendations_view(request):
    user = request.user

    # 1. Самый частый жанр, купленный пользователем
    top_genre = (
        Purchase.objects
        .filter(user=user)
        .values('game__genre')
        .annotate(total=Count('game__genre'))
        .order_by('-total')
        .first()
    )

    # 2. Самый частый разработчик, купленный пользователем
    top_developer = (
        Purchase.objects
        .filter(user=user)
        .values('game__developer')
        .annotate(total=Count('game__developer'))
        .order_by('-total')
        .first()
    )

    # 3. Рекомендации на основе жанра
    genre_games = []
    if top_genre and top_genre['game__genre']:
        genre_games = Game.objects.filter(
            genre_id=top_genre['game__genre']
        ).exclude(purchase__user=user)[:5]

    # 4. Рекомендации на основе разработчика
    developer_games = []
    if top_developer and top_developer['game__developer']:
        developer_games = Game.objects.filter(
            developer_id=top_developer['game__developer']
        ).exclude(purchase__user=user)[:5]

    return render(request, 'recommendations.html', {
        'genre_games': genre_games,
        'developer_games': developer_games
    })