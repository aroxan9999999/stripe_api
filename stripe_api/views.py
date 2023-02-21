from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from .forms import *
import stripe

from stripe_api.models import Order, Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def succesView(request):
    __order = Order.objects.get(user=request.user)
    if __order.many:
        __order.many = False
        __order.save()
        return render(request, template_name='succes.html',
                      context={"product_all": __order})
    pk = __order.item_pk
    item = Item.objects.get(pk=pk)
    return render(request, template_name='succes.html', context={"product": item})


def cancelview(request):
    __order = Order.objects.get(user=request.user)
    if __order.many:
        __order.many = False
    else:
        __order.item = 'null'
    __order.save()
    return render(request, template_name='cancel.html')


def productbuyview(request, pk):
    item = Item.objects.get(pk=pk)
    photo = item.img.url
    context = {'item': item, "photo": photo}
    return render(request, template_name='product_buy.html', context=context)


class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        __order = Order.objects.prefetch_related("products").get(user=request.user)
        order = None
        product = None
        pk = kwargs.get("pk")
        if pk:
            product = Item.objects.get(pk=pk)
            currency = product.currency
            __order.item_pk = product.pk
        else:
            order = True
            products = __order.products.all()
            currency = products[0].currency
            __order.many = True
        __order.save()
        price = int(product.price) if product else sum(
            [int(d_price.price) for d_price in __order.products.all()] + [0])

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {'unit_amount': price, 'currency': f"{currency}",
                                   'product_data': {
                                       'name': product.name if product else '\n'.join([_p.name for _p in products]),
                                   }
                                   },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success',
            cancel_url='http://127.0.0.1:8000//cancel',
        )
        return redirect(checkout_session.url, code=303)


def product_list(request) -> Item:
    __order = Order.objects.get(user=request.user)
    if request.method == "POST":
        try:
            item_pk = request.POST.get("order_id")
            del_item_pk = request.POST.get("del_order_id")
            if item_pk:
                item = __order.products.filter(pk=item_pk)
                if not item.exists():
                    __order.products.add(Item.objects.get(pk=item_pk))
            elif del_item_pk:
                item = __order.products.get(pk=del_item_pk)
                __order.products.remove(item)
        except Exception:
            pass
    product = Item.objects.select_related("currency", 'category').all()
    orders = __order.products.select_related("category").all()
    category = set(category.category for category in orders)
    return render(request, template_name='product_list.html',
                  context={"products": product, "orders": orders, "order": __order, "categories": category})


def product_detail(request, pk):
    product = Item.objects.select_related("currency", 'category').all()
    item = Item.objects.get(pk=pk)
    return render(request, template_name='product_detail.html', context={'products': product, "item": item})


def order(request):
    __order = Order.objects.filter(user=request.user)
    __order[0].many = True
    __order[0].save()
    context = {"order": __order[0], 'item_order': __order[0]}
    photo = __order[0].products.filter().first().img.url
    context["photo"] = photo
    return render(request, template_name='product_buy.html', context=context)


def category_list(request, pk):
    product = Item.objects.select_related("category").filter(category__pk=pk)
    __order = Order.objects.get(user=request.user)
    orders = __order.products.all()
    item = orders[0]
    category = set(category.category for category in orders)
    return render(request, template_name='product_list.html',
                  context={"products": product, "orders": orders, "order": __order, "item": item,
                           "categories": category})
