from rest_framework import serializers
from .models import VideoRecord, VideoByteChunk


class VideoRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoRecord
        fields = "__all__"
        extra_kwargs = {
            "created_at": {"read_only": True},
        }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ff = representation['video'] 
        if ff:
            representation['video'] = 'media'+ff.split('media')[-1]
        # import pdb;pdb.set_trace()
        return representation


class VideoChunkSerializer(serializers.ModelSerializer):
    # video_id = serializers.IntegerField(required=False)
    # video_title = serializers.CharField(required=False)

    class Meta:
        model = VideoByteChunk
        fields = [
            # "video_id",
            # "video_title",
            "chunk_number",
            "chunk_file",
            "is_last",
            "created_at",
        ]
