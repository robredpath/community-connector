from django.db import models

class Message(models.Model):
	message_text_long = models.CharField(max_length=4000)
	message_text_short = models.CharField(max_length=160)
	sms_has_been_sent = models.BooleanField(default=False, editable=False)
	email_has_been_sent = models.BooleanField(default=False, editable=False)
