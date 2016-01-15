from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from mongoengine.django.auth import User as mongoUser
from datetime import datetime


class Tweet(Document):
	text = StringField(max_length=160)
	date = DateTimeField(default=datetime.now())
	likes = IntField(default=0)
	shares = IntField(default=0)

	def to_dict(self):
		from tweety.serializers import TweetSerializer
		serializer = TweetSerializer(self)
		return serializer.data


class TweetyUser(mongoUser):
	tweets = EmbeddedDocumentListField('Tweet')
	fb_id = LongField(default=0)
	email = EmailField(unique=True)
	#followers = ListField(ReferenceField('TweetyUser', reverse_delete_rule=1))
	#following = ListField(ReferenceField('TweetyUser', reverse_delete_rule=1))

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	def to_dict(self):
		from tweety.serializers import TweetyUserSerializer
		serializer = TweetyUserSerializer(self)
		return serializer.data