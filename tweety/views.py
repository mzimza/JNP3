from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from rest_framework.decorators import api_view
from django_q.tasks import async
from serializers import *
from django.core.cache import cache
import facebook
import json


# Create your views here.

def login(request):
	return render(request, 'home.html')


def logout(request):
	if request.user.is_authenticated():
		django_logout(request)
		return HttpResponse(status=200)
	return HttpResponse(status=400)


def home(request):
	if request.user.is_authenticated():
		return render(request, 'wall.html', context={'user': request.user})
	else:
		return redirect('login')


def report(request):
	async('tasks.create_report', hook='tasks.report_ready')
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
		tweets = Tweet.objects.order_by('-date')
		serializer = TweetSerializer(tweets, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		serializer = TweetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return HttpResponse(status=201)
		else:
			print serializer.errors
			return HttpResponse(status=400)


@api_view(['GET', 'DELETE'])
@transaction.atomic
def tweet(request, id):
	try:
		tweet = Tweet.get(id=id)
	except IndexError, Tweet.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		return JsonResponse(tweet)

	elif request.method == 'DELETE':
		id = tweet.get('id', None)
		if id is not None:
			tweet = Tweet.objects.get(id=id)
			if tweet.author == request.user:
				tweet.delete()
				return HttpResponse(status=204)
		return HttpResponse(status=401)


@api_view(['GET'])
@transaction.atomic
def wall(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			tweets_ids = Tweet.objects.filter(author=request.user).values('id').order_by('-date')
			tweets = []
			for val in tweets_ids:
				tweet = Tweet.get(id=val['id'])
				tweets.append(tweet)
			return JsonResponse(tweets, safe=False)
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


@api_view(['GET'])
def popular(request):
	if request.method == 'GET':
		popular_ids = cache.get('popular')
		if popular_ids is None:
			popular_ids = Tweet.objects.values('id').order_by('-popularity')[:10]
		else:
			popular_tweets = json.loads(popular_ids)
			return JsonResponse(popular_tweets, safe=False)
		tweets = []
		for val in popular_ids:
			tweet = Tweet.get(id=val['id'])
			tweets.append(tweet)
		cache.set('popular', json.dumps(tweets), 3)
		return JsonResponse(tweets, safe=False)
	return HttpResponse(status=400)


@api_view(['GET'])
def newest(request):
	if request.method == 'GET':
		newest_ids = cache.get('newest')
		if newest_ids is None:
			newest_ids = Tweet.objects.values('id').order_by('-date')[:10]
		else:
			newest_tweets = json.loads(newest_ids)
			return JsonResponse(newest_tweets, safe=False)
		tweets = []
		for val in newest_ids:
			tweet = Tweet.get(id=val['id'])
			tweets.append(tweet)
		cache.set('newest', json.dumps(tweets), 3)
		return JsonResponse(tweets, safe=False)
	return HttpResponse(status=400)