from django.db import models
from django.contrib.auth.models import User

class smexam(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название экзамена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    exam_date = models.DateField(verbose_name="Дата проведения экзамена")
    image = models.ImageField(upload_to='exam_images/', verbose_name="Изображение")
    participants = models.ManyToManyField(User, verbose_name="Участники экзамена")
    is_public = models.BooleanField(default=False, verbose_name="Опубликовано")

    def __str__(self):
        return self.name

