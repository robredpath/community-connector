from django.apps import AppConfig

class CommunityConfig(AppConfig):
	name = 'community'
	verbose_name = "Community"

	def ready(self):
		import community.signals.handlers