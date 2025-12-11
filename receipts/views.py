from django.shortcuts import render
from rest_framework import generics
from .models import Receipt
from .serializers.common import ReceiptSerializer
from .filters import ReceiptFilter
from django_filters.rest_framework import DjangoFilterBackend


class ReceiptListCreateView(generics.ListCreateAPIView):
    queryset = Receipt.objects.all().prefetch_related("items")
    serializer_class = ReceiptSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReceiptFilter


class ReceiptDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all().prefetch_related("items")
    serializer_class = ReceiptSerializer

