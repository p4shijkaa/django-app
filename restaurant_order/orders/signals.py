# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Order, OrderItem
# from django.core.cache import cache
# from telegram_bot.utils import send_telegram_notification
#
# @receiver(post_save, sender=Order)
# def order_status_changed(sender, instance, created, **kwargs):
#     if not created and instance.status != instance._original_status:
#         # Отправка уведомления при изменении статуса
#         message = f"Статус заказа #{instance.id.hex[:6]} изменен на: {instance.get_status_display()}"
#         send_telegram_notification(instance.user.telegram_chat_id, message)
#
#         # Инвалидация кеша аналитики
#         cache.delete_pattern('analytics_*')
#
# @receiver(post_save, sender=OrderItem)
# @receiver(post_delete, sender=OrderItem)
# def update_order_total(sender, instance, **kwargs):
#     # Пересчет суммы заказа при изменении состава
#     instance.order.save(force_save=True)
#
# # Сохраняем исходный статус для сравнения
# def save_original_status(sender, instance, **kwargs):
#     if instance.pk:
#         instance._original_status = Order.objects.get(pk=instance.pk).status
#
# post_save.connect(save_original_status, sender=Order)