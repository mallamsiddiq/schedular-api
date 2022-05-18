from django.urls import reverse, resolve
from api.views import SchedulesView
from django.test import SimpleTestCase


class TestUrls(SimpleTestCase):
	def test_urls_resolv(self): # testing resolve match
		url=reverse('schedules') 
		print(resolve(url))
		self.assertEquals(resolve(url).func.view_class,SchedulesView)