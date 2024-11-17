from django.contrib import admin

# Register your models here.
from .models import Reward, RedeemedItem

admin.site.register(Reward)
admin.site.register(RedeemedItem)