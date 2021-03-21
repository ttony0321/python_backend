from django import forms
from .models import Order
from user.models import User
from product.models import Product
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password


class RegisterForm(forms.Form):
    # id는 한번에 못불러오므로 생상자 만들어서 연결
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)  # super()은 상속인듯
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required': '수량을 입력해주세요'
        }, label='수량'
    )
    product = forms.IntegerField(
        error_messages={
            'required': '상품설명을 입력해주세요'
        },
        widget=forms.HiddenInput, label='상품설명'
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        user = self.request.session.get('user')

        if not (quantity and product):
            self.add_error('quantity', '값이 없습니다.')
            self.add_error('product', '값이 없습니다.')
