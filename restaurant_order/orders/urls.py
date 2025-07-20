from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TableListView, OrderViewSet, StaffOrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'staff/orders', StaffOrderViewSet, basename='staff-order')

urlpatterns = [
	path('tables/', TableListView.as_view(), name='table-list'),
	path('', include(router.urls))
]