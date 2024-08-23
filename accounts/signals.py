from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer, Product,Portfolio





@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    instance.customer.save()   


# def update_profile(sender, instance, created, **kwargs): 
#      if created == False:
#             instance.Customer.save()
#             print('profile updated')
        
# post_save.connect(update_profile, sender=User)   

 
@receiver(post_save, sender=Product)
def notify_new_product(sender, instance, created, **kwargs):
    if created:
        # Store the new product in the cache
        cache.set('new_product', instance, timeout=60*60)  # Cache it for 1 hour


@receiver(post_save, sender=User)
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)