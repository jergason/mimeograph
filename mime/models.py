from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class MimeographProfile(models.Model):
    user = models.OneToOneField(User)
    following = models.ManyToManyField('self', symmetrical=False,
    through='Following')

    def __unicode__(self):
        return "%s Mimeograph Profile" % self.user.username

    def create_mimeograph_profile(sender, instance, created, **kwargs):
        if created:
            MimeographProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


class Following(models.Model):
    follower = models.ForeignKey(MimeographProfile, related_name='follower')
    followee = models.ForeignKey(MimeographProfile, related_name='followee')

    def __unicode__(self):
        return "%s is following %s" % (self.followee.username,
                self.follower.username)

#TODO: figure out how to do many to one in the list
class List(models.Model):
    name = models.CharField(max_length=201)

class Mime(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    pub_date = models.DateTimeField('date posted')

    def __unicode__(self):
        return "by %s on %s" % (self.author.username, self.pub_date)
