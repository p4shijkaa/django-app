from django.urls import path
from .views import DishDetailView, CategoryListView, DishListView, PopularDishesView

urlpatterns = [
	path('categories/', CategoryListView.as_view(), name='category_list'),
	path('dishes/', DishListView.as_view(), name='dish_list'),
	path('dishes/popular/', PopularDishesView.as_view(), name='popular_dishes'),
	path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish_detail'),
]