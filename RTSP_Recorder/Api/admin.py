from django.contrib import admin

from .models import Recording,Camera

# Register your models here.
@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['name','url','status','active_hours']


@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ['name','path','status','datetime']
