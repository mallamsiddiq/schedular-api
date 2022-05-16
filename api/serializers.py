from rest_framework import serializers


from .models import Holidays

class ScheduleSerializer(serializers.Serializer):
    fr = serializers.DateTimeField(source='from')
    to = serializers.DateTimeField()
    CC = serializers.CharField(max_length=200)

    def create(self, validated_data):
    	return (validated_data)


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = ["date","country_code","name"]