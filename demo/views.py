from django.contrib.auth.decorators import login_required
from django.core import validators
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from demo.forms import RegisterUserForm
from demo.models import *


class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


def validate_username(request):
    username = request.GET.get('username')
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def validate_email(request):
    email = request.GET.get('email')
    try:
        validators.validate_email(email)
    except ValidationError as error:
        response = {
            'is_valid': False
        }
    else:
        response = {
            'is_valid': True,
            'is_taken': User.objects.filter(email__iexact=email).exists()
        }
    return JsonResponse(response)


def about(request):
    products = Product.objects.filter(count__gte=1).order_by('-date')[:5]
    return render(request, 'demo/about.html', context={'products': products})


def catalog(request):
    products = Product.objects.filter(count__gte=1)
    return render(request, 'demo/catalog.html', context={'products': products})


def contact(request):
    return render(request, 'demo/contact.html')


def product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'demo/product.html', context={'product': product})


@login_required
def basket(request):
    return render(request, 'demo/basket.html')


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'demo/orders.html', context={'orders': orders})


@login_required
def delete_order(request, pk):
    order = Order.objects.filter(user=request.user, pk=pk, status='new')
    if order:
        order.delete()
    return redirect('orders')

