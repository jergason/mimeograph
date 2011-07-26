from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from mime.models import Following, Mime, MimeForm, MimeographProfile
from datetime import datetime
from mimeograph_utils import *
from os import remove

@login_required
def own_feed(request):
    followees = Following.objects.filter(follower=request.user)

    followees = request.user.get_profile().get_all_followees(True)
    # This should work. Need to look more at closures in python. What is their scope like?

    #get most recent posts by followees ordered by time
    posts = Mime.objects.filter(author__in=followees).order_by('-pub_date')
    form = MimeForm()

    return render_to_response('own_feed.html',
            {
                'u': request.user,
                'mimes': posts,
                'followees': followees,
                'form': form,
                'flash': get_flash_messages(request)
            },
            context_instance=RequestContext(request))


def other_feed(request, user_name):
    """Look at a user's feed of posts. If the user is logged in, then they will
    be able to follow the user and those they follow."""
    user = User.objects.filter(username=user_name)
    #if they are trying to look at their own page, then show the correct one
    if request.user.username == user_name:
        return redirect('mime.views.own_feed')
    if user.count() == 0:
        set_flash_message(request, 'error', "Feed for %s not found." % user_name)
        return redirect('mime.views.own_feed')
    else:
        user = user[0]
        posts = Mime.objects.filter(author=user)
        if request.user.is_authenticated():
            print("User is authenticated")
        is_current_user_following = Following.objects.filter(follower=User.objects.get(username=request.user.username), followee=User.objects.get(username=user_name)).exists() if request.user.is_authenticated() else False
        return render_to_response('other_feed.html',
                { 'u': user, 'posts': posts,
                    'other_user': user_name,
                    'other_user_id': User.objects.get(username=user_name).id,
                    'is_current_user_following': is_current_user_following,
                    'flash': get_flash_messages(request) },
            context_instance=RequestContext(request))

@login_required
def follow(request, user_name):
    if request.method == "POST":
        followee_id = request.POST['id']
        #TODO: make sure they are not already following
        #TODO: user the name from the URL, not the ID
        following, already_follow = Following.objects.get_or_create(followee=MimeographProfile.objects.get(pk=followee_id), follower=request.user.get_profile())
        following.save()
        set_flash_message(request, 'success', "You successfully followed %s." % MimeographProfile.objects.get(pk=followee_id).user.username)
    else:
        error_for_get_to_post_url(request)
    return redirect("mime.views.own_feed")


@login_required
def unfollow(request, user_name):
    if request.method == "POST":
        Following.objects.filter(follower=request.user.get_profile(),
                followee=MimeographProfile.objects.get(pk=request.POST['id'])).delete()
        set_flash_message(request, 'succes', "Sucessfully unfollowed %s." %
                user_name)
    else:
        error_for_get_to_post_url(request)
    return redirect('mime.views.own_feed')



@login_required
def mime_create(request):
    if request.method == "POST":
        form = MimeForm(request.POST, request.FILES)
        if form.is_valid():
            #process data, create the Mime, set the session and redirect
            img = handle_uploaded_image(request.FILES['content'])
            mime = Mime(author=request.user.get_profile(), content=img)
            mime.save()
            set_flash_message(request, 'success', "Mime successfully posted.")
        else:
            set_flash_message(request, 'error', "Invalid input data. Try again with more valid data.")
    else:
        error_for_get_to_post_url(request)
    return redirect('mime.views.own_feed')

@login_required
def mime_delete(request):
    #make sure the user is trying to delete their own mime.
    #if not, set a flash notice and redirect.
    #TODO: catch DoesNotExist errors
    if request.method == "POST":
        mime = Mime.objects.get(pk=request.POST['id'])
        if mime.author != request.user.get_profile():
            set_flash_message(request, 'error', "You sneaky dog! You can't delete a Mime that isn't yours!")
        else:
            mime.delete()
            set_flash_message(request, 'success', "Successfully deleted mime.")
    else:
        error_for_get_to_post_url(request)
    return redirect('mime.views.own_feed')


def get_follows(request, user_name, followers_or_followees):
    """Will call get_followers or get_followees depending on the value of the
    last argument. Cut down on code duplication."""
    #redirect to last page if there is no user for user_name
    if not User.objects.filter(username=user_name).exists():
        set_flash_message(request, 'warning', "No user named %s exists." % user_name)
        return redirect('mime.views.own_feed')

    #Forgive the long lines. Don't quite have my hand around
    # python formatting rules yet, and Laziness is also a factor.
    u = User.objects.get(username=user_name)
    user_is_following = Following.objects.filter(follower=request.user.get_profile(),followee=u.get_profile()).exists() if (request.user.is_authenticated()) else False
    user_id = u.get_profile().id

    follows = []
    follow_word = ''
    if followers_or_followees == "followers":
        follows = u.get_profile().get_all_followers(False)
        follow_word = 'following'
    elif followers_or_followees == "followees":
        follows = u.get_profile().get_all_followees(False)
        follow_word = 'being followed by'
    else:
        raise ValueError("currently only supports 'followers' or 'followees' as arguments.")

    return render_to_response('follow.html',
            {
                'follow_word': follow_word,
                'user_name': user_name,
                'logged_in_user_is_following': user_is_following,
                'user_profile_id': user_id,
                'follows': follows
            },
            context_instance=RequestContext(request))

def get_followers(request, user_name):
    """Get all users following user_name and render them in a view."""
    return get_follows(request, user_name, 'followers')

def get_following(request, user_name):
    """Get all users that user_name is following and render them in a view."""
    return get_follows(request, user_name, 'followees')

def handle_uploaded_image(f):
    """Save the uploaded file to a temporary directory, run the image
    processing code on it and return the string that represents the image."""
    destination = open("tmp/%s" % f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    image_as_ASCII = convert_image("tmp/%s" % f.name)
    remove("tmp/%s" % f.name)
    return image_as_ASCII
