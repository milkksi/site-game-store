from django.shortcuts import render
from .models import smexam

def smexam_list(request):
    exams = smexam.objects.filter(is_public=True)
    return render(request, 'smexam.html', {'exams': exams})
