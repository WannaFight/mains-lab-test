from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bills.views import BillViewSet

router = DefaultRouter()
router.register(r'bills', BillViewSet, basename='bills')

urlpatterns = [
    path('', include(router.urls))
]
