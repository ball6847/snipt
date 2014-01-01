from django.contrib.auth import authenticate, login
from django.template.defaultfilters import slugify
from registration.signals import user_registered
from pygments.lexers import get_all_lexers


def slugify_uniquely(value, model, slugfield="slug"):
    suffix = 0
    potential = base = slugify(value)[:255]

    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not model.objects.filter(**{slugfield: potential}).count():
            return potential
        suffix += 1

def activate_user(user, request, **kwargs):
    user.is_active = True
    user.save()

    user = authenticate(username=request.POST['username'],
                        password=request.POST['password1'])
    login(request, user)

def get_lexers_list():
    lexers = list(get_all_lexers())

    for l in lexers:
        if l[0] == 'ANTLR With Java Target':
            lexers.remove(l)

    lexers.append(('Markdown', ('markdown',),))
    lexers = sorted(lexers)

    return lexers

user_registered.connect(activate_user)
