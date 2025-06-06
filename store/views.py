from django.contrib.auth.decorators import login_required
from django.shortcuts import render,  get_object_or_404, redirect
from django.db.models import Count
from .models import Game, Genre, Purchase, User, Review

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

    genres = (
        Purchase.objects
        .filter(user=user)
        .values('game__genre')
        .annotate(total=Count('game__genre'))
        .order_by('-total')
    )

    top_total = genres[0]['total'] if genres else 0

    top_genre_ids = [g['game__genre'] for g in genres if g['total'] == top_total]

    genre_games = Game.objects.filter(
        genre_id__in=top_genre_ids
    ).exclude(purchase__user=user)[:5]

    top_devs = (
        Purchase.objects
        .filter(user=user)
        .values('game__developer')
        .annotate(total=Count('game__developer'))
        .order_by('-total')
    )
    dev_top_total = top_devs[0]['total'] if top_devs else 0
    top_dev_ids = [d['game__developer'] for d in top_devs if d['total'] == dev_top_total]

    developer_games = Game.objects.filter(
        developer_id__in=top_dev_ids
    ).exclude(purchase__user=user)[:5]

    return render(request, 'recommendations.html', {
        'genre_games': genre_games,
        'developer_games': developer_games
    })


def all_new_games_view(request):
    games = Game.objects.order_by('-release_date')
    return render(request, 'all_new_games.html', {'games': games})

def top_games_view(request):
    games = Game.objects.annotate(
        purchase_count=Count('purchase')
    ).order_by('-purchase_count')
    return render(request, 'top_games.html', {'games': games})

def all_genres_view(request):
    genres = Genre.objects.annotate(game_count=Count('game')).order_by('-game_count')
    return render(request, 'all_genres.html', {'genres': genres})

def genre_detail_view(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    games = Game.objects.filter(genre=genre)
    return render(request, 'genre_detail.html', {'genre': genre, 'games': games})

@login_required
def favorite_games_view(request):
    user = request.user
    games = user.favorite_games.all()
    return render(request, 'favorite_games.html', {'games': games})

@login_required
def profile_view(request):
    user = request.user
    purchases = Purchase.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)
    return render(request, 'profile.html', {
        'purchases': purchases,
        'reviews': reviews,
        'user': user,
    })

@login_required
def add_to_favorites(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    user.favorite_games.add(game)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_favorites(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    user.favorite_games.remove(game)
    return redirect(request.META.get('HTTP_REFERER', '/'))