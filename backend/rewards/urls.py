from django.urls import path
from .views import *

urlpatterns = [
    path('earn-points/', EarnedRewardView.as_view()), # For general cases
    path('purchase/', RewardPurchaseView.as_view()),
    path('submit-feedback/', RewardFeedbackView.as_view()),
    path('redeem-coupon/', RedeemCouponView.as_view()),
    path('use-coupon/', RedeemCouponView.as_view()),
    path('redeem-donation/', RedeemCouponView.as_view()),
    path('get-points/', GetPointsView.as_view()),
    path('get-all-history/', GetHistoryView.as_view()),
    path('get-user-info/', GetAllInfoView.as_view()),
    path('get-redemptions/', GetRedemptionView.as_view()),
    path('reward-system/', reward_system, name='reward_system')
]