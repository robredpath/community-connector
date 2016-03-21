from django.db import models
import smtplib
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
	message_text_long = models.CharField(max_length=4000)
	message_text_short = models.CharField(max_length=160)
	sms_has_been_sent = models.BooleanField(default=False, editable=False)
	email_has_been_sent = models.BooleanField(default=False, editable=False)

	def __init__(self):
		# Try to send the message through both means, set the appropriate flags

		# TODO: Refactor to allow multiple communities per installation
		# For now, just send any message to everyone
		for user in ser.objects.all():
			subject = "New messages from %s" % COMMUNITY_NAME
			try:
				email_user(subject, message_text_long)
			except:
				pass
			else:
				email_has_been_sent = 1

		# Send the SMS

		# TODO: Integrate esendex API. We need to capture people's mobile numbers first!
		pass