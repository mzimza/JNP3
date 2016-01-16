from rest_framework.serializers import *
from tweety.models import *


class TweetyUserSerializer(ModelSerializer):
	class Meta:
		model = TweetyUser
		fields = ('id', 'first_name', 'last_name', 'email', 'fb_id')


class TweetSerializer(ModelSerializer):
	author = TweetyUserSerializer(required=False)
	text = CharField(required=True, max_length=160)
	date = DateTimeField(read_only=True)
	likes = IntegerField(read_only=True)
	shares = IntegerField(read_only=True)
	replies = IntegerField(read_only=True)
	origin = PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Tweet
