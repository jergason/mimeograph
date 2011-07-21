from django.db import models
from django.contrib.auth.models import User

class MimeographProfile(models.Model):
    user = models.OneToOneField(User)
    following = models.ManyToManyField('self', symmetrical=False,
    through='Following')


class Following(models.Model):
    follower = models.ForeignKey(MimeographProfile, related_name='follower')
    followee = models.ForeignKey(MimeographProfile, related_name='followee')

class List(models.Model):
    name = models.CharField(max_length=201)

class Mime(models.Model):
    content = models.ForeignKey(User)
    text = models.TextField()
    pub_date = models.DateTimeField('date posted')
