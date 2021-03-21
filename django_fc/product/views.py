from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Product
from .forms import RegisterForm
from rest_framework import generics, mixins
from .serializers import ProductSerializer
from django.utils.decorators import method_decorator
from user.decorators import login_required, admin_required
from order.forms import RegisterForm as OrderForm
# Create your views here.


class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer #데이터 검증

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):    #mixins 사용
        return self.list(request, *args, **kwargs)


class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):# 상세보기용
    serializer_class = ProductSerializer #데이터 검증

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):    #get요청이 들어왔을때
        return self.retrieve(request, *args, **kwargs)



class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list' #object_list를 바꿈


@method_decorator(login_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()
        return super().form_valid(form)

class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    def get_context_data(self, **kwargs):   #디테일에서 수량 설정 하는방법
        context = super().get_context_data(**kwargs)

        context['form'] = OrderForm(self.request)
        return context