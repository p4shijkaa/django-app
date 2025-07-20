from django.core.cache import cache
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order, Table
from .serializers import OrderSerializer, CreateOrderSerializer, TableSerializer


class TableListView(generics.ListAPIView):
	queryset = Table.objects.filter(is_available=True)
	serializer_class = TableSerializer


class OrderViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['status', 'order_type']

	def get_queryset(self):
		user = self.request.user
		queryset = Order.objects.filter(user=user).prefetch_related('items__dish')

		if user.is_staff:
			queryset = Order.objects.all().prefetch_related('items__dish')

		return queryset

	def get_serializer_class(self):
		if self.action == 'create':
			return CreateOrderSerializer
		return OrderSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def list(self, request, *args, **kwargs):
		cache_key = f"user_orders_{request.user.id}"
		cached_orders = cache.get(cache_key)

		if cached_orders:
			return Response(cached_orders)

		response = super().list(request, *args, **kwargs)
		cache.set(cache_key, response.data, 60 * 5)  # Кешируем на 5 минут
		return response


class StaffOrderViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	http_method_names = ['get', 'push', 'patch']

	def get_queryset(self):
		return Order.objects.filter(
			Q(status='pending') | Q(status='preparing')
		).order_by('created_at')
