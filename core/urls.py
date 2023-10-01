from django.urls import path
from .views import VideoCreateView, GetVideo


urlpatterns = [
    path("upload", VideoCreateView.as_view(), name="upload video"),
    path("video/<int:pk>", GetVideo.as_view(), name="get video"),
]
