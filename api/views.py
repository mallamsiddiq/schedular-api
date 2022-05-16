import numpy as np
import json


from django.db.models import Q
from django.utils.dateparse import parse_datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import HolidaySerializer,ScheduleSerializer
from .models import Holidays

def do_with_each_req(req,pass_req):
	req['fr']=req['from']
	fr=parse_datetime(req['from'])
	to=parse_datetime(req['to'])

	if (to-fr).days==np.busday_count(fr.date(),to.date()) and {fr.weekday(),to.weekday()}&{5,6}==set():
		if not Holidays.objects.filter(Q(country_code=req['CC'])&((Q(date__date__gte=fr.date()) & Q(date__date__lte=to.date())))).exists():
			pass_req.append(req)


class SchedulesView(APIView):
	def get(self, request, format=None):
		query_cc=request.GET.get('cc')
		if request.GET.get('cc'):
			snippets = Holidays.objects.filter(Q(country_code=query_cc.upper()))
			if snippets.exists():
				serializer = HolidaySerializer(snippets, many=True) 
				return Response(serializer.data)
			return Response('you ve provided a wrong value ==>> eg: CC=Us for united states',status=status.HTTP_204_NO_CONTENT)

		return Response("""kindly provide a lookup parameter "cc" to check all holidays basd on your contry contry code 

							in the format ==>> e.g. ?cc=US Fof united states""" , status=status.HTTP_204_NO_CONTENT)

	def post(self, request, format=None):
		pass_req=[]
		try:
			if not request.data:
				return Response('empty request',status.HTTP_400_BAD_REQUEST)


			if isinstance(request.data,list):
				for req in request.data:
					do_with_each_req(req,pass_req)
			else:
				do_with_each_req(request.data,pass_req)
		except KeyError:
			return Response(f' check provided keys, some might be missing or inproperly configured @ the object {req} ', 
				status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(f' you might be serving us a wrong input as ::{e}',status=status.HTTP_400_BAD_REQUEST)
		if len(pass_req)==0:
			return Response('all provided times are clashing with holidays/weekends on our register',
				status=status.HTTP_204_NO_CONTENT)

		serializer = ScheduleSerializer(data=pass_req, many=True)
		if serializer.is_valid():
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)