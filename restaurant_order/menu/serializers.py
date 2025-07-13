from rest_framework import serializers

from .models import Dish, Category


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name', 'slug', 'order']


class DishSerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only=True)

	class Meta:
		model = Dish
		fields = ['id', 'name', 'description', 'price', 'category',
			'is_available', 'cooking_time', 'popularity']
