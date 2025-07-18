from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum

from menu.models import Dish
from users.models import User


class Table(models.Model):
	number = models.PositiveIntegerField(unique=True)
	capacity = models.PositiveIntegerField()
	is_available = models.BooleanField(default=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return f"Столик #{self.number} ({self.capacity} персон)"


class Order(models.Model):
	ORDER_STATUS = (
		('pending', 'Ожидает подтверждения'),
		('confirmed', 'Подтвержден'),
		('preparing', 'Готовится'),
		('ready', 'Готов к выдаче'),
		('delivered', 'Доставлен'),
		('cancelled', 'Отменен'),
	)

	ORDER_TYPE = (
		('dine_in', 'В заведении'),
		('takeaway', 'На вынос'),
		('delivery', 'Доставка'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
	order_type = models.CharField(max_length=20, choices=ORDER_TYPE, default='dine_in')
	table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	comment = models.TextField(blank=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"Заказ №{self.id}"

	def calculate_total_price(self):
		return self.items.aggregate(
			total=Sum(F('quantity') * F('dish__price'))
		)['total'] or 0

	def save(self, *args, **kwargs):
		if not self.pk:
			self.total_price = self.calculate_total_price()
		super().save(*args, **kwargs)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def save(self, *args, **kwargs):
		if not self.price:
			self.price = self.dish.price
		super().save(*args, **kwargs)
		self.order.save()

	def __str__(self):
		return f"{self.dish.price}*{self.quantity}"
