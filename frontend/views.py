from django.shortcuts import render
from .models import FrontImage, Page


def home_view(request):
    image = FrontImage.objects.all()
    pages = Page.objects.all()
    return render(request, 'frontend/pages/home.html',
                  {'image': image,
                   'pages': pages})