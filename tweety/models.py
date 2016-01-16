from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import mongoengine
import cache
from datetime import datetime


class TweetyUser(cache.CachingModel, AbstractBaseUser):
	fb_id = models.BigIntegerField(default=0)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=50)
	date_joined = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True, null=False)
	is_staff = models.BooleanField(default=False, null=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	_prefix = 'U_'

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	def to_dict(self):
		from tweety.serializers import TweetyUserSerializer
		serializer = TweetyUserSerializer(self)
		return serializer.data

	@property
	def serializer(self):
		from tweety.serializers import TweetyUserSerializer
		return TweetyUserSerializer(self)

	@property
	def backend(self):
		return 'django.contrib.auth.backends.ModelBackend'


class Tweet(cache.CachingModel, models.Model):
	author = models.ForeignKey(TweetyUser)
	text = models.TextField(max_length=160)
	date = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)
	shares = models.IntegerField(default=0)
	popularity = models.IntegerField(default=0)
	origin = models.ForeignKey('Tweet', default=None, blank=True, null=True)

	@classmethod
	def cache_prefix(cls):
		return 'T_'

	def save(self, *args, **kwargs):
		print "tweet save"
		self.popularity = self.likes + self.shares
		return super(Tweet, self).save(*args, **kwargs)

	def to_dict(self):
		from tweety.serializers import TweetSerializer
		serializer = TweetSerializer(self)
		return serializer.data

	@property
	def serializer(self):
		from tweety.serializers import TweetSerializer
		return TweetSerializer(self)


class Report(mongoengine.Document):
	date = mongoengine.DateTimeField(default=datetime.now())
	tweets = mongoengine.IntField(default=0)
	users = mongoengine.IntField(default=0)