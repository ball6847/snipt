from accounts.models import UserProfile
from blogs.views import blog_list
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from annoying.decorators import ajax_request, render_to
from django.shortcuts import render_to_response
from django.template import RequestContext
from snipts.utils import get_lexers_list
from django.contrib.auth.models import User
from django.db.models import Count
from snipts.models import Snipt
from taggit.models import Tag

import hashlib
import stripe

from django.conf import settings

@render_to('homepage.html')
def homepage(request):

    if request.blog_user:
        return blog_list(request)

    coders = []

    users_with_gravatars = User.objects.filter(
        userprofile__in=UserProfile.objects.filter(has_gravatar=True)
    ).order_by('?')

    for user in users_with_gravatars:
        public_snipts_count = Snipt.objects.filter(
            user=user, public=True).values('pk').count()

        if public_snipts_count:
            user.email_md5 = hashlib.md5(user.email.lower()).hexdigest()
            coders.append(user)

        if len(coders) == 35:
            break

    return {
        'coders': coders,
        'snipts_count': Snipt.objects.all().count(),
        'users_count': User.objects.all().count(),
    }


@ajax_request
def lexers(request):
    lexers = get_lexers_list()
    objects = []

    for l in lexers:

        try:
            filters = l[2]
        except IndexError:
            filters = []

        try:
            mimetypes = l[3]
        except IndexError:
            mimetypes = []

        objects.append({
            'name': l[0],
            'lexers': l[1],
            'filters': filters,
            'mimetypes': mimetypes
        })

    return {'objects': objects}


def login_redirect(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/' + request.user.username + '/')
    else:
        return HttpResponseRedirect('/')


@login_required
@render_to('pro-signup.html')
def pro_signup(request):
    if request.user.profile.is_pro:
        return HttpResponseRedirect('/' + request.user.username + '/')
    return {}


@login_required
@render_to('pro-signup-complete.html')
def pro_signup_complete(request):

    if request.method == 'POST':

        token = request.POST['token']
        stripe.api_key = settings.STRIPE_SECRET_KEY

        plan = 'snipt-pro-monthly'

        customer = stripe.Customer.create(card=token,
                                          plan=plan,
                                          email=request.user.email)

        profile = request.user.profile
        profile.is_pro = True
        profile.stripe_id = customer.id
        profile.save()

        return {}

    else:
        return HttpResponseBadRequest()


def sitemap(request):

    tags = Tag.objects.filter(snipt__public=True)
    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count')[:1000]

    return render_to_response('sitemap.xml',
                              {'tags': tags},
                              context_instance=RequestContext(request),
                              mimetype='application/xml')


@render_to('tags.html')
def tags(request):

    all_tags = Tag.objects.filter(snipt__public=True).order_by('name')
    all_tags = all_tags.annotate(count=Count('taggit_taggeditem_items__id'))

    popular_tags = Tag.objects.filter(snipt__public=True)
    popular_tags = popular_tags.annotate(
        count=Count('taggit_taggeditem_items__id'))
    popular_tags = popular_tags.order_by('-count')[:20]
    popular_tags = sorted(popular_tags, key=lambda tag: tag.name)

    return {
        'all_tags': all_tags,
        'tags': popular_tags
    }