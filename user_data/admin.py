from django.contrib import admin

from user_data.models import Address, BankInfo, BrowserDetail, Client, CreditCard, Financial, SocialMeidia

# Register your models here.
admin.site.register(Client)
admin.site.register(Address)
admin.site.register(CreditCard)
admin.site.register(BankInfo)
admin.site.register(Financial)
admin.site.register(SocialMeidia)
admin.site.register(BrowserDetail)
