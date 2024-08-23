from django.contrib import admin
from  accounts.models import *

# Register your models here.
admin.site.register(Register)
admin.site.register(Customer)
admin.site.register(RecoveryKeyRequest)
admin.site.register(ProfileApp)
admin.site.register(SocialApp)
admin.site.register(GiftCardPayment)
admin.site.register(CryptoTransaction)
admin.site.register(Holding)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer') 

@admin.register(DigitalKey)
class DigitalKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ('currency', 'address')