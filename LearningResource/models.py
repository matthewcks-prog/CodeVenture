from django.db import models
from django.core.exceptions import ValidationError

from . import youtube_utils


class VideoTutorial(models.Model):
    name = models.CharField(max_length=50, default='')
    video_id = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        """
        Validate that video_id looks like a real YouTube identifier or URL.
        """
        super().clean()
        if self.video_id:
            normalised = youtube_utils.extract_video_id(self.video_id)
            if normalised and not youtube_utils.is_valid_video_id(normalised):
                raise ValidationError(
                    {"video_id": "Enter a valid YouTube video ID or URL."}
                )

    def save(self, *args, **kwargs):
        """
        Normalise and persist a clean video ID so templates can rely on it.
        """
        if self.video_id:
            self.video_id = youtube_utils.extract_video_id(self.video_id)
        super().save(*args, **kwargs)

    @property
    def embed_url(self):
        """
        Return the fully-qualified YouTube embed URL or None.
        """
        return youtube_utils.build_embed_url(self.video_id)

    @property
    def watch_url(self):
        """
        Return the standard YouTube watch URL or None.

        This is used as a graceful fallback when embedding is not allowed
        by the video owner.
        """
        return youtube_utils.build_watch_url(self.video_id)

    @property
    def thumbnail_url(self):
        """
        Return a best-effort thumbnail URL for this video.

        Uses YouTube's public thumbnail endpoint which is fast, free,
        and does not require API keys.
        """
        return youtube_utils.build_thumbnail_url(self.video_id)


class LearningModule(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=50, unique=True, null=True)
    description = models.TextField()
    thumbnail = models.URLField(default='', null=True)

    def __str__(self):
        return self.name


class SubModule(models.Model):
    DIFFICULTY_CHOICES = [
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=50)
    parent_module = models.ForeignKey(LearningModule, related_name='sub_modules', on_delete=models.CASCADE)
    difficulty_level = models.CharField(
        max_length=15,
        choices=DIFFICULTY_CHOICES,
        default='Basic'
    )
    description = models.TextField()
    video = models.OneToOneField(VideoTutorial, on_delete=models.SET_NULL, null=True)
    prev_submodule = models.OneToOneField('SubModule', on_delete=models.SET_NULL, null=True, blank=True, related_name='prev_lecture')
    next_submodule = models.OneToOneField('SubModule', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_lecture')

    def __str__(self):
        return self.parent_module.short_name + ' - ' + self.name


class Badge(models.Model):
    name = models.CharField(max_length=50)
    icon_url = models.URLField()
    description = models.TextField()
