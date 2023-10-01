from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


def video_dir(instance, filename):
    return "videos/{0}".format(filename)


class VideoRecord(models.Model):
    title = models.CharField(_("video record"), max_length=50)
    video = models.FileField(
        _("video file"), upload_to=video_dir, blank=True, null=True
    )
    caption = models.TextField(blank=True, null=True)
    # video_url = models.FilePathField(_("video url"), path=None, match=None, recursive=recursive, max_length=100)

    created_at = models.DateTimeField(_("date created"), auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}   {self.pk}"


def chunk_dir(instance, filename):
    return "video_chunks/{0}".format(filename)


class VideoByteChunk(models.Model):
    video = models.ForeignKey(
        VideoRecord, on_delete=models.CASCADE, blank=True, null=True
    )
    chunk_number = models.PositiveSmallIntegerField(_("chunk number"))
    chunk_file = models.FileField(_("video chunk"), upload_to=chunk_dir)
    is_last = models.BooleanField(_("last chunk"), default=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)

    class Meta:
        ordering = ["chunk_number"]

    def __str__(self) -> str:
        return f"chunk number: {self.chunk_number}, belong to {self.video}"
