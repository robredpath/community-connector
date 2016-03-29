from django.db import models

class Message(models.Model):
	message_text_long = models.CharField(max_length=4000)
	message_text_short = models.CharField(max_length=160)
	sms_has_been_sent = models.BooleanField(default=False, editable=False)
	email_has_been_sent = models.BooleanField(default=False, editable=False)

	def __str__(self):
		return "Long message ({}): {} Short message ({}): {}".format('Sent' if self.email_has_been_sent else 'Unsent', 
																	self.message_text_long,
																	'Sent' if self.sms_has_been_sent else 'Unsent',
																	self.message_text_short
		 )


class Event(models.Model):
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	title = models.CharField(max_length=250)

	def __str__(self):
		return "{}: {} to {}".format(title, start_time, end_time)