from rest_framework import serializers

from menu.models import Dish
from menu.serializers import DishSerializer
from .models import Order, OrderItem, Table


class TableSerializer(serializers.ModelSerializer):
	class Meta:
		model = Table
		fields = ['id', 'number', 'capacity', 'is_available']


class OrderItemSerializer(serializers.ModelSerializer):
	dish = DishSerializer(read_only=True)

	class Meta:
		model = OrderItem
		fields = ['id', 'dish', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
	items = OrderItemSerializer(many=True, read_only=True)
	table = TableSerializer(read_only=True)
	user = serializers.StringRelatedField()

	class Meta:
		model = Order
		fields = ['id', 'user', 'created_at', 'status', 'order_type',
				  'table', 'total_price', 'comment', 'items']
		read_only_fields = ['user', 'created_at', 'total_price']


class CreateOrderItemSerializer(serializers.ModelSerializer):
	dish_id = serializers.PrimaryKeyRelatedField(
		queryset=Dish.objects.filter(is_available=True),
		source='dish'
	)

	class Meta:
		model = OrderItem
		fields = ['dish_id', 'quantity']


class CreateOrderSerializer(serializers.ModelSerializer):
	items = CreateOrderItemSerializer(many=True)
	table_id = serializers.PrimaryKeyRelatedField(
		queryset=Table.objects.filter(is_available=True),
		source='table',
		required=False
	)

	class Meta:
		model = Order
		fields = ['order_type', 'table_id', 'comment', 'items']

	def create(self, validated_data):
		items_data = validated_data.pop('items')
		order = Order.objects.create(
			**validated_data,
			user=self.context['request'].user
		)

		for item_data in items_data:
			OrderItem.objects.create(order=order, **item_data)

		return order
