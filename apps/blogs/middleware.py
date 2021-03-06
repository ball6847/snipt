from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from annoying.functions import get_object_or_None
import re, os

class BlogMiddleware:
    def process_request(self, request):
        request.blog_user = None
        
        """ catch HTTP_HOST """
        host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST')
 
        """
        if you deploy in port other than 80,
        HTTP_HOST may contains that port
        and we don't want it to appear here
        """
        host, port = host.split(':')
        
        if not port:
            port = 80
            
        " Setup ENV, we may need it in our app "
        os.environ['SNIPT_HOSTNAME'], os.environ['SNIPT_PORT'] = host, port
 
        """ blog_user parsing is not neccessary, since domain is match with settings """
        if host in ['127.0.0.1', 'localhost', settings.DOMAIN]:
            return
        
        """ try extracting blog_user from domain eg. username.snipt.net """
        matched = re.search('^([^\.]+)\.' + re.escape(settings.DOMAIN) + '$', host)

        """ we got it! """
        if (matched):
            blog_user = matched.group(1)
            
            """ now resolve blog_user to User Model """
            if '-' in blog_user:
                request.blog_user = get_object_or_None(User, username__iexact=blog_user)
                
                if request.blog_user is None:
                    request.blog_user = get_object_or_404(User, username__iexact=blog_user.replace('-', '_'))
                return
                
            request.blog_user = get_object_or_404(User, username__iexact=blog_user)
            return
        
        """    
        try searching for domain records
        i prefer not letting user has multiple domains for now, since current schema will kill server
        @todo support multiple domains per user, using separated domain object
        """
        request.blog_user = get_object_or_404(User, userprofile__is_pro=True, userprofile__blog_domain=host)
        return
