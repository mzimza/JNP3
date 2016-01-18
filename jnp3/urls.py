"""jnp3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tweety import views
from django.views.decorators.cache import cache_page
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
	url(r'^', include('favicon.urls')),
	url(r'^$', views.login, name="login"),
	url(r'^admin/', admin.site.urls),
	url(r'^report/$', cache_page(0)(views.report)),
	url(r'^newest/$', cache_page(1)(views.newest), name="newest"),
	url(r'^user/$', cache_page(3)(views.user_getpost), name="user"),
	url(r'^user_fb/$', cache_page(0)(views.user_facebook), name="user_fb"),
	url(r'^user/(?P<id>[\d]+)/$', cache_page(1)(views.user), name="user_id"),
	url(r'^tweet/$', cache_page(3)(views.tweet_getpost), name="tweet"),
	url(r'^tweet/(?P<id>[\d]+)/$', cache_page(1)(views.tweet), name="tweet_id"),
	url(r'^retweet/(?P<id>[\d]+)/$', cache_page(0)(views.retweet), name="retweet"),
	url(r'^wall/$', cache_page(0)(views.wall), name="wall"),
	url(r'^like/(?P<id>[\d]+)/$', cache_page(0)(views.like), name="like"),
	url(r'^home/$', cache_page(0)(views.home)),
	url(r'^popular/$', cache_page(5)(views.popular), name="popular"),
	url(r'^logout/$', cache_page(0)(views.logout), name="logout"),

	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(BASE_DIR, "static")})
]