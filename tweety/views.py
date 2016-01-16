from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from mongoengine.django.auth import *
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import *
from rest_framework.decorators import api_view
from serializers import *
import facebook
import json

# Create your views here.

def home(request):
	return render(request, 'home.html')

def test(request):
	"""
	#jan = TweetyUser.objects[0]
	janusz = TweetyUser()
	janusz.first_name = 'janusz2'
	janusz.last_name = 'janusz2'
	janusz.email = 'janusz2@janusze.pl'
	janusz.username = 'januszz2'
	janusz.save()

	#usr = TweetyUser.objects
	#serializer = TweetyUserSerializer(usr[0])
	#return JsonResponse(usr[0].to_dict())

	#janusz = TweetyUser.objects[0]
	#janusz.backend = 'mongoengine.django.auth.MongoEngineBackend'
	#login(request, janusz)
	#x = authenticate(username=janusz.username, password=janusz.password)

	#print x
	"""
	return HttpResponse(status=200)


@api_view(['POST'])
def user_facebook(request):
	if request.method == 'POST':
		token = request.data.get('token', None)
		if token is not None:
			user = facebook.create_facebook_user(token=token)
			print user
			if user is not None:
				created = False
				if len(TweetyUser.objects.filter(fb_id=user.fb_id)) == 0:
					user.save()
					created = True
				auth.login(request, user)
				if created:
					return HttpResponse(status=201)
				else:
					return HttpResponse(status=200)
	return HttpResponse(status=400)


@api_view(['GET', 'POST'])
def user_getpost(request):
	if request.method == 'GET':
		users = TweetyUser.objects
		serializer = TweetyUserSerializer(users, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		serializer = TweetyUserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return HttpResponse(status=201)
		else:
			return HttpResponse(status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def user(request, id):
	try:
		usr = TweetyUser.objects(id=ObjectId(id))[0]
	except InvalidId, TweetyUser.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		return JsonResponse(usr.to_dict())

	elif request.method == 'PUT':
		serializer = TweetyUserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return HttpResponse(status=201)
		else:
			return HttpResponse(status=400)

	elif request.method == 'DELETE':
		usr.delete()
		return HttpResponse(status=204)
