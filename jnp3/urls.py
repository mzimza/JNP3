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
from django.conf.urls import url
from django.contrib import admin
from tweety import views

urlpatterns = [
	url(r'^$', views.login),
	url(r'^admin/', admin.site.urls),
	url(r'^test/$', views.test),
	url(r'^report/$', views.report),
	url(r'^user/$', views.user_getpost, name="user"),
	url(r'^user_fb/$', views.user_facebook, name="user_fb"),
	url(r'^user/(?P<id>[\d]+)/$', views.user, name="user_id"),
	url(r'^tweet/$', views.tweet_getpost, name="tweet"),
	url(r'^tweet/(?P<id>[\d]+)/$', views.tweet, name="tweet_id"),
	url(r'^retweet/(?P<id>[\d]+)/$', views.retweet, name="retweet"),
	url(r'^wall/$', views.wall, name="wall"),
	url(r'^like/(?P<id>[\d]+)/$', views.like, name="like"),
	url(r'^home/$', views.home),
	url(r'^popular/$', views.popular, name="popular"),
]
