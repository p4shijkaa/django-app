from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Category, Dish


@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
	cache.delete('all_categories')


@receiver(post_save, sender=Dish)
def update_dish_popularity(sender, instance, created, **kwargs):
	if created or not instance.is_available:
		cache.delete_pattern('popular_dishes_*')
