from django.contrib import admin
from .models import Genre, Developer, Game, User, Purchase, Review
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_display_links = ("name",)


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "website")
    list_filter = ("country",)
    search_fields = ("name", "country")
    list_display_links = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
        ('Дополнительно', {'fields': ('role', 'favorite_games')}),  # можно оставить
    )
    filter_horizontal = ('groups', 'user_permissions', 'favorite_games')

    def save_model(self, request, obj, form, change):
        # Сначала создаём пользователя
        obj.save()
        # Потом сохраняем M2M связи
        form.save_m2m()




class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ("created_at",)
    raw_id_fields = ("user",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "release_date", "genre", "developer", "is_new_display")
    list_filter = ("genre", "release_date")
    search_fields = ("title", "description")
    date_hierarchy = "release_date"
    raw_id_fields = ("developer", "genre")
    list_display_links = ("title",)
    inlines = [ReviewInline]

    @admin.display(description="Новая?")
    def is_new_display(self, obj):
        from datetime import date, timedelta
        return obj.release_date >= date.today() - timedelta(days=30)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "game", "price", "purchase_date")
    list_filter = ("purchase_date",)
    search_fields = ("user__username", "game__title")
    date_hierarchy = "purchase_date"
    list_display_links = ("user",)
    raw_id_fields = ("user", "game")



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "game", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "game__title", "text")
    date_hierarchy = "created_at"
    list_display_links = ("user",)
    raw_id_fields = ("user", "game")


