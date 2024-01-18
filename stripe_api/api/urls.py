from django.urls import path
from .views import (BuyItemView, CancelView, ItemInfoView, HomePageData,
                    OrderView, SuccessView, PaymentView)


urlpatterns = [
    path('', HomePageData.as_view(), name='home_page'),
    path('buy/<int:id>/', BuyItemView.as_view(), name='buy'),
    path('item/<int:id>/', ItemInfoView.as_view(), name='item'),
    path('order/<int:id>/', OrderView.as_view(), name='order'),
    path('payment/<int:id>/', PaymentView.as_view(), name='payment'),
    path('success/', SuccessView.as_view(), name='success_payment'),
    path('cancel/', CancelView.as_view(), name='cancelled_payment'),
]
