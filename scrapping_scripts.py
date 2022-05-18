from urllib.request import urlopen as uReq
import os
import sys
import django
from django.conf import settings
from bs4 import BeautifulSoup as soup



sys.path.append(
    os.path.join(os.path.dirname(__file__), 'schedularqualis')
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schedularqualis.settings")
django.setup()

from api.models import Holidays

my_url = "https://support.google.com/business/answer/6333474?hl=en"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, 'html.parser')
big_container = (page_soup.find("div",{"class":"cc"})).div
ps=big_container.findAll(['p','h2'])


for i in (range(1,len(ps),2)):
	pi=(str(ps[i+1])).strip('<p>')
	hi=(ps[i]).get_text()

	for item in pi.split('\n'):
		print(Holidays.objects.create(name=(item.split(':')[1]).strip('<br/>'),country_code=hi,date=(item.split(':')[0]).strip(' ')))
