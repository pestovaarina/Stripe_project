import stripe
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View, generic
from .models import Discount, Item, Order, ItemsOrder, Tax
from stripe_api.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY


stripe.api_key = STRIPE_SECRET_KEY


class HomePageData(generic.TemplateView):
    """Представление для начальной страницы."""

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        items = Item.objects.all()
        context = super(HomePageData, self).get_context_data(**kwargs)
        context.update({
            'items': items
        })
        return context


class BuyItemView(generic.TemplateView):
    """Представление для страницы с покупкой товара."""

    def get(self, request, *args, **kwargs) -> JsonResponse:
        DOMAIN = 'http://127.0.0.1:8000'
        item = get_object_or_404(Item, id=self.kwargs['id'])
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/cancel',
        )
        return JsonResponse({'id': checkout_session.id})


class ItemInfoView(generic.TemplateView):
    """Представление для отображения карточки товара."""

    template_name = 'item_detail.html'

    def get_context_data(self, **kwargs):
        item = get_object_or_404(Item, id=self.kwargs['id'])
        context = super(ItemInfoView, self).get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY,
            'name': item.name,
            'item': item,
            'description': item.description,
            'price': item.price,
            'currency': item.currency
        })
        return context


class OrderView(generic.TemplateView):
    """Представление для отображения заказа."""

    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['id'])
        context = super(OrderView, self).get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY,
            'id': order.id,
            'order': order,
            'items': ItemsOrder.objects.filter(order_id=self.kwargs['id'])
        })
        return context


class PaymentView(View):
    """Представление для оформления заказа."""

    def get(self, request, *args, **kwargs) -> JsonResponse:
        DOMAIN = 'http://127.0.0.1:8000'
        order = get_object_or_404(Order, id=self.kwargs['id'])
        items = ItemsOrder.objects.filter(order_id=self.kwargs['id'])
        discount = None
        if Discount.objects.filter(order_id=order.id):
            discount = Discount.objects.filter(order_id=order.id)[0]
            coupon = stripe.Coupon.create(
                api_key=STRIPE_SECRET_KEY,
                duration="once",
                percent_off=discount.percentage,
                name=discount.name
            )
            discount = [
                {
                    'coupon': coupon
                }]
        tax_obj = Tax.objects.all()[0]
        if tax_obj.inclusive:
            tax = stripe.TaxRate.create(
                api_key=STRIPE_SECRET_KEY,
                display_name=tax_obj.display_name,
                percentage=tax_obj.percentage,
                inclusive=tax_obj.inclusive
            )
        checkout_session = stripe.checkout.Session.create(
            api_key=STRIPE_SECRET_KEY,
            line_items=[{
                'price_data': {
                    'currency': item.item.currency,
                    'product_data': {
                        'name': item.item.name,
                    },
                    'unit_amount': item.item.price,
                },
                'quantity': item.amount,
                'tax_rates': [tax.id],
            }for item in items],
            discounts=discount,
            payment_method_types=['card'],
            mode='payment',
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/cancel'
        )
        return JsonResponse({'id': checkout_session.id})


class SuccessView(generic.TemplateView):
    """Представление для отображения успешной оплаты."""

    template_name = 'success.html'


class CancelView(generic.TemplateView):
    """Представление для отображения, что оплата не прошла."""

    template_name = 'cancel.html'
