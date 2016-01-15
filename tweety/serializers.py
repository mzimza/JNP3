from rest_framework_mongoengine.serializers import DocumentSerializer
from tweety.models import *
from bson.objectid import ObjectId, InvalidId


class TweetSerializer(DocumentSerializer):
	class Meta:
		model = Tweet
		fields = ('id', 'text', 'date', 'likes', 'shares', 'replies')


class TweetyUserSerializer(DocumentSerializer):
	class Meta:
		model = TweetyUser
		fields = ('id', 'username', 'first_name', 'last_name', 'email', 'fb_id')
		tweets = TweetSerializer(many=True)

	def validate_following(self, value):
		try:
			for id in value:
				usr = TweetyUser.objects(id=ObjectId(id))[0]
		except InvalidId, TweetyUser.DoesNotExist:
			raise ValidationError('User does not exist')
		return value

	def validate_followers(self, value):
		try:
			for id in value:
				usr = TweetyUser.objects(id=ObjectId(id))[0]
		except InvalidId, TweetyUser.DoesNotExist:
			raise ValidationError('User does not exist')
		return value