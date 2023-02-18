import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

product = stripe.Product.create(name="my_product")