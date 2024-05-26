from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from datetime import datetime
from .models import User, Video ,Car
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import VideoUploadForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
import json

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
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video_file']
            if Video.objects.filter(video_file=video_file).exists():
                messages.info(request, '該影片已存在。')
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
    import os
    import uuid
    filename = str(uuid.uuid4()) + '.mp4'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    with open(filepath, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)
    return settings.MEDIA_URL + filename

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
    search_results = []
    if request.method == 'GET':
        license_plate = request.GET.get('license_plate')
        date = request.GET.get('date')
        location = request.GET.get('location')
        
        date_obj = datetime.strptime(date, '%Y-%m-%d') if date else None
        
        if license_plate:
            search_results.extend(Car.objects.filter(license_plate=license_plate))
        if date_obj:
            next_day = date_obj + timedelta(days=1)
            search_results.extend(Car.objects.filter(date_time__gte=date_obj, date_time__lt=next_day))
        if location:
            search_results.extend(Car.objects.filter(location=location))
            
        if not search_results:
            message = "未查詢到符合的結果"
    return render(request, 'search.html', {'search_results': search_results, 'message': message})







