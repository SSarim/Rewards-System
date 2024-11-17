from django.db import models

class Reward(models.Model):
    reward_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField() # We don't require a user table for our api, we assume the api calls are made from validated users, and are properly constructed
    points_earned = models.IntegerField()
    points_redeemed = models.IntegerField()
    reward_description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False) # Only True if there's an associated Item with it
    earned_date = models.DateTimeField(blank=True, null=True) # can be nullable, if we are only redeeming something
    redeemed_date = models.DateTimeField(blank=True, null=True) # can filter to get redeemed items by searching for rewards that have a redeemed_date

class RedeemedItem(models.Model):
    item_code = models.CharField(unique=True, max_length=16, null=True) # Max 16 char coupon code, for example
    reward = models.OneToOneField(Reward, on_delete=models.CASCADE, primary_key=True)
    amount = models.FloatField(null=True)
    item_description = models.CharField(max_length=255) # Can be "Coupon: $5" Or "Donation: Tree" for example
