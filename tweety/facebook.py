from tweety.models import TweetyUser
from django.utils.crypto import get_random_string
import requests

FB_API_VERSION = 'v2.5'

FACEBOOK_API_URL = 'https://graph.facebook.com/' + FB_API_VERSION + '/me/'


def get_facebook_data(token, field_list='email,first_name,last_name,id'):
	content = {'access_token': token, 'fields': field_list}
	request = requests.get(FACEBOOK_API_URL, params=content)
	if request.status_code != 200:
		return None
	return request.json()


class FacebookBackend(object):
	@staticmethod
	def authenticate(token=None):
		if token is None:
			return None
		fb_dict = get_facebook_data(token=token, field_list=['id'])
		try:
			user = TweetyUser.objects.get(fb_id=fb_dict['id'])
			return user
		except TweetyUser.DoesNotExist:
			return None

	@staticmethod
	def get_user(user_id):
		try:
			return TweetyUser.objects.get(id=user_id)
		except TweetyUser.DoesNotExist:
			return None


def create_facebook_user(token):
	facebook_data = get_facebook_data(token)
	if facebook_data is None:
		return None
	password = get_random_string(length=24)
	user = TweetyUser(first_name=facebook_data['first_name'],
	                  last_name=facebook_data['last_name'],
	                  fb_id=facebook_data['id'],
	                  email=facebook_data['email'],
	                  password=password)
	return user

