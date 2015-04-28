from django import template
register = template.Library()
from django.core.urlresolvers import reverse_lazy
from users.models import Notification

def get_notifications(user_id):
  notifications = Notification.objects.filter(user_id=user_id, status=False)
  return notifications.order_by('-date')
  
register.filter('get_notifications', get_notifications)
