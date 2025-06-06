from django.contrib.auth.decorators import login_required
from django.shortcuts import render,  get_object_or_404, redirect
from django.db.models import Count
from .models import Game, Genre, Purchase, User, Review
from .forms import GameForm

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

    purchased_ids = []
    if request.user.is_authenticated:
        purchased_ids = list(
            Purchase.objects.filter(user=request.user).values_list('game_id', flat=True)
        )

    context = {
        'popular_games': popular_games,
        'new_releases': new_releases,
        'top_genres': top_genres,
        'search_results': search_results,
        'request': request,
        'purchased_ids': purchased_ids,
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

    purchased_ids = []
    if request.user.is_authenticated:
        purchased_ids = list(
            Purchase.objects.filter(user=request.user).values_list('game_id', flat=True)
        )

    context = {
        'games': games,
        'purchased_ids': purchased_ids,
    }
    return render(request, 'all_new_games.html', context)


def top_games_view(request):
    games = Game.objects.annotate(
        purchase_count=Count('purchase')
    ).order_by('-purchase_count')
    purchased_ids = []
    if request.user.is_authenticated:
        purchased_ids = list(
            Purchase.objects.filter(user=request.user).values_list('game_id', flat=True)
        )

    context = {
        'games': games,
        'purchased_ids': purchased_ids,
    }
    return render(request, 'top_games.html', context)

def all_genres_view(request):
    genres = Genre.objects.annotate(game_count=Count('game')).order_by('-game_count')
    return render(request, 'all_genres.html', {'genres': genres})

def genre_detail_view(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    games = Game.objects.filter(genre=genre)

    purchased_ids = []
    if request.user.is_authenticated:
        purchased_ids = list(
            Purchase.objects.filter(user=request.user).values_list('game_id', flat=True)
        )

    context = {
        'genre': genre,
        'games': games,
        'purchased_ids': purchased_ids,
    }
    return render(request, 'genre_detail.html', context)

@login_required
def favorite_games_view(request):
    user = request.user
    games = user.favorite_games.all()
    purchased_ids = []
    if user.is_authenticated:
        purchased_ids = list(
            Purchase.objects.filter(user=user).values_list('game_id', flat=True)
        )
    return render(request, 'favorite_games.html', {'games': games, 'purchased_ids': purchased_ids})


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
    if Purchase.objects.filter(user=user, game=game).exists():
        return redirect(request.META.get('HTTP_REFERER', '/'))
    user.favorite_games.add(game)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_favorites(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    user.favorite_games.remove(game)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    request.user.cart_games.add(game)
    return redirect(request.META.get('HTTP_REFERER', '/profile/'))

@login_required
def remove_from_cart(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    request.user.cart_games.remove(game)
    return redirect(request.META.get('HTTP_REFERER', '/profile/'))

@login_required
def buy_cart(request):
    user = request.user
    for game in user.cart_games.all():
        Purchase.objects.create(user=user, game=game, price=game.price)
        user.favorite_games.remove(game)  
    user.cart_games.clear()
    return redirect('profile')

def games_list_view(request):
    games = Game.objects.all()
    return render(request, 'games_list.html', {'games': games})

def game_detail_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    reviews = Review.objects.filter(game=game)
    purchases = Purchase.objects.filter(game=game)
    buyers = User.objects.filter(purchase__game=game).distinct()
    return render(request, 'game_detail.html', {'game': game, 'reviews': reviews, 'buyers': buyers, 'purchases': purchases})

@login_required
def game_create_view(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('games_list')
    else:
        form = GameForm()
    return render(request, 'game_form.html', {'form': form, 'is_edit': False})

@login_required
def game_edit_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_detail', game_id=game.id)
    else:
        form = GameForm(instance=game)
    return render(request, 'game_form.html', {'form': form, 'is_edit': True, 'game': game})


@login_required
def game_delete_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == "POST":
        game.delete()
        return redirect('games_list')
    return render(request, 'game_confirm_delete.html', {'game': game})


