from rest_framework import serializers

from bills.models import BillInquiry


class BillsUploadSerializer(serializers.Serializer):  # noqa
    file = serializers.FileField()


class BillSerializer(serializers.ModelSerializer):
    service_class = serializers.CharField(source='service_class.name')

    class Meta:
        model = BillInquiry
        exclude = ('id',)
