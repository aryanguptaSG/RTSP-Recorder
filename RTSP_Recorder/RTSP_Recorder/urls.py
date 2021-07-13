from django.contrib import admin
from django.urls import path
from Api import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('health_check', views.health_check),
    path('health_check/name=<str:Name>', views.health_check),
    path('store_urls', views.store_urls),
    path('start', views.start),
    path('stop', views.stop),
    path('getpath', views.getpath),
    path('corrupt_checker',views.corrupt_checker),
]
