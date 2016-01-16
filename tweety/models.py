from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class TweetyUser(AbstractBaseUser):
	fb_id = models.BigIntegerField(default=0)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=50)
	date_joined = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True, null=False)
	is_staff = models.BooleanField(default=False, null=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	def to_dict(self):
		from tweety.serializers import TweetyUserSerializer
		serializer = TweetyUserSerializer(self)
		return serializer.data

	@property
	def backend(self):
		return 'django.contrib.auth.backends.ModelBackend'

class Tweet(models.Model):
	author = models.ForeignKey(TweetyUser)
	text = models.TextField(max_length=160)
	date = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)
	shares = models.IntegerField(default=0)

	def to_dict(self):
		from tweety.serializers import TweetSerializer
		serializer = TweetSerializer(self)
		return serializer.data
