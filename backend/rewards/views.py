from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reward, RedeemedItem
from .serializers import *
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
class EarnedRewardView(APIView):
    def post(self, request):
        serializer = EarnedRewardSerializer(data = request.data)
        if serializer.is_valid():
            reward = Reward.objects.create(
                user_id=serializer.validated_data['user_id'],
                points_earned=serializer.validated_data['points_earned'],
                reward_description=serializer.validated_data['reward_description'],
                points_redeemed=0,
                earned_date=timezone.now()
            )
            reward.save()
            return Response({"message" : "Earned Points Operation Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RewardPurchaseView(APIView):
    def post(self, request):
        serializer = RewardPurchaseSerializer(data = request.data)
        if serializer.is_valid():
            points = _calculate_points(serializer.validated_data['price'])
            reward = Reward.objects.create(
                user_id=serializer.validated_data['user_id'],
                points_earned=points,
                reward_description=serializer.validated_data['reward_description'],
                points_redeemed=0,
                earned_date=timezone.now()
            )
            reward.save()
            message = "Rewarded {points} Points based on Purchase Operation Successful"
            return Response({"message" : message}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def _calculate_points(price): # Simple Helper function for Reward Purchase api call
        return int(price * 2)

class RewardFeedbackView(APIView):
    def post(self, request):
        serializer = RewardFeedbackSerializer(data = request.data)
        if serializer.is_valid():
            reward = Reward.objects.create(
                user_id=serializer.validated_data['user_id'],
                points_earned = 10, # Flat Point Rewards for Feedback
                reward_description=serializer.validated_data['reward_description'],
                points_redeemed=0,
                earned_date=timezone.now()
            )
            reward.save()
            return Response({"message" : "Earned Points Operation Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RedeemCouponView(APIView):
    def post(self, request):
        serializer = RedeemCouponSerializer(data = request.data)
        if serializer.is_valid():
            reward = Reward.objects.create(
                user_id=serializer.validated_data['user_id'],
                points_earned=0,
                reward_description=serializer.validated_data['reward_description'],
                points_redeemed=serializer.validated_data['points_redeemed'],
                redeemed_date=timezone.now(),
                is_active=True
            )
            reward.save()
            unique_code = False
            item_code = ""
            while not unique_code:
                item_code = get_random_string(length=16)
                try:
                    item = RedeemedItem.objects.create(
                        item_code=item_code,
                        reward=reward,
                        amount=serializer.validated_data['coupon_amount'],
                        item_description=serializer.validated_data['reward_description']
                    )
                    unique_code = True
                    item.save()
                except IntegrityError:
                    continue
            return Response({"message" : "Coupon: " + item_code + " has been redeemed for " + str(serializer.validated_data['points_redeemed']) + " points."}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RedeemDonationView(APIView):
    def post(self, request):
        serializer = RedeemDonationSerializer(data = request.data)
        if serializer.is_valid():
            reward = Reward.objects.create(
                user_id=serializer.validated_data['user_id'],
                points_earned=0,
                reward_description=serializer.validated_data['reward_description'],
                points_redeemed=serializer.validated_data['points_redeemed'],
                redeemed_date=timezone.now(),
                is_active=False
            )
            reward.save()
            unique_code = False
            item_code = ""
            while not unique_code:
                item_code = get_random_string(length=16)
                try:
                    item = RedeemedItem.objects.create(
                        item_code=item_code,
                        reward=reward,
                        amount=serializer.validated_data['donation_amount'],
                        item_description=serializer.validated_data['reward_description']
                    )
                    unique_code = True
                    item.save()
                except IntegrityError:
                    continue
            return Response({"message" : "Donation of $" + str(serializer.validated_data['donation_amount']) + " has been redeemed for " + str(serializer.validated_data['points_redeemed']) + " points."}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UseCouponView(APIView):
    def post(self, request):
        serializer = UseCouponSerializer(data=request.data)
        if serializer.is_valid():
            item_code = serializer.validated_data['item_code'] 
            try:
                redeemed_item = RedeemedItem.objects.get(item_code=item_code)
                reward = redeemed_item.reward
                reward.is_active = False
                reward.save()

                return Response({"message": "Coupon used successfully."}, status=status.HTTP_200_OK)
            except RedeemedItem.DoesNotExist:
                return Response({"error": "Invalid item code."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetPointsView(APIView):
    def post(self, request):
        serializer = GetPointsSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            
            totals = Reward.objects.filter(user_id=user_id).aggregate(
                total_points_earned=Sum('points_earned'),
                total_points_redeemed=Sum('points_redeemed')
            )

            total_points_earned = totals['total_points_earned'] or 0
            total_points_redeemed = totals['total_points_redeemed'] or 0
            total_points = total_points_earned - total_points_redeemed

            return Response({
                "user_id": user_id,
                "total_points_earned": total_points_earned,
                "total_points_redeemed": total_points_redeemed,
                "total_points": total_points,
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetHistoryView(APIView):
    def post(self, request):
        serializer = GetHistorySerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            reward_history = Reward.objects.filter(user_id=user_id)
            reward_history_data = RewardHistorySerializer(reward_history, many=True).data
            
            return Response({
                "user_id": user_id,
                "reward_history": reward_history_data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllInfoView(APIView):
    def post(self, request):
        serializer = GetAllInfoSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            
            reward_history = Reward.objects.filter(user_id=user_id)
            reward_history_data = RewardHistorySerializer(reward_history, many=True).data

            totals = reward_history.aggregate(
                total_points_earned=Sum('points_earned'),
                total_points_redeemed=Sum('points_redeemed')
            )

            total_points_earned = totals['total_points_earned'] or 0
            total_points_redeemed = totals['total_points_redeemed'] or 0
            total_points = total_points_earned - total_points_redeemed

            return Response({
                "user_id": user_id,
                "total_points_earned": total_points_earned,
                "total_points_redeemed": total_points_redeemed,
                "total_points": total_points,
                "reward_history": reward_history_data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetRedemptionView(APIView):
    def post(self, request):
        serializer = GetRedemptionSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']

            rewards = Reward.objects.filter(user_id=user_id, redeemeditem__isnull=False)
            rewards_data = RewardWithRedemptionSerializer(rewards, many=True).data
            
            return Response({
                "user_id": user_id,
                "redemption_history": rewards_data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Front-End View
def reward_system(request):
    return render(request, 'reward_system.html')

