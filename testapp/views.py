from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from datetime import datetime, timedelta
from .models import User, Video, Car, Vehicle, Record
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import VideoUploadForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import Http404
from django.contrib.auth import logout
from django.conf import settings
import cv2, pytesseract, json, os
import numpy as np

def home(request):
    try:
        latest_video = Video.objects.latest('uploaded_at')
        context = {
            'latest_video_url': latest_video.video_file.url
        }
    except Video.DoesNotExist:
        context = {
            'latest_video_url': None
        }
    
    return render(request, 'home.html', context)
    
def submit_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '無效的登入資訊')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
    

def login_view(request):
    return render(request, 'login.html')
    
def submit_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video_file')
        if video_file:
            video = Video(video_file=video_file)
            video.save()
            return HttpResponse("Video uploaded successfully")
        else:
            return HttpResponse("No file uploaded", status=400)
    return render(request, 'upload_video.html')

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

def favicon_not_found(request):
    return HttpResponseNotFound()
    
def search(request):
    return render(request, 'search.html')
    
def car_input(request):
    if request.method == 'POST':
        license_plate = request.POST.get('license_plate').upper()
        date_time = request.POST.get('date_time')
        location = request.POST.get('location').upper()
        violation = request.POST.get('violation','')
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

    search_results = search_results.order_by('-id')
    
    for result in search_results:
        result.location = result.location.upper()
    
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
        
def submit_license_plate(request):
    if request.method == 'POST':
        license_plate = request.POST.get('license_plate').upper()
        return render(request, 'user_profile.html', {'user_email': request.user.email, 'license_plate': license_plate})
    else:
        return render(request, 'user_profile.html')
        
def update_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            updates = data.get('updates', [])
            for update in updates:
                record = Vehicle.objects.get(id=update['id'])
                record.license_plate = update['license_plate']
                record.date_time = update['date_time']
                record.location = update['location']
                record.violation = update['violation']
                record.save()
            return JsonResponse({'success': True})
        except Vehicle.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Record not found'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'})
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'success': False, 'message': 'Server error'})
    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def delete_record(request, id):
    if request.method == 'DELETE':
        try:
            record = Vehicle.objects.get(id=id)
            record.delete()
            return JsonResponse({'status': 'success'})
        except Vehicle.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Record not found'})
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'status': 'error', 'message': 'Server error'})
    return HttpResponseBadRequest('Invalid request method')

def record_detail(request, id):
    record = get_object_or_404(Car, id=id)

    try:
        latest_video = Video.objects.latest('uploaded_at')  
    except Video.DoesNotExist:
        latest_video = None  

    # 根据 record.id 设置视频 URL
    if record.id >= 1 and record.id <= 81:
        video_url = f"{settings.MEDIA_URL}videos/output_video.mp4"  # 使用 MEDIA_URL
    elif record.id > 81 and record.id <= 150:
        video_url = f"{settings.MEDIA_URL}videos/output_video2.mp4"  # 使用 MEDIA_URL
    else:
        video_url = None

    context = {
        'record': record,
        'latest_video_url': video_url,  # 使用根据 record.id 选择的视频 URL
        'start_seconds': record.seconds if record.seconds else 0  
    }

    return render(request, 'record_detail.html', context)



