from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.cache import cache
from django.db.models import F
from .models import Category, Dish
from .serializers import CategorySerializer, DishSerializer


class CategoryListView(generics.ListAPIView):
	serializer_class = CategorySerializer
	queryset = Category.objects.filter(is_active=True)

	def get_queryset(self):
		cache_key = 'all_categories'
		categories = cache.get(cache_key)

		if not categories:
			categories = super().get_queryset()
			cache.set(cache_key, categories, 60 * 60 * 24)
		return categories


class DishListView(generics.ListAPIView):
	serializer_class = DishSerializer
	filterset_fields = ['category', 'is_available']

	def get_queryset(self):
		result = Dish.objects.select_related('category').filter(
			is_available=True
		).annotate(
			category_name=F('category__name')
		).order_by('category__order', 'name')
		return result


class PopularDishesView(APIView):
	def get(self, request):
		limit = int(request.query_params.get('limit', 5))
		dishes = Dish.get_popular_dishes(limit)
		serializer = DishSerializer(dishes, many=True)
		return Response(serializer.data)


class DishDetailView(generics.RetrieveAPIView):
	queryset = Dish.objects.all()
	serializer_class = DishSerializer

	def retrieve(self, request, *args, **kwargs):
		dish = self.get_object()
		dish_popularity = F('popularity') + 1
		dish.save(update_fields=['popularity'])
		return super().retrieve(request, *args, **kwargs)