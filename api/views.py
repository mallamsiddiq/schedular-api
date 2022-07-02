import numpy as np
import json

import coreapi

from django.db.models import Q
from django.utils.dateparse import parse_datetime

from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend

from .serializers import HolidaySerializer,ScheduleSerializer
from .models import Holidays

#fuction to be called on each time slot
def do_with_each_req(req,pass_req): 	# a funtion to evaluate if any holiday falls within the provided timt range
	req['fr']=req['from'] 				# from is in the test input and i dont want to change it but it clahes with python built in from
	fr=parse_datetime(req['from'])		# so i create a key 'fr' that conforms with our serializer key
	to=parse_datetime(req['to'])		# parse strint to python datetime 

	if (to-fr).days==np.busday_count(fr.date(),to.date()) and {fr.weekday(),to.weekday()}&{5,6}==set(): # first check for weekend
		if not Holidays.objects.filter(Q(country_code=req['CC'])&((Q(date__date__gte=fr.date()) & Q(date__date__lte=to.date())))).exists(): # check against database holidays
			pass_req.append(req) 		# append slot to array if it passes all test


#a class to make the 'cc' ry param field visisble to swagger docuentation UI
class SimpleFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field( name='cc', location='query', required=False, type='string')]

 #the main class
class SchedulesView(generics.ListCreateAPIView):
	filter_backends = (SimpleFilterBackend,)
	queryset = Holidays.objects.all()
	def get_serializer_class(self):
		if self.request.method == "GET":
			return HolidaySerializer
		return ScheduleSerializer
	def list(self, request, *args, **kwargs):
		query_cc=request.GET.get('cc') 
		if request.GET.get('cc'):
			snippets = self.queryset.filter(Q(country_code=query_cc.upper())) 	#filter holidays based on cc query params
			if snippets.exists():
				serializer = HolidaySerializer(snippets, many=True) 
				return Response(serializer.data)
			return Response('you ve provided a wrong value ==>> eg: CC=Us for united states',status=status.HTTP_204_NO_CONTENT)

		return Response("""kindly provide a lookup parameter "cc" to check all holidays basd on your contry contry code 

							in the format ==>> e.g. ?cc=US Fof united states""" , status=status.HTTP_204_NO_CONTENT)

	def post(self, request,format=None, *args, **kwargs):
		# serializer = ScheduleSerializer(data=request.data)
		pass_req=[]
		try:
			if not request.data: # on empty requests
				return Response('empty request',status.HTTP_400_BAD_REQUEST)


			if isinstance(request.data,list): 		# if input is a list of  time slots
				for req in request.data: 			# loop through slots and evalute each
					do_with_each_req(req,pass_req)	# call the evaluating function 
			else:
				do_with_each_req(request.data,pass_req) # if a sigle slot was provided
		except KeyError:
			return Response(f' check provided keys, some might be missing or inproperly configured @ the object {req} ', 
				status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(f' you might be serving us a wrong input as ::{e}',status=status.HTTP_400_BAD_REQUEST)
		if len(pass_req)==0: 						#if all no available slot was provided
			return Response('all provided times are clashing with holidays/weekends on our register',
				status=status.HTTP_204_NO_CONTENT)

		serializer = ScheduleSerializer(data=pass_req, many=True)
		if serializer.is_valid():
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)