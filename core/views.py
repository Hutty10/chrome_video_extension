import os
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from django.db.models.manager import BaseManager
from rest_framework.generics import RetrieveAPIView
from django.core.files import File

from .models import VideoRecord, VideoByteChunk
from .serializers import VideoRecordSerializer, VideoChunkSerializer

# Create your views here.


class VideoCreateView(APIView):
    serializer_class = VideoChunkSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        video_chunk = serializer.save()
        video_id = data.get("video_id")
        print("title: ", data.get("video_title"))
        print("id: ", data.get("video_id"))

        try:
            video = VideoRecord.objects.get(id=video_id)
        except VideoRecord.DoesNotExist:
            VideoRecord.objects.get(title=data.get("video_title"))
        except VideoRecord.DoesNotExist:
            video = VideoRecord.objects.create(title=data.get("video_title"))
            video_dir = os.path.join(settings.MEDIA_ROOT, "videos")
            os.makedirs(video_dir, exist_ok=True)
            video_path = f"{video_dir}/{video.title}_{video.pk}.mp4"
            # import pdb;pdb.set_trace()
            ff = open(video_path, "+xb")
            video.video = video_path
            video.save()

            # print(ff)
        if video:
            video_chunk.video = video
            video_chunk.save()

        if video_chunk.is_last:
            chunks = VideoByteChunk.objects.filter(video=video).order_by("chunk_number")
            file = video.video.path
            # import pdb;pdb.set_trace()
            file_path = Path(file)
            with file_path.open(mode="ab") as video_file:
                for chunk in chunks:
                    chunk_file = chunk.chunk_file
                    # with open(chunk_file, "rb") as file:
                    chunk_byte = chunk_file.read()
                    video_file.write(chunk_byte)
        response = serializer.data
        response["video_id"] = video.pk
        return Response(response, status=status.HTTP_201_CREATED)


class GetVideo(APIView):
    def get(self, request, pk):
        try:
            video = VideoRecord.objects.get(pk=pk)
        except VideoRecord.DoesNotExist:
            return Response({"error": "invalid id"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VideoRecordSerializer(video)
        data = serializer.data
        video_dir = data.get("video").split("media")[-1]
        video_path = "media" + video_dir
        data["video"] = video_path

        return Response(data)
