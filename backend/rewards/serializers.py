from rest_framework import serializers
from .models import Reward, RedeemedItem

class EarnedRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['user_id', 'points_earned', 'reward_description']

class RewardPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['user_id', 'reward_description', 'price']
        extra_kwargs = {
            'price' : {'required': True, 'allow_null': False}
        }

class RewardFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['user_id', 'reward_description']

class RedeemCouponSerializer(serializers.ModelSerializer):
    coupon_amount = serializers.FloatField(write_only=True)
    class Meta:
        model = Reward
        fields = ['user_id', 'points_redeemed', 'reward_description', 'coupon_amount']
        
class RedeemDonationSerializer(serializers.ModelSerializer):
    donation_amount = serializers.FloatField(write_only=True)
    class Meta:
        model = Reward
        fields = ['user_id', 'points_redeemed', 'reward_description', 'donation_amount']

class UseCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedeemedItem
        fields = ['item_code']

class GetPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['user_id']

class GetHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['user_id']

class RewardHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['points_earned', 'points_redeemed', 'earned_date', 'redeemed_date', 'reward_description']

class GetAllInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['user_id']

class GetRedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['user_id']

class RedeemedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedeemedItem
        fields = ['item_code', 'amount', 'item_description']

class RewardWithRedemptionSerializer(serializers.ModelSerializer):
    redeemed_item = RedeemedItemSerializer(source='redeemeditem', read_only=True)
    class Meta:
        model = Reward
        fields = ['redeemed_date', 'is_active', 'redeemed_item']