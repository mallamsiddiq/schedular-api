from django.urls import reverse, resolve
from api.views import SchedulesView
from django.test import TestCase, Client
from api.models import Holidays
import json


class TestUrls(TestCase):

	def setUp(self):
		self.client=Client()
		self.url=reverse('schedules') 

		self.payload_1=[{
			"from": "2021-12-24T00:00:00Z",
			"to": "2021-12-26T12:00:00Z",
			"CC":"NG"
		}]
		self.payload_2={
			"from": "2021-12-27T00:00:00Z",
			"to": "2021-12-27T00:00:00Z",
			"CC":"NG"
			}
		

		with open('data/holidays.json', 'r') as file:
			holdays = json.load(file)
			Holidays.objects.bulk_create([Holidays(name=holiday['name'],
				country_code=holiday['country_code'],
				date=holiday['date']) for holiday in holdays])
		with open('data/input.json', 'r') as file:
			self.sched_slots = json.load(file)



	def load_data(self,payload,code):
		response = self.client.post(self.url,payload,content_type='application/json')
		self.assertEquals(response.status_code,code)
		return response


	def test_get(self):
		response=self.client.get(self.url,{'cc':'nG'})
		self.assertEquals(response.status_code,200)
		response=self.client.get(self.url)
		self.assertEquals(response.status_code,204)  

	def test_mixed_post(self):
		response=self.load_data(self.sched_slots,200)
		self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{
                        "fr": "2023-05-02T03:30:00Z",
                         "to": "2023-05-02T11:30:00Z",
                         "CC": "NG"
                         }]
             )

	def test_invalid_post(self):
		self.load_data([],400)
		self.load_data([{}],400)
		self.load_data([{"random":"random"}],400)

	def test_singles_post(self):
		self.load_data(self.payload_1,204)
		self.load_data((self.payload_1)[0],204)
		self.load_data(self.payload_2,200)


