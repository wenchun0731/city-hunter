from django.contrib import admin
from django.urls import path
from testapp.views import index, submit_login, login_view, submit_video, success_view, favicon_not_found, home, car_input, search

from django.conf import settings
from django.conf.urls.static import static
from testapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('submit_login/', submit_login, name='submit_login'),
    path('submit_video/', submit_video, name='submit_video'),
    path('login/', login_view, name='login'),
    path('success/', success_view, name='success_url'),
    path('favicon.ico', favicon_not_found),
    path('login/', views.login_view, name='login'),
    path('upload_video/', views.submit_video, name='upload_video'),
    path('car_input/', car_input, name='car_input'),
    path('search/', search, name='search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

