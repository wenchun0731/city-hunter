from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from datetime import datetime, timedelta
from .models import User, Video ,Car
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import VideoUploadForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
import cv2, pytesseract , json, os
import numpy as np

def home(request):
    try:
        latest_video = Video.objects.latest('video_file') 
        context = {
            'latest_video_url': latest_video.video_file.url
        }
        return render(request, 'home.html', context)
    except ObjectDoesNotExist:
        return render(request, 'home.html')
    
def index(request):
    return render(request, 'login.html')
    
def submit_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email, password=password).exists():
            return render(request, 'car_input.html')
        else:
            user = User.objects.create_user(email=email, password=password)
            user.save()
            return render(request, 'car_input.html')
    else:
        return render(request, 'login.html')


def login_view(request):
    return render(request, 'login.html')
    
def submit_video(request):
    message = None
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video_file']
            if video_exists(video_file.name):
                message = "該影片已存在"
                return HttpResponseRedirect(reverse('submit_video'))
            else:
                video = Video(video_file=video_file)
                video.save()
                video_url = handle_uploaded_video(video_file)
                return HttpResponseRedirect(reverse('submit_video') + '?video_url=' + video_url)
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})

def handle_uploaded_video(video_file):
    from django.conf import settings
    filepath = os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name)  
    with default_storage.open(filepath, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)
    return settings.MEDIA_URL + 'videos/' + video_file.name

def video_exists(filename):
    from django.conf import settings
    return default_storage.exists(os.path.join(settings.MEDIA_ROOT, 'videos', filename))


def success_view(request):
    return render(request, 'success.html')

def favicon_not_found(request):
    return HttpResponseNotFound()
    
def search(request):
    return render(request, 'search.html')
    
def car_input(request):
    if request.method == 'POST':
        license_plate = request.POST.get('license_plate')
        date_time = request.POST.get('date_time')
        location = request.POST.get('location')
        violation = request.POST.get('violation') == 'true'
        car = Car.objects.create(
            license_plate=license_plate,
            date_time=date_time,
            location=location,
            violation=violation
        )
        messages.success(request, '車輛資訊已成功輸入。')
        return render(request, 'car_input.html')
    else:
        return render(request, 'car_input.html')

def search(request):
    message = None
    search_results = Car.objects.all()
    
    if request.method == 'GET':
        license_plate = request.GET.get('license_plate')
        date = request.GET.get('date')
        location = request.GET.get('location')
        
        if license_plate:
            search_results = search_results.filter(license_plate=license_plate)
        if date:
            search_results = search_results.filter(date_time__date=date)
        if location:
            search_results = search_results.filter(location=location)
            
        if not search_results.exists():
            message = "未查詢到符合的結果"
            
    return render(request, 'search.html', {'search_results': search_results, 'message': message})



def process_image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image = request.FILES['image']
            image_path = 'static/image.jpg'
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            img = cv2.imread(image_path)
            text = '辨識結果'
            response_data = {'text': text}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Image file is missing'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
