from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from mime.models import Following, Mime, MimeForm
from datetime import datetime
from mimeograph_utils import get_flash_messages, error_for_get_to_post_url, set_flash_message

@login_required
def own_feed(request):
    followees = Following.objects.filter(follower=request.user)

    #TODO: remove self from followees
    followees = request.user.get_profile().get_all_followees()

    #get most recent posts by followees ordered by time
    posts = {}
    posts = Mime.objects.filter(author__in=followees).order_by('-pub_date')[:10]
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
    #if they are trying to look at their own page, then
    #show the correct one
    if request.user.username == user_name:
        return redirect('mime.views.own_feed')
    if user.count() == 0:
        # request.session['flash']['error'] = "Feed for %s not found" % user_name
        raise Http404
    else:
        user = user[0]
        posts = Mime.objects.filter(author=user)
        is_current_user_following = Following.objects.filter(follower=User.objects.get(username=request.username),
                followee=User.objects.get(username=user_name)).exists()
        return render_to_response('feed.html',
                { 'u': user, 'posts': posts, 'other_user': user_name,
                    'is_current_user_following': is_current_user_following,
                    'flash': get_flash_messages(request) },
            context_instance=RequestContext(request))

@login_required
def follow(request):
    if request.method == "POST":
        followee_id = request.POST['id']
        #TODO: make sure they are not already following
        following, already_follow = Following.objects.get_or_create(followee=MimographProfile.objects.get(pk=followee_id), follower=request.user.get_profile())
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
        form = MimeForm(request.POST)
        if form.is_valid():
            #process data, create the Mime, set the session and redirect
            mime = Mime(author=request.user.get_profile(),
                    content=form.cleaned_data['content'],
                    pub_date=datetime.now())
            mime.save()
            set_flash_message(request, 'success', "Mime successfully posted.")
            print("Mime created, and here is flash:")
            print(request.session['flash'])
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
