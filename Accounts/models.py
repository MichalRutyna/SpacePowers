from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def user_to_inactive(sender, instance, created, update_fields, **kwargs):
    if created:
        #instance.active = False
        try:
            my_group = Group.objects.get(name='Confirmed User')
            my_group.user_set.add(instance)
        except Group.DoesNotExist:
            pass
