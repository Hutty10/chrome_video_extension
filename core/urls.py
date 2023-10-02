from django.urls import path
from .views import VideoCreateView, GetVideo, GetAllVideo


urlpatterns = [
    path("upload", VideoCreateView.as_view(), name="upload video"),
    path("videos", GetAllVideo.as_view(), name="get videos"),
    path("video/<int:pk>", GetVideo.as_view(), name="get video"),
]
