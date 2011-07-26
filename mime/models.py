from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms
from datetime import datetime

class MimeographProfile(models.Model):
    user = models.OneToOneField(User)
    following = models.ManyToManyField('self', symmetrical=False, through='Following')

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

    def get_all_followees(self, include_self=False):
        """Get all users that are followed by this user excluding
        themselves."""
        followees = [f.followee for f in Following.objects.filter(follower=self)]
        if include_self:
            return followees
        else:
            return filter(lambda x: x.user.username != self.user.username, followees)

    def get_all_followees_without_self(self):
        return self.get_all_followees(False)

    def get_all_followers(self, include_self=False):
        """Get all users that follow this user besides themselves."""
        followers = [f.follower for f in Following.objects.filter(followee=self)]
        if include_self:
            return followers
        else:
            return filter(lambda x: x.user.username != self.user.username, followers)

    def get_all_followers_without_self(self):
        return self.get_all_followers(False)

    def number_of_followers(self, include_self=False):
        return len(self.get_all_followers(include_self))

    def number_of_followees(self, include_self=False):
        return len(self.get_all_followees(include_self))

    def most_recent_post_content(self):
        """Get the content of the most recent post by this user, or return None if they have
        no posts."""
        if self.mime_set.all().exists():
            return self.mime_set.all().order_by('-pub_date')[0].content
        else:
            return None



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
    pub_date = models.DateTimeField('date posted', default=datetime.now())

    def __unicode__(self):
        return "by %s on %s" % (self.author.user.username, self.pub_date)

class MimeForm(forms.Form):
    content = forms.FileField(label="Upload an image.")
