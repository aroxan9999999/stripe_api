from django.urls import path, include
from .views import *


urlpatterns = [
    path('', product_list, name='list'),
    path('item/<int:pk>', product_detail, name='item'),
    path('buy/<int:pk>', productbuyview, name='buy'),
    path('category/<int:pk>', category_list, name='category'),
    path('buy', order, name='buy_order'),
    path('session/<int:pk>', CreateCheckoutSession.as_view(), name='session'),
    path('session/', CreateCheckoutSession.as_view(), name='session_order'),
    path('success', succesView, name='success'),
    path('cancel', cancelview, name='cancel'),
]
