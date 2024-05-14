import datetime
from django.db import models
from django.conf import settings
import boto3
from pathlib import Path
from urllib.parse import urlparse, unquote


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    last_viewed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="last_viewed_posts",
        null=True,
    )
    last_viewed_datetime = models.DateTimeField(
        default=datetime.datetime.now())

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.image_url:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
                region_name='ap-northeast-2'
            )
            bucket_name = 'next-session-14-bucket-hyunsung'
            key = urlparse(unquote(self.image_url)).path[1:]
            s3_client.delete_object(Bucket=bucket_name, Key=key)
        super().delete(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.content

    def delete(self, *args, **kwargs):
        if self.image_url:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
                region_name='ap-northeast-2'
            )
            bucket_name = 'next-session-14-bucket-hyunsung'
            key = urlparse(unquote(self.image_url)).path[1:]
            s3_client.delete_object(Bucket=bucket_name, Key=key)
        super().delete(*args, **kwargs)


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscribers"
    )
