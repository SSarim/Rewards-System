Setup commands:
python -m venv venv <!--- Set up virtual env --->
pip install -r requirements.txt <!--- Install Django and other libraries --->

To run backend server:
cd backend
python manage.py runserver

API Calls:
rewards-api/earn-points/     --- Expects post with { user_id: INTEGER, points_earned: INTEGER, reward_description: STRING } <!--- General Purpose, can be used for Bonus Points --->
rewards-api/purchase/        --- Expects post with { user_id: INTEGER, reward_description: STRING, price: DOUBLE }
rewards-api/submit-feedback/ --- Expects post with { user_id: INTEGER, reward_description: STRING }
rewards-api/redeem-coupon/   --- Expects post with { user_id: INTEGER, points_redeemed: INTEGER, reward_description: STRING, amount: DOUBLE }
rewards-api/redeem-donation/ --- Expects post with { user_id: INTEGER, points_redeemed: INTEGER, reward_description: STRING, donation_amount: DOUBLE }
rewards-api/use-coupon/      --- Expects post with { item_code: STRING } <!--- Uses secondary key as coupon code, uses reward attribute, makes it inactive --->
rewards-api/get-points/      --- Expects post with { user_id: INTEGER } <!--- Goes through all reward history and calculates remaining points --->
rewards-api/get-all-history/ --- Expects post with { user_id: INTEGER } <!--- POTENTIALLY NOT REQUIRED Returns all user rewards accumulation and redemption history --->
<!--- Ex Return: return_history: [{'points_earned': 50, 'points_redeemed': 0, 'earned_date': '2024-11-05T12:58:33.973288-05:00', 'redeemed_date': None, 'reward_description': 'Purchased Item #230'}, {'points_earned': 0, 'points_redeemed': 50, 'earned_date': None, 'redeemed_date': '2024-11-10T17:03:03.471627-05:00', 'reward_description': 'Redeemed Coupon for $5.00'}] --->
rewards-api/get-user-info/   --- Expects post with { user_id: INTEGER } <!--- Returns remaining points and all user rewards accumulation and redemption history, for user profile and admin dashboard --->
rewards-api/get-redemptions/ --- Expects post with { user_id: INTEGER } <!--- Returns all user redeemed coupons and donations, with their active/inactive status --->