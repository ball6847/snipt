from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from annoying.decorators import render_to
from snipts.models import Snipt

from django.contrib.auth.views import password_change

@login_required
@render_to('account.html')
def account(request):
    return {}

@login_required
@render_to('stats.html')
def stats(request):

    snipts = Snipt.objects.filter(user=request.user).order_by('-views')

    return {
        'snipts': snipts
    }