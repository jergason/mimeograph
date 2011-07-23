from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms

class MimeographProfile(models.Model):
    user = models.OneToOneField(User)
    following = models.ManyToManyField('self', symmetrical=False,
    through='Following')

    def __unicode__(self):
        return "%s" % self.user.username

    def create_mimeograph_profile(sender, instance, created, **kwargs):
        if created:
            #If is is just create, then loading data from fixtures will break.
            # We use get_or_create so when a user and profile is loaded
            # from a fixture it doesn't try to automatically create another
            # MimeographProfile and run into non-unique primary key problems.
            prof, res = MimeographProfile.objects.get_or_create(user=instance)

            # Each new user follows themselves so their own posts show
            # up  in their feed.
            Following.objects.get_or_create(follower=prof, followee=prof)

    post_save.connect(create_mimeograph_profile, sender=User)

    def get_all_followees(self):
        return [f.followee for f in
                Following.objects.filter(follower=self)]

    def get_all_followers(self):
        return [f.follower for f in
                Following.objects.filter(followee=self)]



class Following(models.Model):
    follower = models.ForeignKey(MimeographProfile, related_name='follower')
    followee = models.ForeignKey(MimeographProfile, related_name='followee')

    def __unicode__(self):
        return "%s is following %s" % (self.follower.user.username,
                self.followee.user.username)


#TODO: figure out how to do many to one in the list
class List(models.Model):
    name = models.CharField(max_length=201)

class Mime(models.Model):
    author = models.ForeignKey(MimeographProfile)
    content = models.TextField()
    pub_date = models.DateTimeField('date posted')

    def __unicode__(self):
        return "by %s on %s" % (self.author.username, self.pub_date)

class MimeForm(forms.Form):
    content = forms.CharField(min_length=1, label="Upload a photo")
