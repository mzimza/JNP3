from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import mongoengine
import cache
import dateutil.parser
from datetime import datetime


class TweetyUserManager(BaseUserManager):
	def create_user(self, first_name, last_name, email, password=None):
		if not email or not first_name or not last_name:
			raise ValueError()

		user = self.model(first_name=first_name, last_name=last_name, email=self.normalize_email(email),)
		user.is_active = True
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, first_name, last_name, email, password):
		user = self.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class TweetyUser(cache.CachingModel, AbstractBaseUser, PermissionsMixin):
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

	objects = TweetyUserManager()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	def to_dict(self):
		from tweety.serializers import TweetyUserSerializer
		serializer = TweetyUserSerializer(self)
		return serializer.data

	def get_full_name(self):
		fullname = self.first_name + ' ' + self.last_name
		return fullname

	def get_short_name(self):
		return self.first_name

	@property
	def serializer(self):
		from tweety.serializers import TweetyUserSerializer
		return TweetyUserSerializer(self)

	@property
	def backend(self):
		return 'django.contrib.auth.backends.ModelBackend'


class Tweet(cache.CachingModel, models.Model):
	author = models.ForeignKey(TweetyUser,  db_index=True)
	text = models.TextField(max_length=160)
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	likes = models.IntegerField(default=0)
	shares = models.IntegerField(default=0)
	popularity = models.IntegerField(default=0)
	origin = models.ForeignKey('Tweet', default=None, blank=True, null=True)

	_prefix = 'T_'

	def save(self, *args, **kwargs):
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

	def __unicode__(self):
		return unicode(str(self.author), 'utf-8') + ', ' + str(self.date) + ': ' + self.text

	@classmethod
	def from_dict(cls, **kwargs):
		try:
			print kwargs
			tweet = Tweet()
			tweet.author = TweetyUser.from_dict(kwargs.pop('author', None))
			tweet.text = kwargs.pop('text')
			tweet.date = dateutil.parser.parse((kwargs.pop('date')))
			tweet.likes = kwargs.pop('likes')
			tweet.shares = kwargs.pop('shares')
			tweet.popularity = kwargs.pop('popularity')
			tweet.origin = kwargs.pop('')
			return tweet
		except KeyError:
			return None

	@property
	def prefix(self):
		return self._prefix


class Report(mongoengine.Document):
	date = mongoengine.DateTimeField(default=datetime.now())
	tweets = mongoengine.IntField(default=0)
	users = mongoengine.IntField(default=0)
