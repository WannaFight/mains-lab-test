import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, MultiPartParser, \
    FormParser
from rest_framework.response import Response

from bills.models import BillInquiry
from bills.serializers import BillSerializer, BillsUploadSerializer
from bills.services import process_bills_dataframe, \
    create_bill_inquiries_from_df


class BillViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin):
    serializer_class = BillSerializer

    def get_queryset(self) -> QuerySet[BillInquiry]:
        queryset = BillInquiry.objects.all()

        client_org = self.request.query_params.get('client_org')
        client_name = self.request.query_params.get('client_name')

        if client_org:
            queryset = queryset.filter(client_org__iexact=client_org)
        if client_name:
            queryset = queryset.filter(client_name__iexact=client_name)

        return queryset

    @action(methods=['post'], detail=False, url_path="upload-excel",
            serializer_class=BillsUploadSerializer,
            parser_classes=[MultiPartParser, FormParser, FileUploadParser])
    def upload_excel_with_bills(self, request, *args, **kwargs):
        file_obj: InMemoryUploadedFile = request.data['file']
        df = pd.read_excel(file_obj.file, index_col=None)  # noqa
        df = process_bills_dataframe(df)
        create_bill_inquiries_from_df(df)
        return Response(status=status.HTTP_201_CREATED)
