import datetime
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from .models import Order
from django .db.models import F, Q
from django.db import transaction
from django.utils.html import format_html#실제 태그를 적용시키고 싶을때
from django.template.response import TemplateResponse
from django.urls import path
# Register your models here.


def refund(modeladmin, request, queryset):

    with transaction.automic():
        qs = queryset.filter(~Q(status='환불'))  # 환불이 아닌경우
        ct = ContentType.objects.get_for_model(queryset.model)
        for obj in qs:
            #if obj.status == '환불':continue
            obj.Product.stock += obj.Order.quantity
            obj.Product.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr='주문 환불',
                action_flag=CHANGE,
                change_message='주문 환불'
            )
        qs.update(status='환불')



refund.short_description = '환불'


class OrderAdmin(admin.ModelAdmin):

    list_filter = ('status',)        #오른쪽 필터 생성
    list_display = ('user', 'product', 'styled_status', 'action')
    change_list_template = 'admin/order_change_list.html'
    change_form_template = 'admin/order_change_form.html'
    # 액션 설정
    actions = [
        refund
    ]

    #버튼 만들기
    def action(self, obj):
        if obj.status != '환불':
            return format_html('<input type="button" value="환불" onclick="order_refund_submit({obj.id})" class="btn btn-primary btn-sm">')
            #클릭하는 환불 버튼에 해당되는 obj.id연결
    #필터에 해당되는 상태 스타일변화
    def styled_status(self, obj):
        if obj.status == '환불':
            return format_html(f'<span style="color:red">{obj.status}</span>')#f스트링 기능
        if obj.status == '결재완료':
            return format_html(f'<span style="color:green">{obj.status}</span>')
        return obj.status

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': "주문 목록"}

        if request.method == 'POST':#버튼 클릭시 동작
            #obj_id 모델 가져오기
            obj_id = request.POST.get('obj_id') #order_change_list 에서 가져온거
            if obj_id:
                qs = Order.objects.filter(pk=obj_id)
                ct = ContentType.objects.get_for_model(qs.model)
                for obj in qs:
                    # if obj.status == '환불':continue
                    obj.Product.stock += obj.Order.quantity
                    obj.Product.save()

                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ct.pk,
                        object_id=obj.pk,
                        object_repr='주문 환불',
                        action_flag=CHANGE,
                        change_message='주문 환불'
                    )
                qs.update(status='환불')

        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        order = Order.objects.get(pk=object_id)
        extra_context = {'title': f"'{order.user.email}'의'{order.product.name}'주문 수정"}#제목 바꾸기
        #버튼 없애기     submitline.html에서 확인가능
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False #True 일때 버튼 생성
        return super().changeform_view(request, object_id, form_url, extra_context)
    def get_urls(self):
        urls = super().get_urls()
        date_urls = [
            path('date_view/', self.date_view)
        ]
        return date_urls + urls

    def date_view(self, request):
        #최근 1주일 데이터
        week_date = datetime.datetime.now() - datetime.timedelta(days=7)
        week_data = Order.objects.filter(register_date__gte=week_date)#__gte : 보다 작은
        data = Order.objects.filter(register_date__lt=week_date)
        context = dict(
            self.admin_site.each_context,#기존 설정한 admin 그대로 나옴
            week_data = week_data,
            data=data
        )
        return TemplateResponse(request, 'admin/order_date_view.html', context)
    styled_status.short_description = '상태'


admin.site.register(Order, OrderAdmin)