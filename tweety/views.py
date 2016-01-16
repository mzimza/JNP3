from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.views.decorators.csrf import *
from rest_framework.decorators import api_view
from django_q.tasks import async
from serializers import *
import facebook
import tasks


# Create your views here.

def login(request):
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


def report(request):
	async(tasks.create_report, sync=True, hook=tasks.report_ready)
	return HttpResponse(status=200)


@api_view(['POST'])
@transaction.atomic
def user_facebook(request):
	if request.method == 'POST':
		token = request.data.get('token', None)
		if token is not None:
			user = facebook.create_facebook_user(token=token)
			if user is not None:
				created = False
				try:
					user_db = TweetyUser.objects.filter(fb_id=user.fb_id)[0]
				except IndexError:
					user.save()
					created = True
					user_db = TweetyUser.objects.filter(fb_id=user.fb_id)[0]
				if not request.user.is_authenticated():
					django_login(request, user_db)
				if created:
					return HttpResponse(status=201)
				else:
					return HttpResponse(status=200)
	return HttpResponse(status=400)


@api_view(['GET', 'POST'])
@transaction.atomic
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
@transaction.atomic
def user(request, id):
	try:
		usr = TweetyUser.objects.filter(id=id)[0]
	except IndexError, TweetyUser.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		return JsonResponse(usr.to_dict())

	elif request.method == 'PUT':
		serializer = TweetyUserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(usr)
			return HttpResponse(status=201)
		else:
			return HttpResponse(status=400)

	elif request.method == 'DELETE':
		if request.user.id == id:
			usr.delete()
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=401)


@api_view(['GET', 'POST'])
@transaction.atomic
def tweet_getpost(request):
	if request.method == 'GET':
		users = Tweet.objects
		serializer = TweetSerializer(users, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		serializer = TweetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return HttpResponse(status=201)
		else:
			print serializer.errors
			return HttpResponse(status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@transaction.atomic
def tweet(request, id):
	try:
		tweet = Tweet.objects.filter(id=id)[0]
	except IndexError, Tweet.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		return JsonResponse(tweet.to_dict())

	elif request.method == 'PUT':
		serializer = TweetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(tweet)
			return HttpResponse(status=201)
		else:
			return HttpResponse(status=400)

	elif request.method == 'DELETE':
		if tweet.author == request.user:
			tweet.delete()
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=401)


@api_view(['GET'])
@transaction.atomic
def wall(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			tweets = Tweet.objects.filter(author=request.user)
			serializer = TweetSerializer(tweets, many=True)
			return JsonResponse(serializer.data, safe=False)
		else:
			return HttpResponse(status=401)
	else:
		return HttpResponse(status=400)


@api_view(['POST'])
@transaction.atomic
def like(request, id):
	if request.method == 'POST' and request.user.is_authenticated():
		try:
			tweet = Tweet.objects.filter(id=id).exclude(author=request.user)[0]
			tweet.likes += 1
			tweet.save()
			return HttpResponse(status=200)
		except IndexError, Tweet.DoesNotExist:
			pass
	return HttpResponse(status=400)


@api_view(['POST'])
@transaction.atomic
def retweet(request, id):
	if request.method == 'POST' and request.user.is_authenticated():
		try:
			tweet = Tweet.objects.filter(id=id).exclude(author=request.user)[0]
			tweet.shares += 1
			tweet.save()
			new_tweet = Tweet()
			new_tweet.text = tweet.text
			new_tweet.author = request.user
			new_tweet.origin = tweet
			new_tweet.save()
			return HttpResponse(status=201)
		except IndexError, Tweet.DoesNotExist:
			pass
	return HttpResponse(status=400)


def home(request):
	return render(request, 'wall.html')


@api_view(['GET'])
def popular(request):
	if request.method == 'GET':
		tweets = Tweet.objects.order_by('-popularity')[:10]
		serializer = TweetSerializer(tweets, many=True)
		return JsonResponse(serializer.data, safe=False)
	return HttpResponse(status=400)
