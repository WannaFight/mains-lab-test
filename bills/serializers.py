from rest_framework import serializers

from bills.models import BillInquiry


class BillsUploadSerializer(serializers.Serializer):  # noqa
    file = serializers.FileField()


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillInquiry
        exclude = ('id',)
