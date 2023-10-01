from django.contrib import admin

from .models import VideoRecord, VideoByteChunk

# Register your models here.
admin.site.register(VideoRecord)
admin.site.register(VideoByteChunk)
