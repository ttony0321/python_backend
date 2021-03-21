from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from user.decorators import login_required
from .models import Order
from django.db import transaction
from user.models import User
from product.models import Product
# Create your views here.


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'
    #session 가져오기

    def form_valid(self, form):
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))  # product 불러오기
            order = Order(
                quantity=form.data.get('quantity'),#form에서 의 data를 가져온다
                product=prod,
                user=User.objects.get(email=self.request.get('user'))
            )
            order.save()
            prod.stock -= int(form.data.get('quantity'))
            prod.save()
        return super().form_valid(form)

    def form_invalid(self, form):#실패했을떄
        return redirect('product' + str(form.data.get('product')))

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    #model = Order   #이거는 모든 사용자의 주문정보를 볼수있음..   query셋 만들어서 사용
    template_name = 'order.html'
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):#Queryset 오버라이딩
        queryset = Order.objects.filter(user__email=self.request.session.get('user'))
        return queryset

    #원래는 Dispatch 함수가 있고 dispatch(request, *args, **kwargs)인자가 있음 안보이지만 있음 기능도함