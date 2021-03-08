from django.db import models


class Tweet(models.Model):
    parent_tweet_id = models.IntegerField(default=None,null=True)
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    image_path = models.FileField(null=True)
    created_at = models.DateTimeField('created at')

    def __str__(self):
        return self.name