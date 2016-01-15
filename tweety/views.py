from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import *
from rest_framework.decorators import api_view
from serializers import *
import json

# Create your views here.

def home(request):
	return render(request, 'home.html')

def test(request):
	"""
	jan = TweetyUser.objects[0]
	janusz = TweetyUser()
	janusz.first_name = 'janusz2'
	janusz.last_name = 'janusz2'
	janusz.email = 'janusz2@janusze.pl'
	janusz.username = 'januszzz2'
	janusz.following = [jan]
	janusz.save()
	"""
	usr = TweetyUser.objects
	serializer = TweetyUserSerializer(usr[0])
	return JsonResponse(usr[0].to_dict())


@api_view(['GET', 'POST'])
def user2(request):
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
