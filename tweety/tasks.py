from tweety.models import *
from datetime import datetime


# report generator
def create_report():
	report = Report()
	report.date = datetime.now()
	report.tweets = Tweet.objects.count()
	report.users = TweetyUser.objects.count()
	return report


def report_ready(task):
	if task.success:
		task.result.save()
	else:
		print 'not succes'
