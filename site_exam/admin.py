from django.contrib import admin
from .models import smexam

@admin.register(smexam)
class smexamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_date', 'is_public')
    search_fields = ('name', 'participants__email')
    list_filter = ('is_public', 'created_at')
    filter_horizontal = ('participants',)
    date_hierarchy = 'exam_date'
