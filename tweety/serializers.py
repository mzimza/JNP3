from rest_framework.serializers import ModelSerializer
from tweety.models import *


class TweetyUserSerializer(ModelSerializer):
	class Meta:
		model = TweetyUser
		fields = ('id', 'first_name', 'last_name', 'email', 'fb_id')


class TweetSerializer(ModelSerializer):
	author = TweetyUserSerializer()

	class Meta:
		model = Tweet
		fields = ('id', 'author', 'text', 'date', 'likes', 'shares', 'replies')


