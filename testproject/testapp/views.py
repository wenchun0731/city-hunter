from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from datetime import datetime
from .models import User, Video
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import VideoUploadForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
import json

def home(request):
    return render(request, 'home.html')

    
def index(request):
    return render(request, 'login.html')
    
def submit_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email, password=password).exists():
            return render(request, 'upload_video.html')
        else:
            user = User.objects.create_user(email=email, password=password)
            user.save()
            return render(request, 'upload_video.html')
    else:
        return render(request, 'login.html')


def login_view(request):
    return render(request, 'login.html')
    
def submit_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video_file']
            if Video.objects.filter(video_file=video_file).exists():
                messages.info(request, 'The video already exists.')
                return HttpResponseRedirect(reverse('submit_video'))
            else:
                new_video = form.save()
                video_url = new_video.video_file.url
                return HttpResponseRedirect(reverse('submit_video') + '?video_url=' + video_url)
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')

def favicon_not_found(request):
    return HttpResponseNotFound()
    
def search(request):
    return render(request, 'search.html')

