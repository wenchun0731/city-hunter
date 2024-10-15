from django.contrib import admin
from django.urls import path
from testapp.views import (
    submit_login, login_view, submit_video, favicon_not_found, home, 
    car_input, search, process_image, submit_license_plate, delete_record, 
    update_record, record_detail, submit_video, logout_view
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('submit_login/', submit_login, name='submit_login'),
    path('upload_video/', submit_video, name='upload_video'),
    path('favicon.ico', favicon_not_found),
    path('car_input/', car_input, name='car_input'),
    path('search/', search, name='search'),
    path('process_image/', process_image, name='process_image'),
    path('submit_license_plate/', submit_license_plate, name='submit_license_plate'),
    path('delete_record/<int:id>/', delete_record, name='delete_record'),
    path('update_record/', update_record, name='update_record'),
    path('record/<int:id>/', record_detail, name='record_detail'),
    path('submit_video/', submit_video, name='submit_video'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

