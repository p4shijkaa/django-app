from django.core.cache import cache
from django.db import models
from django.db.models import Count
from django.utils.text import slugify


class Category(models.Model):
	name = models.CharField(max_length=25)
	slug = models.SlugField(max_length=25)
	order = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=False)

	class Meta:
		ordering = ['order']
		verbose_name_plural = 'Категории'

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
		cache.delete('all_categories')


class Dish(models.Model):
	name = models.CharField(max_length=30)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
	is_available = models.BooleanField(default=True)
	cooking_time = models.PositiveIntegerField(help_text='Время приготовления в минутах')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	popularity = models.IntegerField(default=0)

	class Meta:
		ordering = ['-popularity', 'name']
		verbose_name_plural = "Блюда"

	def __str__(self):
		return f"{self.name} - {self.price} руб."

	@classmethod
	def get_popular_dishes(cls, limit=5):
		cache_key = f'popular_dishes_{limit}'
		popular_dishes = cache.get(cache_key)

		if not popular_dishes:
			popular_dishes = cls.objects.annotate(
				order_count=Count('order_items')
			).filter(
				is_available=True
			).order_by(
				'-order_count', '-popularity'
			)[:limit]

			cache.set(cache_key, popular_dishes, 60 * 60)

		return popular_dishes
		