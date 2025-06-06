from django.db import models
from django.contrib.auth.models import AbstractUser



class Genre(models.Model):
    name = models.CharField("Название жанра", max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField("Имя разработчика", max_length=100)
    country = models.CharField("Страна", max_length=50, blank=True, null=True)
    website = models.URLField("Сайт", blank=True, null=True)

    class Meta:
        verbose_name = "Разработчик"
        verbose_name_plural = "Разработчики"

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField("Название игры", max_length=100)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    release_date = models.DateField("Дата выхода")
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Разработчик")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, verbose_name="Жанр")
    cover_image = models.ImageField("Обложка", upload_to='game_covers/', blank=True)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return self.title


class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('admin', 'Администратор'),
        ('developer', 'Разработчик'),
    ]
    role = models.CharField("Роль", max_length=20, choices=ROLE_CHOICES, default='client')
    favorite_games = models.ManyToManyField('Game', blank=True)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    cart_games = models.ManyToManyField('Game', blank=True, related_name='cart_users')



    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username




class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Игра")
    price = models.DecimalField("Цена покупки", max_digits=8, decimal_places=2)
    purchase_date = models.DateTimeField("Дата покупки", auto_now_add=True)

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"

    def __str__(self):
        return f"{self.user} — {self.game}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Игра")
    rating = models.PositiveSmallIntegerField("Оценка", choices=[(i, i) for i in range(1, 11)])
    text = models.TextField("Текст отзыва")
    created_at = models.DateTimeField("Дата отзыва", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.user} — {self.game} — {self.rating}/10"
