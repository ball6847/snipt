from django.conf.urls import *

import views


urlpatterns = patterns('',

    # Redirects
    url(r'^s/(?P<snipt_key>[^/]+)/(?P<lexer>[^\?]+)?$',    views.redirect_snipt,    name='redirect-snipt'),
    url(r'^(?P<username>[^/]+)/feed/$',                    views.redirect_user_feed,     name='redirect-feed'),
    url(r'^public/tag/(?P<tag_slug>[^/]+)/feed/$',         views.redirect_public_tag_feed, name='redirect-public-tag-feed'),
    url(r'^(?P<username>[^/]+)/tag/(?P<tag_slug>[^/]+)/feed/$', views.redirect_user_tag_feed, name='redirect-user-tag-feed'),

    url(r'^public/$',                                      views.list_public,       name='list-public'),
    url(r'^public/tag/(?P<tag_slug>[^/]+)/$',              views.list_public,       name='list-public-tag'),
    url(r'^download/(?P<snipt_key>[^/]+).*$',              views.download,          name='download'),
    url(r'^embed/(?P<snipt_key>[^/]+)/$',                  views.embed,             name='embed'),
    url(r'^raw/(?P<snipt_key>[^/]+)/(?P<lexer>[^\?]+)?$',  views.raw,               name='raw'),
    url(r'^(?P<username_or_custom_slug>[^/]+)/$',          views.list_user,         name='list-user'),
    url(r'^(?P<username_or_custom_slug>[^/]+)/tag/(?P<tag_slug>[^/]+)/$', views.list_user, name='list-user-tag'),
    url(r'^(?P<username>[^/]+)/favorites/$',               views.favorites,         name='favorites'),
    url(r'^(?P<username>[^/]+)/blog-posts/$',              views.blog_posts,        name='blog-posts'),
    url(r'^(?P<username>[^/]+)/(?P<snipt_slug>[^/]+)/$',   views.detail,            name='detail'),

)
