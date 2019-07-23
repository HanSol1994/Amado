import datetime
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.forms import models
from django.shortcuts import redirect
from .models import *
import jdatetime
from django.utils.safestring import mark_safe
from django.db.models import Q,Sum
from AmadoFinance.models import *
from AmadoAccounting.models import *
from ActualCost.models import *
from import_export import resources,fields
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin.models import LogEntry
import random
import string
import requests
import json
from django.http import HttpResponse, JsonResponse
import xlwt
from xlwt import Workbook as _WB_, Font, XFStyle, Borders, Alignment, Formula
import datetime
from django.db.models import FloatField


class AmountForm(forms.ModelForm):
 class Meta:
     model = RequestProduct
     fields = ('request_product', 'request_amount')
     widgets = {
         'request_amount': forms.NumberInput(attrs={'step': 0.5,'min':0}),
     }




class UnitAdmin(admin.ModelAdmin):
 list_display = ['id','unit_name','unit_description']

 def get_readonly_fields(self, request, obj=None):

     if request.user.is_superuser:
         return list([])


     if request.user.has_perm('AmadoWHApp.can_see_unit'):#if only can see
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     #if can see and change

     return list([])


class WarehouseAdmin(admin.ModelAdmin):
 list_display = ['id','warehouse_name','warehouse_description']

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if request.user.has_perm('AmadoWHApp.can_see_wh'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     return list([])

class AccountInline(admin.TabularInline):
 model = Supplier.supplier_account.through

 # def get_fields(self, request, obj=None):
 #     print(self.opts.local_fields)
 #     return

 # fields = ['bankaccountbank']
 readonly_fields  = ['bankaccount']


 extra = 1

class CashInline(admin.TabularInline):
 model=CashPayment
 extra = 1

 fields = ['payment_due_date', 'payment_cost', 'payment_cause', 'payment_recipient', 'payment_account',
           'payment_description',
           'payment_status']

 readonly_fields = ['payment_due_date', 'payment_cost', 'payment_cause', 'payment_recipient', 'payment_account',
           'payment_description',
           'payment_status']

class SupplierAdmin (admin.ModelAdmin):
 list_display = ['id', 'supplier_company', 'supplier_name','supplier_phone','supplier_address']

 filter_horizontal = ['supplier_account']
 # exclude = ['supplier_account']

 search_fields = ['supplier_name','supplier_company']

 inlines = [AccountInline,CashInline]

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if request.user.has_perm('AmadoWHApp.can_see_supplier'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     return list([])


class ProductCategoryAdmin (admin.ModelAdmin):
 list_display = ['id', 'product_category_name']
 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if request.user.has_perm('AmadoWHApp.can_see_pcat'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     return list([])


class PriceForm(forms.ModelForm):
 class Meta:
     exclude=()
     model = Product
     widgets = {
         'current_price': forms.NumberInput(attrs={'step': 500,'min':500}),
         'previous_price': forms.NumberInput(attrs={'step': 500,'min':500}),
         'product_weekly_consumption': forms.NumberInput(attrs={'step': 0.5,'min':0.5}),
     }

class PriceInline(admin.TabularInline):
 model = Price
 extra = 0

class Recipe12Inline (admin.TabularInline):
 extra = 1
 model = Recipe12
 autocomplete_fields = ['recipe_parent_product']

class Recipe23Inline (admin.TabularInline):
 extra = 1
 model = Recipe23
 autocomplete_fields = ['recipe_child_product']


class UnitToUnitInline(admin.TabularInline):
    extra = 1
    model = UnitToUnit

class ACPFilter(admin.SimpleListFilter):
    title = ('موثر در آنالیز')
    parameter_name = 'acp'

    def lookups(self, request, model_admin):
        role = request.user.groups.all()[0].name

        return (
            ('yes', 'بله'),
            ('no','خیر')
        )

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            ids = Recipe23.objects.all()
            ids2 = []
            for id in ids:
                ids2.append(id.recipe_parent_product.id)

            return queryset.filter(id__in=ids2)
        elif self.value() == 'no':
            ids = Recipe23.objects.all()
            ids2 = []
            for id in ids:
                ids2.append(id.recipe_parent_product.id)

            return queryset.exclude(id__in=ids2)

        else:
            return queryset.filter()    
        
class GolestanFilter(admin.SimpleListFilter):
    title = ('قابل فروش')
    parameter_name = 'sale'

    def lookups(self, request, model_admin):
        role = request.user.groups.all()[0].name

        return (
            ('yes', 'بله'),
            ('no','خیر')
        )

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter(Q(id=455)|(Q(product_is_active=True)&(Q(id__in=[125,100,215,216,221,222,223,224,23,24,25,26,260,27,31,33,35,36,42,47,51,52,57,58,30,59,232,179,233,102,246
,	126
,	127
,	128
,	132
,	132
,	134
,	138
,	140
,	141
,	143
,	144
,	147
,	148
,	149
,	150
,	151
,	152
,	153
,	154
,	155
,	177
,	180
,	182
,	185
,	206
,	207
,	231
,	234
,	240
,	242
,	250
,	257
,	258
,	266
,	28
,	29
,	395
,	396
,	62
,	7
,	129
]))))    

        elif self.value() == 'no':
            return queryset.exclude(Q(id=455)|(Q(product_is_active=True)&(Q(id__in=[125,100,215,216,221,222,223,224,23,24,25,26,260,27,31,33,35,36,42,47,51,52,57,58,30,59,232,179,233,102,246
,	126
,	127
,	128
,	132
,	132
,	134
,	138
,	140
,	141
,	143
,	144
,	147
,	148
,	149
,	150
,	151
,	152
,	153
,	154
,	155
,	177
,	180
,	182
,	185
,	206
,	207
,	231
,	234
,	240
,	242
,	250
,	257
,	258
,	266
,	28
,	29
,	395
,	396
,	62
,	7
,	129
]))))    

        else:
            return queryset.filter()            
    
    
    

    
class ProductAdmin (admin.ModelAdmin):
 # list_display = ['id','product_warehouse' , 'product_name','product_unit','current_price','previous_price','price_change_date','product_weekly_consumption','warehouse_product_finish_date','product_description']
 list_display = ['id','product_warehouse' , 'product_name','product_unit','product_unit_ratio','product_second_unit','product_is_active','product_level','report_index','product_actual_price_1','getsaleprice']
    
 def getsaleprice(self,obj):
    if Price.objects.filter(product=obj).order_by('date'):
        return Price.objects.filter(product=obj).order_by('date').last().cost
    else:
        return 0


 inlines = [PriceInline,Recipe12Inline,Recipe23Inline,UnitToUnitInline] 

 list_filter = [GolestanFilter,ACPFilter,'product_level','product_is_active','product_branch_warehouse']

 def action(self,request,queryset):
     for q in queryset:
         q.product_level = 'lvl1-2'
         q.save()
            
 def action2(self,request,queryset):
     for q in queryset:
         q.product_is_active = False
         q.save()

 actions = [action,action2]

 ordering =['product_name']
 search_fields = ['product_name','id']
 # list_filter = ['product_supplier']
 filter_horizontal = ['product_supplier',]

 form = PriceForm

 def get_fields(self, request, obj=None):
     role = request.user.groups.all()[0].name
     if role == 'manager':
         return list([])

     if role == 'amado':

         return list(['product_name','product_supplier','product_category','product_unit','product_warehouse','current_price','previous_price',
           'price_change_date','product_description','product_weekly_consumption','product_is_active',
           'product_level','product_payment_is_check','product_payment_check_days','report_index','sale_percentage'])

     return list(['product_name','product_supplier','product_category','product_unit','product_second_unit','product_unit_ratio','product_warehouse','current_price','previous_price',
       'price_change_date','product_description','product_weekly_consumption','product_is_active',
       'product_level','product_payment_is_check','product_payment_check_days','report_index','product_actual_price_1','product_actual_price_2','product_branch_warehouse','sale_percentage'])

 def warehouse_product_finish_date(self, obj):
     d = jdatetime.datetime.today().strftime("%Y-%m-%d")
     return d;
     #TODO akharin mojodie anbar bashe inja too list_display

 # def get_queryset(self, request):
 #     role = request.user.groups.all()[0].name
 #     if role == 'manager':
 #         qs = super(ProductAdmin, self).get_queryset(request)

 #         return qs.filter(product_is_active=True)

 def get_queryset(self, request):


     role = request.user.groups.all()[0].name
     qs = super(ProductAdmin, self).get_queryset(request)
     if request.user.is_superuser :
        return qs     
     if role == 'manager':
            if request.user.has_perm('AmadoWHApp.other_branch_poonak'):
                return qs.filter(Q(product_is_active=True)&(Q(id__in=[125,232,179,233
,	126
,	127
,	128
,	132
,	132
,	134
,	138
,	140
,	141
,	143
,	144
,	147
,	148
,	149
,	150
,	151
,	152
,	153
,	154
,	155
,	177
,	180
,	182
,	185
,	206
,	207
,	231
,	234
,	240
,	242
,	250
,	257
,	258
,	266
,	28
,	29
,	395
,	396
,	62
,	7
,	129
])))
            if request.user.has_perm('AmadoWHApp.other_branch'):
                return qs.filter(Q(id=455)|(Q(product_is_active=True)&(Q(id__in=[125,100,215,216,221,222,223,224,23,24,25,26,260,27,31,33,35,36,42,47,51,52,57,58,30,59,232,179,233,102,246
,	126
,	127
,	128
,	132
,	132
,	134
,	138
,	140
,	141
,	143
,	144
,	147
,	148
,	149
,	150
,	151
,	152
,	153
,	154
,	155
,	177
,	180
,	182
,	185
,	206
,	207
,	231
,	234
,	240
,	242
,	250
,	257
,	258
,	266
,	28
,	29
,	395
,	396
,	62
,	7
,	129
]))))
            if request.user.has_perm('AmadoWHApp.can_see_special_products'):
                return qs.filter(Q(product_is_active=True)&(Q(product_level='lvl2')|Q(product_level='lvl1-2')))
            else:
                return qs.filter(~Q(id__in=[434,377,441,439,271,440,418,378,272,322,442,356,353,443,430,444,270])&Q(product_is_active=True)&(Q(product_level='lvl2')|Q(product_level='lvl1-2')))
     # elif or role == 'amadoup':
     #     return qs.filter(Q(product_is_active=True) & (Q(product_level='lvl1') | Q(product_level='lvl1-2')))
     else:
         return qs.filter(Q(product_is_active=True)&(Q(product_level='lvl2')|Q(product_level='lvl1-2')))

 warehouse_product_finish_date.short_description = 'پیشبینی تاریخ اتمام محصول در انبار'

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])
     if request.user.has_perm('AmadoWHApp.can_see_product'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     return list([])


 # def get_queryset(self, request):
 #     qs = super(ProductAdmin, self).get_queryset(request)

 #     user = request.user
 #     role = request.user.groups.all()[0].name
 #     if role != 'admin' and role !="amado":
 #         redirect('/admin/')
 #         return qs   #.filter(id=-1)
 #     else:
 #         return qs

class ProductInlineForm(forms.ModelForm):
 def __init__(self, *args, **kwargs):
     super(ProductInlineForm, self).__init__(*args, **kwargs)
     self.fields['add_variance'].widget = admin.widgets.AdminTextareaWidget()



 # class Meta:
 #     exclude=()
 #     readonly_fields=('add_variance')
 #     model = Product
 #     widgets = {
 #         'add_variance': forms.NumberInput(attrs={'step': 500,'min':500}),
 #         'previous_price': forms.NumberInput(attrs={'step': 500,'min':500}),
 #         'product_weekly_consumption': forms.NumberInput(attrs={'step': 0.5,'min':0.5}),
 #     }

class ModelLinkWidget(forms.Widget):
 def __init__(self, obj, attrs=None):
     self.object = obj
     super(ModelLinkWidget, self).__init__(attrs)

 def render(self, name, value, attrs=None,renderer=None):
     if self.object.pk:
         state = RequestProduct.objects.filter(id=self.object.pk).values(
                 'request_request__request_received')[0]
         if state['request_request__request_received'] == '1' or state['request_request__request_received'] == 'closed':
             link = '<a style="padding:5px;border-radius:5px;background: #b65e41;color:white;" href="/admin/AmadoWHApp/requestproduct/%i/change/">کلیک کنید</a>' % self.object.pk
             return mark_safe(link)
         else:
             link = '<a style="opacity: 0.5;cursor:not-allowed !important;pointer-events: none;padding:5px;border-radius:5px;background: gray;color:white;" href="/admin/AmadoWHApp/requestproduct/%i/change/">امکان پذیر نیست</a>' % self.object.pk
             return mark_safe(link)
     else:
         return mark_safe(u'')

class RAmountForm(forms.ModelForm):
 link = forms.CharField(label='ثبت مغایرت', required=False)

 def __init__(self, *args, **kwargs):
     super(RAmountForm, self).__init__(*args, **kwargs)
     # instance is always available, it just does or doesn't have pk.
     self.fields['link'].widget = ModelLinkWidget(self.instance)


 class Meta:
     model = RequestProduct
     fields = ('request_product', 'request_amount')
     widgets = {
         'request_amount': forms.NumberInput(attrs={'step': 0.5,'min':0,'style':"width:60px"}),
     }




        
class AddProductInline(admin.TabularInline):
    model = RequestProduct
    extra = 1
#    form = RAmountForm
    readonly_fields = ['mfield']
    fields = ( 'request_amount','request_unit', 'request_description',)

    autocomplete_fields = ['request_product']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj.request_received == 'waiting' or obj.request_received == '0':
         return True
        
        return True

    def get_readonly_fields(self, request, obj=None):
        # return list(['mfield_1'])
        if request.user.is_superuser:
            return list(['mfield_1'])
        if obj == None:
            return list(['mfield_1'])


        if request.user.has_perm('AmadoWHApp.can_add_anbar_variance'):
            #             result.remove('request_amount_sent')
            #             result.remove('request_unit_sent')
            return list(['mfield_1', 'request_amount', 'request_unit', 'request_description'])
        else:
            return list(['mfield_1','request_amount_sent','request_amount_unit'])
        return result

    def get_fields(self, request, obj=None):

        if request.user.is_superuser:
            return list(['request_product', 'request_amount', 'request_unit', 'mfield_1', 'request_description',
                         'request_amount_sent', 'request_unit_sent'])
        if request.user.has_perm('AmadoWHApp.can_add_anbar_variance'):
            return list(['request_product',
                         'request_amount_sent', 'request_unit_sent'])
        else:
            return list(['request_product', 'request_amount', 'request_unit', 'request_description'])        
        
class ProductInline(admin.TabularInline):
 model = RequestProduct
 extra = 1
 form = RAmountForm
 readonly_fields = ['mfield']
    
    
    
 fields = ('request_amount','request_description','link')
#
 def has_delete_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        return False

# def has_change_permission(self, request, obj=None):
#    return False

 autocomplete_fields = ['request_product']

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list(['mfield_1'])
     if obj == None :
            return list(['mfield_1'])
        
     if obj.request_received == 'waiting':
        return list(['mfield_1'])
    
     result = list(set(
                 [field.name for field in self.opts.local_fields] +
                 [field.name for field in self.opts.local_many_to_many]+['mfield_1']
             ))
     result.remove('id')
     return result
    
     if obj.request_received == 'closed' or obj.request_received == '4':
             result = list(set(
                 [field.name for field in self.opts.local_fields] +
                 [field.name for field in self.opts.local_many_to_many]+['mfield_1']
             ))
             result.remove('id')
             return result

     if obj != None and obj.request_received != 'waiting' and obj.request_received != '0':
         
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]+['mfield_1']
         ))
         result.remove('id')
         if request.user.has_perm('AmadoWHApp.can_add_anbar_variance'):
#             result.remove('request_amount_sent')
#             result.remove('request_unit_sent')
                
                return list(['mfield_1','request_amount','request_unit','request_description'])
         return result

     # print(obj.request_received)

     if obj != None and (obj.request_received == 'waiting' or obj.request_received == '0'):
         
         if request.user.has_perm('AmadoWHApp.can_see_requestp'):
             result = list(set(
                 [field.name for field in self.opts.local_fields] +
                 [field.name for field in self.opts.local_many_to_many]+['mfield_1']
             ))
             result.remove('id')
             result.remove('request_unit_sent')
             return result
         else:
             return list(['mfield_1','request_amount','request_unit','request_description'])

     if obj == None :
         return list(['mfield_1'])

     return list(['mfield_1'])

     # if role == 'accountant':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     # elif role == 'manager' and obj != None and obj.request_received != '0':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     # elif role == 'amado':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     #
     # return list([])

 def get_fields(self, request, obj=None):
    
     
     if request.user.is_superuser:
         return list(['request_product', 'request_amount','request_unit','mfield_1', 'request_description', 'request_amount_sent','request_unit_sent','link'])
     if request.user.has_perm('AmadoWHApp.can_add_anbar_variance'):
         return list(['request_product','request_amount','request_unit','request_description','mfield_1','request_amount_sent','request_unit_sent'])
     else:
         return list(['request_product', 'request_amount','request_unit', 'request_description', 'link'])


class DateFilterR(admin.SimpleListFilter):
 title = ('وضعیت')
 parameter_name = 'request_date'

 def lookups(self, request, model_admin):
     today = jdatetime.datetime.today().strftime("%Y-%m-%d")
     yesterday = (jdatetime.datetime.today()+jdatetime.timedelta(days=-1)).strftime("%Y-%m-%d")
     yesterday2 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-2)).strftime("%Y-%m-%d")
     yesterday3 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-3)).strftime("%Y-%m-%d")
     yesterday4 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-4)).strftime("%Y-%m-%d")
     yesterday5 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-5)).strftime("%Y-%m-%d")
     yesterday6 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-6)).strftime("%Y-%m-%d")

     return (
         ('today', today),
         ('yesterday', yesterday),
         ('yesterday2', yesterday2),
         ('yesterday3', yesterday3),
         ('yesterday4', yesterday4),
         ('yesterday5', yesterday5),
         ('yesterday6', yesterday6),
     )

 def queryset(self, request, queryset):
     today = jdatetime.datetime.today().strftime("%Y-%m-%d")
     yesterday = (jdatetime.datetime.today() + jdatetime.timedelta(days=-1)).strftime("%Y-%m-%d")
     yesterday2 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-2)).strftime("%Y-%m-%d")
     yesterday3 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-3)).strftime("%Y-%m-%d")
     yesterday4 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-4)).strftime("%Y-%m-%d")
     yesterday5 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-5)).strftime("%Y-%m-%d")
     yesterday6 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-6)).strftime("%Y-%m-%d")

     if self.value() == 'today':
         return queryset.filter(request_date=today)
     elif self.value() == 'yesterday':
         return queryset.filter(request_date=yesterday)
     elif self.value() == 'yesterday2':
         return queryset.filter(request_date=yesterday2)
     elif self.value() == 'yesterday3':
         return queryset.filter(request_date=yesterday3)
     elif self.value() == 'yesterday4':
         return queryset.filter(request_date=yesterday4)
     elif self.value() == 'yesterday5':
         return queryset.filter(request_date=yesterday5)
     elif self.value() == 'yesterday6':
         return queryset.filter(request_date=yesterday6)
     else:
         return queryset.filter()

class BranchFilterR(admin.SimpleListFilter):
 title = ('شعبه')
 parameter_name = 'request_branch'

 def lookups(self, request, model_admin):
     role = request.user.groups.all()[0].name

     if role == 'accountant':#TODO
         return (
             ('jannat', 'جنت آباد'),
             ('saadat', 'سعادت آباد'),
             ('poonak', 'پونک'),
             ('hyper', 'هایپراستار'),
             ('golestan', 'گلستان'),
         )
     elif role == 'manager':
         branch = Branch.objects.filter(branch_manager__manager_user=request.user).values('branch_name')[0]
         return (
             (request.user, branch['branch_name']),
         )
     else:
         return (
             ('admin', 'ادمین'),
             ('sample', 'نمونه'),
             ('jannat', 'جنت آباد'),
             ('saadat', 'سعادت آباد'),
             ('poonak', 'پونک'),
             ('hyper', 'هایپراستار'),
             ('golestan', 'گلستان'),
         )




 def queryset(self, request, queryset):

     if self.value() == 'admin':
         return queryset.filter(request_branch__id=1)
     elif self.value() == 'sample':
         return queryset.filter(request_branch__id=2)
     elif self.value() == 'poonak':
         return queryset.filter(request_branch__id=3)
     elif self.value() == 'jannat':
         return queryset.filter(request_branch__id=4)
     elif self.value() == 'saadat':
         return queryset.filter(request_branch__id=5)
     elif self.value() == 'golestan':
         return queryset.filter(request_branch__id=6)
     elif self.value() == 'hyper':
         return queryset.filter(request_branch__id=7)
     else:
         return queryset.filter()


class ConfirmFilter(admin.SimpleListFilter):
 title = ('وضعیت')
 parameter_name = 'request_received'

 def lookups(self, request, model_admin):
     return (
         ('0', 'انتظار'),
         ('1', 'تایید'),
         ('2', 'رد'),
     )

 def queryset(self, request, queryset):
     if self.value() == '0':
         return queryset.filter(request_received='0')
     elif self.value() == '1':
         return queryset.filter(request_received='1')
     elif self.value() == '2':
         return queryset.filter(request_received='2')
     else:
         return queryset.filter()

class RequestProductVarianceInline(admin.TabularInline):
 model = RequestProductVariance
 extra = 1

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if obj == None:
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     if obj.request_request.request_received == '0' or obj.request_request.request_received == 'waiting':
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     if request.user.has_perm('AmadoWHApp.can_see_requestpvar'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     return list([])
     # role = request.user.groups.all()[0].name
     # if role == 'accountant':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     # if role == 'manager' and obj != None:
     #     if obj.request_request.request_received != '1':
     #         result = list(set(
     #             [field.name for field in self.opts.local_fields]
     #         ))
     #         result.remove('id')
     #         return result
     # if role == 'amado':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result



 fields = ('request_product','request_amount_received','request_unit','request_type','request_description')

class RequestAdmin (admin.ModelAdmin):
 # list_display = ['getcode','request_code', 'request_branch','request_operator', 'request_date','request_time', 'status','printform']  # kholase mahsoolat TODO request code
 list_display = ['getcode', 'request_branch','request_operator', 'request_date','request_time', 'status','printform']  # kholase mahsoolat TODO request code
 # readonly_field=('account_actions',)

 ordering = ['-request_date']

 change_list_template = 'request_change_list.html'

 def printform(self, obj):
     state = Request.objects.filter(id=obj.id).values(
         'request_received')[0]
     if state['request_received'] == '1' or state['request_received'] == 'closed':
         link = '<a target="_blank" style="padding:5px;border-radius:5px;background: #b65e41;color:white;" href="../../../report/getform?rc=%s&k=h47g1304817g">پرینت درخواست</a>' % obj.request_code
         return mark_safe(link)
     else:
         link = '<a target="_blank" style="opacity: 0.5;cursor:not-allowed !important;pointer-events: none;padding:5px;border-radius:5px;background-color:gray;color:white;" >امکان پذیر نیست</a>'
         return mark_safe(link)

 printform.short_description = "پرینت درخواست"


 def getcode(self,obj):
     if obj.request_received != 'waiting' and obj.request_received != '0':
         return mark_safe('<a href="./%i/change/">%s مشاهده جزئیات</a>'%(obj.id,obj.request_code))

     return mark_safe('<a href="./%i/change/">%s ویرایش</a>' % (obj.id, obj.request_code))

 getcode.short_description = 'لینک'

 fields=()


 search_fields = ['request_code']
 list_filter = [BranchFilterR, ConfirmFilter, DateFilterR, ]

 # exclude = ('request_branch', 'request_date','request_time', 'request_received')

 readonly_fields = ('request_date', 'request_code','request_operator')
# inlines=(ProductInline,AddProductInline)
 inlines=(ProductInline,)
# inlines=(AddProductInline,)

 def status(self,obj):
     if obj.request_received == 'waiting' or obj.request_received == '0':
         return 'در انتظار تایید'
     elif obj.request_received == 'confirmed' or obj.request_received == '1':
         return 'تایید شده'
     elif obj.request_received == 'declined':
         return 'رد شده'
     elif obj.request_received == 'closed':
            return 'بسته شده'

 status.admin_order_field = 'request_received'
 status.short_description = 'وضعیت درخواست'

 def confirm(modeladmin, request, queryset):
     rows_updated = 0

     if not request.user.has_perm('AmadoWHApp.can_confirm_request'):
         messages.error(request, "شما اجازه تایید ندارید")
         return

     rows_updated = queryset.update(request_received='1')

     if rows_updated >0:
         message_bit = "%i درخواست تایید شد" % rows_updated
         modeladmin.message_user(request, "%s" % message_bit)
     else:
         message_bit = "هیچ درخواستی تایید نشد"
         messages.error(request, "%s" % message_bit)

     # role = request.user.groups.all()[0].name
     # if role != 'admin' and role != 'accountant':
     #     messages.error(request, "شما اجازه تایید ندارید")
     #     return
     #
     # if role != 'manager':#age az ghabl tayeed nashode bood #TODO
     #     rows_updated = queryset.update(request_received='1')
     #
     # if rows_updated >0:
     #     message_bit = "%i درخواست تایید شد" % rows_updated
     #     modeladmin.message_user(request, "%s" % message_bit)
     # else:
     #     if role != 'manager':
     #         message_bit = "هیچ درخواستی تایید نشد"
     #     else:
     #         message_bit = "شما اجازه تایید این درخواست را ندارید"
     #     # modeladmin.message_user(request, "%s" % message_bit)
     #     messages.error(request, "%s" % message_bit)

        
 def close(modeladmin, request, queryset):
     rows_updated = 0

     if not request.user.has_perm('AmadoWHApp.can_close_request'):
         messages.error(request, "شما اجازه بستن ندارید")
         return

     rows_updated = queryset.update(request_received='closed')

     if rows_updated >0:
         message_bit = "%i درخواست بسته شد" % rows_updated
         modeladmin.message_user(request, "%s" % message_bit)
     else:
         message_bit = "هیچ درخواستی بسته نشد"
         messages.error(request, "%s" % message_bit)

        
        
 def decline(modeladmin, request, queryset):
     if not request.user.has_perm('AmadoWHApp.can_decline_request'):
         messages.error(request, "شما اجازه رد ندارید")
         return

     rows_updated = queryset.update(request_received='2')

     if rows_updated >0:
         message_bit = "%i درخواست رد شد" % rows_updated
         modeladmin.message_user(request, "%s" % message_bit)
     else:
         message_bit = "هیچ درخواستی رد نشد"
         messages.error(request, "%s" % message_bit)
     # rows_updated = 0
     # role = request.user.groups.all()[0].name
     # if role != 'admin' and role != 'accountant':
     #     messages.error(request, "شما اجازه رد ندارید")
     #     return
     #
     # if role != 'manager':#age az ghabl tayeed nashode bood #TODO
     #     rows_updated = queryset.update(request_received='2')
     #
     # if rows_updated > 0:
     #     message_bit = "%i درخواست رد شد" % rows_updated
     #     modeladmin.message_user(request, "%s" % message_bit)
     # else:
     #     role = request.user.groups.all()[0].name
     #
     #     if role != 'manager':
     #         message_bit = "هیچ درخواستی رد نشد"
     #     else:
     #         message_bit = "شما اجازه رد این درخواست را ندارید"
     #     # modeladmin.message_user(request, "%s" % message_bit)
     #     messages.error(request, "%s" % message_bit)


 confirm.short_description = "تایید درخواست توسط انبار"
 decline.short_description = "رد درخواست توسط انبار"
 close.short_description = "بستن درخواست توسط انبار"


 def wordifyfa(self, num, level):

    if not num:
        return ""

    if num < 0:
        num = num * -1;
        return "منفی " + self.wordifyfa(num, level);

    if num == 0:
        if level == 0:
            return "صفر";
        else:
            return "";

    result = ""
    yekan = [" یک ", " دو ", " سه ", " چهار ", " پنج ", " شش ", " هفت ", " هشت ", " نه "]
    dahgan = [" بیست ", " سی ", " چهل ", " پنجاه ", " شصت ", " هفتاد ", " هشتاد ", " نود "]
    sadgan = [" یکصد ", " دویست ", " سیصد ", " چهارصد ", " پانصد ", " ششصد ", " هفتصد ", " هشتصد ", " نهصد "]
    dah = [" ده ", " یازده ", " دوازده ", " سیزده ", " چهارده ", " پانزده ", " شانزده ", " هفده ", " هیجده ",
           " نوزده "];

    if level > 0:
        result += " و ";
        level -= 1;

    if num < 10:
        result += yekan[num - 1];
    elif num < 20:
        result += dah[num - 10];
    elif num < 100:
        result += dahgan[int(num / 10) - 2] + self.wordifyfa(num % 10, level + 1);
    elif num < 1000:
        result += sadgan[int(num / 100) - 1] + self.wordifyfa(num % 100, level + 1);
    elif num < 1000000:
        result += self.wordifyfa(int(num / 1000), level) + " هزار " + self.wordifyfa(num % 1000, level + 1);
    elif num < 1000000000:
        result += self.wordifyfa(int(num / 1000000), level) + " میلیون " + self.wordifyfa(num % 1000000,
                                                                                          level + 1);
    elif num < 1000000000000:
        result += self.wordifyfa(int(num / 1000000000), level) + " میلیارد " + self.wordifyfa(num % 1000000000,
                                                                                              level + 1);
    elif num < 1000000000000000:
        result += self.wordifyfa(int(num / 1000000000000), level) + " تریلیارد " + self.wordifyfa(
            num % 1000000000000, level + 1);

    return result;

 def wordifyRials(self, num):
    return self.wordifyfa(num, 0) + " ریال";

 def wordifyRialsInTomans(self, num):
    if num >= 10:
        num = int(num / 10);
    elif num <= -10:
        num = int(num / 10);
    else:
        num = 0;

    return self.wordifyfa(num, 0) + " تومان";

 def creat_factor(self, request, queryset):
        if not request.user.has_perm('AmadoWHApp.can_creat_factor'):
            messages.error(request, "شما اجازه ایجاد فاکتور ندارید")
            return

        def my_int(num):
            if num:
                return num
            else:
                return 0


        response = HttpResponse(content_type='application/ms-excel')

        today = jdatetime.datetime.today()
        response['Content-Disposition'] = u'attachment; filename=factor_foroosh_%s.xls'%(today.strftime('%Y-%m-%d'))
        wb = xlwt.Workbook(encoding='utf-8')



        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        #
        # alnum = Alignment()
        # alnum.horz = Alignment.HORZ_CENTER
        # alnum.vert = Alignment.VERT_CENTER

        al2 = Alignment()
        al2.horz = Alignment.HORZ_CENTER
        al2.vert = Alignment.VERT_CENTER

        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.left_colour = 0x00
        borders.right_colour = 0x00
        borders.top_colour = 0x00
        borders.bottom_colour = 0x00

        font_style = xlwt.XFStyle()  # normal
        font_style.alignment = al2
        font_style.num_format_str = '#,##0'
        font_style.font.height = 220
        font_style.borders = borders
        font_style.font.name = 'B Nazanin'
        
        amount_style = xlwt.XFStyle()  # normal
        amount_style.alignment = al2
        amount_style.num_format_str = '#,##0.00'
        amount_style.font.height = 220
        amount_style.borders = borders
        amount_style.font.name = 'B Nazanin'

        signature = xlwt.XFStyle()  # normal
        signature.alignment = al2
        signature.num_format_str = '#,##0'
        signature.font.height = 220
        signature.font.name = 'B Nazanin'

        header = xlwt.XFStyle()  # normal
        header.alignment = al
        header.font.bold = True
        header.num_format_str = '#,##0'
        header.font.height = 250
        header.borders = borders
        header.font.name = 'B Nazanin'

        request_date = None
        sum = 0

        def turn_to_unit(price,product,unit):
            if product.product_unit == unit:
                return price
#            ur = UnitToUnit.objects.filter(Q(product=product)&Q(first_unit=product.product_unit)&Q(second_unit=unit)).last().ration
#            return price/ur
            try:
                ur = UnitToUnit.objects.filter(
                    Q(product=product) & Q(first_unit=product.product_unit) & Q(second_unit=unit)).last().ration
                return price / ur
            except:
                return 1



        branch = None
        queryset = queryset.filter().order_by('request_date','request_branch')
        for q in queryset:
            date = q.request_date + jdatetime.timedelta(days=1)
            if q.request_date != request_date or q.request_branch != branch:
                if request_date != None:

                    ws.write(row_num+1,0,'جمع کل(حروف)',font_style)
                    ws.write_merge(row_num + 1, row_num + 1, 1, 5, '%s ریال' % self.wordifyfa(int(sum), 0), font_style)

                    ws.write(row_num,0,'',header)
                    ws.write(row_num,1,'',header)
                    ws.write(row_num,2,'',header)
                    ws.write(row_num,3,'',header)
                    ws.write(row_num , 4, 'جمع کل (ریال)',header)
                    ws.write(row_num , 5, int(sum),header)
                    sum = 0

                branch = q.request_branch
                request_date = q.request_date
                ws = wb.add_sheet('%s شعبه %s'%(date.strftime('%Y-%m-%d'),branch.branch_name))
                ws.cols_right_to_left = 1


                ws.write_merge(0,0,0,2,'فاکتور فروش شعبه %s'%q.request_branch.branch_name,header)
                ws.write_merge(0,0,3,5,'تاریخ خرید : %s'%date.strftime('%Y/%m/%d'),header)

                ws.col(0).width = int(70 * 42.3)
                ws.col(1).width = int(190 * 42.3)
                ws.col(2).width = int(53 * 42.3)
                ws.col(3).width = int(53 * 42.3)
                ws.col(4).width = int(101 * 42.3)
                ws.col(5).width = int(101 * 42.3)

                ws.write(1,0,'ردیف',header)
                ws.write(1,1,'نام کالا',header)
                ws.write(1,2,'مقدار',header)
                ws.write(1,3,'واحد',header)
                ws.write(1,4,'فی(ریال)',header)
                ws.write(1,5,'مبلغ کل(ریال)',header)
                row_num = 2
                counter = 1


            for p in RequestProduct.objects.filter(Q(request_request=q)&~Q(request_amount_sent=0)):
                ws.write(row_num,0,counter,font_style)
                ws.write(row_num,1,p.request_product.product_name,font_style)

#                price = Price.objects.filter(Q(product=p.request_product)).order_by(
#                    'date').last().cost  # for first unit
                try:
                    price = Price.objects.filter(Q(product=p.request_product) & Q(date__lte=request_date)).order_by(
                        'date').last().cost  # for first unit
                except:
                    try:
                        price = Price.objects.filter(Q(product=p.request_product) ).order_by(
                        'date').last().cost  # for first unit
                    except:
                        price = 0
                    

                amount = p.request_amount
                unit = p.request_product.product_unit


                if p.request_amount_sent:
                    amount = p.request_amount_sent
                    if p.request_unit_sent:
                        unit = p.request_unit_sent
                else:
                    if p.request_unit:
                        unit = p.request_unit

                cost = turn_to_unit(price,p.request_product,unit)

                ws.write(row_num, 2, amount, amount_style)
                ws.write(row_num, 3, unit.unit_name, font_style)
                ws.write(row_num, 4, cost, font_style)

                tot = cost*amount
                sum += tot
                ws.write(row_num, 5, tot,font_style)

                row_num += 1
                counter += 1



            # self.wordifyfa(q.pardakhti, 0)

        ws.write(row_num + 1, 0, 'جمع کل(حروف)', font_style)
        ws.write_merge(row_num + 1, row_num+1, 1, 5, '%s ریال'%self.wordifyfa(int(sum), 0), font_style)

        ws.write(row_num, 0, '', header)
        ws.write(row_num, 1, '', header)
        ws.write(row_num, 2, '', header)
        ws.write(row_num, 3, '', header)
        ws.write(row_num, 4, 'جمع کل(ریال)',header)
        ws.write(row_num, 5, int(sum),header)









            # ws.write_merge(row, row, 6, 7, 'امضا و اثرانگشت', signature)  # TODO

        wb.save(response)
        return response

    
 creat_factor.short_description = 'ایجاد فاکتور'    
    
 actions = [confirm,decline,close,creat_factor]

 def get_queryset(self, request):
     qs = super(RequestAdmin, self).get_queryset(request)
     user = request.user

     role = request.user.groups.all()[0].name
     if role == 'accountant':
         branch = Branch.objects.exclude(id__in = [1,2]).values('id')
         return qs.filter(request_branch__in=branch)
     elif role == 'manager':
         branch = Branch.objects.filter(branch_manager__manager_user=user).values('id')[0]
         return qs.filter( request_branch=branch['id'])
     else:#admin
         return qs

 def has_delete_permission(self, request, obj=None):
     if request.user.is_superuser:
         return True

     # print(request.user.has_perm('AmadoWHApp.delete_request'))

     if request.user.has_perm('AmadoWHApp.delete_request') and request.POST and request.POST.get('action') == 'delete_selected':
         ids = request.POST.getlist('_selected_action')
         for i in ids:
             r = Request.objects.filter(id=int(i)).values('request_received')[0]['request_received']
             if r == '1' or r == '2' or r == ' confirmed' or r == 'rejected':
                 return False
         return True

     if obj != None and obj.request_received != '0':
         return False

     if request.user.has_perm('delete_request') and obj != None:
         return True;

     return True
     # if role == 'manager':
     #     if request.POST and request.POST.get('action') == 'delete_selected':
     #         ids = request.POST.getlist('_selected_action')
     #         for i in ids:
     #             r = Request.objects.filter(id=int(i)).values('request_received')[0]['request_received']
     #             if r == '1':
     #                 return False
     #         return True

     # role = request.user.groups.all()[0].name
     # if role == 'manager' and obj != None:
     #     if obj.request_received != '0':
     #         return False;
     # elif role == 'manager':
     #     if request.POST and request.POST.get('action') == 'delete_selected':
     #
     #         ids = request.POST.getlist('_selected_action')
     #         for i in ids:
     #             r = Request.objects.filter(id=int(i)).values('request_received')[0]['request_received']
     #             if r == '1':
     #                 return False
     #         return True
     # return True

 def save_model(self, request, instance, form, change):

     user = request.user

     if not change:
         role = request.user.groups.all()[0].name
         if role != 'admin':
             user = Branch.objects.get(branch_manager__manager_user=user)
             rand = ''.join(random.choice(string.digits) for m in range(2))
             userId = "%02d" % (user.id,)
             date = jdatetime.datetime.today().strftime("%y%m%d")
             count = "%02d" % (Request.objects.filter(
                 Q(request_date=jdatetime.datetime.today().strftime("%Y-%m-%d")) & Q(request_branch=user)).count() + 1)
             rand = ''.join(random.choice(string.digits) for m in range(2))
             code = '%s%s%s-%s' %(date,userId,count,rand)
             instance.request_code=code
             
             instance.request_branch = user
             instance.request_operator = request.user

             message = "سفارش شعبه "
             message += Branch.objects.get(branch_manager__manager_user=request.user).branch_name
             message += ' %s' % (jdatetime.datetime.today().strftime("%y/%m/%d"))
             message += ' (کد %s) ' % (code)
             message += "\n"
             message += "http://5.152.221.185/report/getform?rc="
             message += code
             message += "%26k=h47g1304817g"


             resp = requests.post(
                 "https://api.telegram.org/bot612831717:AAE5n-BJs-JrNdBooJhHPryIcR-YtWyvz8U/sendmessage?chat_id=-1001231911243&text=" + message,
                 # "https://api.telegram.org/bot492363761:AAFej7iOxjZdIpxhLcN0ywAWuHCojn_JIyg/sendmessage?chat_id=106825278&text=" + message,
                 headers={
                     "Accept": "application/json"
                 })

     instance = form.save(commit=False)

     instance.save()
     form.save_m2m()
     return instance

 def get_readonly_fields(self, request, obj=None):
     # if obj != None and obj.request_received != 'waiting':#if confirmed or rejected cant be changed
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     #
     # if obj != None and obj.request_received == 'waiting' and request.user.has_perm('AmadoWHApp.can_see'):#if only can see registered requests
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     #
     # if obj == None:
     #     return ['request_code', 'request_date', 'request_time', 'request_branch', 'request_received',
     #             'request_operator']
     if request.user.is_superuser:
         return list([])
     
     else:
         result = list(set(
                 [field.name for field in self.opts.local_fields]
             ))
         result.remove('id')
         return result


     # role = request.user.groups.all()[0].name
     # if role == 'amado':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     # elif role == 'manager':
     #     return ['request_code','request_date','request_time','request_branch','request_received','request_operator']
     # else:
     #     return list([])


class RequestInline(admin.TabularInline):
 model = Request
 extra = 1

 # fields = ('request_date','get_brief','request_received')
 fields = ('request_date','request_received')

 # readonly_fields = ('get_link',)

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])
     if request.user.has_perm('AmadoWHApp.can_see_request'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     return list([])


class BranchAdmin (admin.ModelAdmin):
 list_display = ['id', 'branch_name', 'get_branch_manager','branch_phone']

 # inlines = (RequestInline,)

 def get_branch_manager(self,obj):
     try:
         m = Branch.objects.filter(id=obj.id).values('branch_manager__manager_name')[0]
         return '%s' % m['branch_manager__manager_name']
     except:
         return '-'

 get_branch_manager.short_description = 'مدیر'

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])
     if request.user.has_perm('AmadoWHApp.can_see_branch'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     return list([])

 change_list_template = 'branch_change_list.html'

 def calc_cost_benefits(self, request, queryset):

        start_date = request.POST['from_date']
        finish_date = request.POST['to_date']

        # start_date = '1397-07-01'
        # finish_date = '1397-07-30'

        def my_int(num):
            if num:
                return num
            else:
                return 0

        months = [
            'فروردین',
            'اردیبهشت',
            'خرداد',
            'تیر',
            'مرداد',
            'شهریور',
            'مهر',
            'آبان',
            'آذر',
            'دی',
            'بهمن',
            'اسفند',
        ]

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=cost_benefit.xls'
        wb = xlwt.Workbook(encoding='utf-8')

        today = jdatetime.datetime.today().strftime('%Y/%m/%d')

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER

        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.left_colour = 0x00
        borders.right_colour = 0x00
        borders.top_colour = 0x00
        borders.bottom_colour = 0x00

        font_style = xlwt.XFStyle()  # normal
        font_style.alignment = al
        font_style.num_format_str = '#,##0'
        font_style.font.height = 220
        font_style.borders = borders
        font_style.font.name = 'B Nazanin'

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']

        header = xlwt.XFStyle()  # normal
        header.alignment = al
        header.font.bold = True
        header.num_format_str = '#,##0'
        header.font.height = 220
        header.borders = borders
        header.font.name = 'B Nazanin'
        header.pattern = pattern

        for q in queryset:

            sales = Sales.objects.filter(Q(sales_branch=q)&Q(sales_date__gte=start_date)&Q(sales_date__lte=finish_date)).aggregate(sum=Sum('sales_tot_cash_cost'))['sum']

            warehouse_cost = 0
            for p in BranchWarehouseProduct.objects.filter(
                            Q(branch_warehouse__date=start_date) & Q(branch_warehouse__branch=q)):
                if p.product.product_actual_price_1:
                    if not p.unit or p.unit == p.product.product_unit:
                        warehouse_cost += (p.amount * (p.product.product_actual_price_1))
                    else:
                        warehouse_cost += ((p.amount * p.product.product_actual_price_1 )/p.product.product_unit_ratio)
                else:
                    warehouse_cost += 0


            request_cost = 0
            for p in RequestProduct.objects.filter(~Q(request_request__request_received='rejected')&
                    Q(request_request__request_date__gte=start_date) & Q(request_request__request_date__lte=finish_date) & Q(request_request__request_branch=q)):
                if p.request_product.product_actual_price_1:
                    if not p.request_unit or p.request_unit == p.request_product.product_unit:
                        request_cost += (
                        p.request_amount * (p.request_product.product_actual_price_1))
                    else:
                        request_cost += ((p.request_amount * p.request_product.product_actual_price_1)/p.request_product.product_unit_ratio)

                else:
                    request_cost += 0


            salaries = SalaryDetail.objects.filter( (Q(payment_status='paid')|Q(payment_status='confirmed'))&
                Q(salary__branch=q) & Q(salary__from_date__gte=start_date) & Q(salary__to_date__lte=finish_date)).aggregate(sum=Sum('pardakhti'))['sum']


            others = []
            for account in OverAccount.objects.all():

                x = CashPayment.objects.filter(Q(over_account=account)
                                                           &Q(payment_due_date__gte=start_date)&Q(payment_due_date__lte=finish_date))
                x = RecedeImage.objects.filter(Q(factor__in=x)& Q(def_account=q)).aggregate(sum=Sum('cost'))['sum']


                y = CheckPayment.objects.filter(Q(over_account=account)
                                                           & Q(check_due_date__gte=start_date) & Q(
                    check_due_date__lte=finish_date))

                y = RecedeImage.objects.filter(Q(checkp__in=y)& Q(def_account=q)).aggregate(sum=Sum('cost'))['sum']

                z = FundPayment.objects.filter(Q(over_account=account)
                                                & Q(payment_due_date__gte=start_date) & Q(
                    payment_due_date__lte=finish_date))
                z = RecedeImage.objects.filter(Q(fund__in=z)& Q(def_account=q)).aggregate(sum=Sum('cost'))['sum']

                sum = 0
                if x:
                    sum += x
                if y:
                    sum += y
                if z:
                    sum += z

                others.append({'account':account.name,'sum':sum})





            ws = wb.add_sheet(q.branch_name)
            ws.cols_right_to_left = 1

            ws.col(0).width = int(55 * 42.3)
            ws.col(1).width = int(160 * 42.3)
            ws.col(2).width = int(120 * 42.3)
            ws.col(3).width = int(120 * 42.3)

            ws.row(0).height_mismatch = True
            ws.row(0).height = int(30 * 20)

            ws.row(1).height_mismatch = True
            ws.row(1).height = int(30 * 20)


            ws.write_merge(0, 0, 0, 3, 'سود و زیان شعبه %s - %s %i' % (q.branch_name,months[jdatetime.datetime.strptime(start_date,'%Y-%m-%d').month-1],jdatetime.datetime.strptime(start_date,'%Y-%m-%d').year), header)

            row_num = 1

            ws.write(row_num, 0, 'ردیف', header)
            ws.write(row_num, 1, 'موضوع', header)
            ws.write(row_num, 2, 'مبلغ در آمد - ریال', header)
            ws.write(row_num, 3, 'مبلغ هزینه - ریال', header)

            row_num += 1

            ws.write(row_num, 0, row_num-1, font_style)
            ws.write(row_num, 1, 'فروش', font_style)
            ws.write(row_num, 2, sales, font_style)
            ws.write(row_num, 3, None, font_style)

            row_num += 1

            ws.write(row_num, 0, row_num-1, font_style)
            ws.write(row_num, 1, 'موجودی مواد اولیه (انبارگردانی سر ماه)', font_style)
            ws.write(row_num, 2, warehouse_cost, font_style)
            ws.write(row_num, 3, None, font_style)

            row_num += 1

            ws.write(row_num, 0, row_num-1, font_style)
            ws.write(row_num, 1, 'مواد اولیه مصرف شده', font_style)
            ws.write(row_num, 3, request_cost, font_style)
            ws.write(row_num, 2, None, font_style)

            row_num += 1

            ws.write(row_num, 0, row_num - 1, font_style)
            ws.write(row_num, 1, 'حقوق پرسنل', font_style)
            ws.write(row_num, 3, salaries, font_style)
            ws.write(row_num, 2, None, font_style)


            for o in others:
                row_num += 1

                ws.write(row_num, 0, row_num - 1, font_style)
                ws.write(row_num, 1, o['account'], font_style)
                ws.write(row_num, 2, None, font_style)
                ws.write(row_num, 3, o['sum'], font_style)

            row_num += 1

            ws.write(row_num, 0, None, header)
            ws.write(row_num, 1, 'جمع', header)
            ws.write(row_num, 2, Formula('Sum(C3:C%i)'%(row_num)), header)
            ws.write(row_num, 3, Formula('Sum(D3:D%i)'%row_num), header)

            row_num += 1

            ws.write(row_num, 0, None, header)
            ws.write(row_num, 1, None, header)
            ws.write(row_num, 2, 'سود / زیان', header)
            ws.write(row_num, 3, Formula('C%i-D%i'%(row_num,row_num)), header)

            ws.row(row_num-1).height_mismatch = True
            ws.row(row_num-1).height = int(30 * 20)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = int(30 * 20)

            for i in range(0, row_num-3):
                ws.row(i + 2).height_mismatch = True
                ws.row(i + 2).height = int(20 * 20)

        wb.save(response)
        return response

 calc_cost_benefits.short_description = 'محاسبه سود و زیان'
 actions = [calc_cost_benefits]


class ManagerAdmin (admin.ModelAdmin):
 list_display = ['id', 'manager_name', 'get_manager_branch','manager_tel']

 def get_manager_branch(self,obj):
     try:
         b = Branch.objects.filter(branch_manager__id=obj.id).values('branch_name')[0]
         return '%s' % b['branch_name']
     except:
         return '-'

 get_manager_branch.short_description = 'شعبه'

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])
     if request.user.has_perm('AmadoWHApp.can_see_manager'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     return list([])

 # def get_number_of_requests(self,obj):TODO
 #     m = Branch.objects.filter(id=obj.id).values('branch_manager__manager_name')[0]
 #     return '%s' % m['branch_manager__manager_name']
 # def get_latest_request(self,obj):
 #     m = Branch.objects.filter(id=obj.id).values('branch_manager__manager_name')[0]
 #     return '%s' % m['branch_manager__manager_name']


class PriceForm(forms.ModelForm):
 def __init__(self, *args, **kwargs):
     super(PriceForm, self).__init__(*args, **kwargs)
     self.fields['price_change_date'].initial= jdatetime.datetime.today()#TODO

 class Meta:
     exclude=()
     model = Product
     widgets = {
         'current_price': forms.NumberInput(attrs={'step': 500,'min':500}),
         'previous_price': forms.NumberInput(attrs={'step': 500,'min':500}),
         'product_weekly_consumption': forms.NumberInput(attrs={'step': 0.5,'min':0.5}),
     }


class WAmountForm(forms.ModelForm):
 class Meta:
     model = Warehouse_Product
     exclude = ()
     widgets = {
         'warehouse_product_stock': forms.NumberInput(attrs={'step': 0.1,'min':0.1}),
     }


class Warehouse_ProductAdmin (admin.ModelAdmin):
 list_display = ['id', 'warehouse_product','getProvider','getUnit', 'warehouse_handling_date', ]
 form = WAmountForm

 def getUnit (self,obj):
     b = Warehouse_Product.objects.filter(id=obj.id).values('warehouse_product__product_unit__unit_name')[0]
     return '%i %s' % (obj.warehouse_product_stock,b['warehouse_product__product_unit__unit_name'])

 def getProvider (self,obj):
     b = Warehouse_Product.objects.filter(id=obj.id).values('warehouse_product__product_supplier__supplier_name')[0]
     return '%s' % ( b['warehouse_product__product_supplier__supplier_name'])

 getUnit.short_description = 'موجودی انبار'
 getProvider.short_description = 'تامین کننده'

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])
     if request.user.has_perm('AmadoWHApp.can_see_whproduct'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     return list([])


class DateFilter(admin.SimpleListFilter):
 title = ('تاریخ ارسال درخواست')
 parameter_name = 'request_date'

 def lookups(self, request, model_admin):
     today = jdatetime.datetime.today().strftime("%Y-%m-%d")
     yesterday = (jdatetime.datetime.today()+jdatetime.timedelta(days=-1)).strftime("%Y-%m-%d")
     yesterday2 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-2)).strftime("%Y-%m-%d")
     yesterday3 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-3)).strftime("%Y-%m-%d")
     yesterday4 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-4)).strftime("%Y-%m-%d")
     yesterday5 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-5)).strftime("%Y-%m-%d")
     yesterday6 = (jdatetime.datetime.today()+jdatetime.timedelta(days=-6)).strftime("%Y-%m-%d")

     return (
         ('today', today),
         ('yesterday', yesterday),
         ('yesterday2', yesterday2),
         ('yesterday3', yesterday3),
         ('yesterday4', yesterday4),
         ('yesterday5', yesterday5),
         ('yesterday6', yesterday6),
     )

 def queryset(self, request, queryset):
     today = jdatetime.datetime.today().strftime("%Y-%m-%d")
     yesterday = (jdatetime.datetime.today() + jdatetime.timedelta(days=-1)).strftime("%Y-%m-%d")
     yesterday2 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-2)).strftime("%Y-%m-%d")
     yesterday3 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-3)).strftime("%Y-%m-%d")
     yesterday4 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-4)).strftime("%Y-%m-%d")
     yesterday5 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-5)).strftime("%Y-%m-%d")
     yesterday6 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-6)).strftime("%Y-%m-%d")
     yesterday7 = (jdatetime.datetime.today() + jdatetime.timedelta(days=-7)).strftime("%Y-%m-%d")

     # if self.value() == 'today':
     #     return queryset.filter(Q(request_request__request_date=today)
     # elif self.value() == 'yesterday':
     #     return queryset.filter(request_request__request_date=yesterday)
     # elif self.value() == 'yesterday2':
     #     return queryset.filter(request_request__request_date=yesterday2)
     # elif self.value() == 'yesterday3':
     #     return queryset.filter(request_request__request_date=yesterday3)
     # elif self.value() == 'yesterday4':
     #     return queryset.filter(request_request__request_date=yesterday4)
     # elif self.value() == 'yesterday5':
     #     return queryset.filter(request_request__request_date=yesterday5)
     # elif self.value() == 'yesterday6':
     #     return queryset.filter(request_request__request_date=yesterday6)
     # else:
     #     return queryset.filter()
     if self.value() == 'today':
         return queryset.filter((Q(request_date=today) & Q(request_time__lte='3:00') & Q(request_time__gte='00:00')) |
                                     (Q(request_date=yesterday) & Q(request_time__lte='23:59') & Q(request_time__gte='19:00')))
     elif self.value() == 'yesterday':
         return queryset.filter((Q(request_date=yesterday) & Q(request_time__lte='3:00') & Q(request_time__gte='00:00')) |
                                     (Q(request_date=yesterday2) & Q(request_time__lte='23:59') & Q(request_time__gte='19:00')))
     elif self.value() == 'yesterday2':
         return queryset.filter((Q(request_date=yesterday2) & Q(request_time__lte='3:00') & Q(request_time__gte='00:00')) |
                                     (Q(request_date=yesterday3) & Q(request_time__lte='23:59') & Q(request_time__gte='19:00')))
     elif self.value() == 'yesterday3':
         return queryset.filter((Q(request_date=yesterday3) & Q(request_time__lte='3:00') & Q(request_time__gte='00:00')) |
                                     (Q(request_date=yesterday4) & Q(request_time__lte='23:59') & Q(request_time__gte='19:00')))
     elif self.value() == 'yesterday4':
         return queryset.filter((Q(request_date=yesterday4) & Q(request_time__lte='3:00') & Q(request_time__gte='00:00')) |
                                     (Q(request_date=yesterday5) & Q(request_time__lte='23:59') & Q(request_time__gte='19:00')))
     elif self.value() == 'yesterday5':
         return queryset.filter((Q(request_date=yesterday5) & Q(request_time__lte='3:00') & Q(request_time__gte='00:00')) |
                                     (Q(request_date=yesterday6) & Q(request_time__lte='23:59') & Q(request_time__gte='19:00')))
     elif self.value() == 'yesterday6':
         return queryset.filter((Q(request_date=yesterday6) & Q(request_time__lte='3:00') & Q(request_time__gte='00:00')) |
                                     (Q(request_date=yesterday7) & Q(request_time__lte='23:59') & Q(request_time__gte='19:00')))
     else:
         return queryset.filter()


class RequestProductResource(resources.ModelResource):
 product_name = fields.Field(
     column_name='نام کالا',
     attribute='request_product__product_name',)
 product_amount = fields.Field(
     column_name='مقدار',
     attribute='request_amount', )
 product_description = fields.Field(
     column_name='توضیحات',
     attribute='request_description', )
 product_unit = fields.Field(
     column_name='واحد',
     attribute='request_product__product_unit__unit_name', )
 request_branch = fields.Field(
     column_name='شعبه',
     attribute='request_request__request_branch__branch_name', )

 request_date = fields.Field(
     column_name='تاریخ',
     attribute='request_request__request_date', )

 class Meta:
     model = RequestProduct
     fields = ('product_name', 'product_amount','product_unit','product_description','request_date','request_branch',)
     export_order = ('product_name', 'product_amount','product_unit','product_description','request_date','request_branch',)

 def get_queryset(self):
     return self._meta.model.objects.order_by('product_name')


class BranchFilter(admin.SimpleListFilter):
 title = ('شعبه')
 parameter_name = 'request_request__request_branch'

 def lookups(self, request, model_admin):
     role = request.user.groups.all()[0].name

     if role == 'accountant':#TODO
         return (
             ('jannat', 'جنت آباد'),
             ('saadat', 'سعادت آباد'),
             ('poonak', 'پونک'),
             ('hyper', 'هایپراستار'),
             ('golestan', 'گلستان'),
         )
     elif role == 'manager':
         branch = Branch.objects.filter(branch_manager__manager_user=request.user).values('branch_name')[0]
         return (
             (request.user, branch['branch_name']),
         )
     else:
         return (
             ('admin', 'ادمین'),
             ('sample', 'نمونه'),
             ('jannat', 'جنت آباد'),
             ('saadat', 'سعادت آباد'),
             ('poonak', 'پونک'),
             ('hyper', 'هایپراستار'),
             ('golestan', 'گلستان'),
         )




 def queryset(self, request, queryset):

     if self.value() == 'admin':
         return queryset.filter(request_request__request_branch__id=1)
     elif self.value() == 'sample':
         return queryset.filter(request_request__request_branch__id=2)
     elif self.value() == 'poonak':
         return queryset.filter(request_request__request_branch__id=3)
     elif self.value() == 'jannat':
         return queryset.filter(request_request__request_branch__id=4)
     elif self.value() == 'saadat':
         return queryset.filter(request_request__request_branch__id=5)
     elif self.value() == 'golestan':
         return queryset.filter(request_request__request_branch__id=6)
     elif self.value() == 'hyper':
         return queryset.filter(request_request__request_branch__id=7)
     else:
         return queryset.filter()



class BranchLastFilter(admin.SimpleListFilter):
 title = ('آخرین درخواست شعبه')
 parameter_name = 'request_branch'

 def lookups(self, request, model_admin):
     role = request.user.groups.all()[0].name

     if role == 'accountant':#TODO
         return (
             ('jannat', 'آخرین درخواست جنت آباد'),
             ('saadat', 'آخرین درخواست سعادت آباد'),
             ('poonak', 'آخرین درخواست پونک'),
             ('hyper', 'آخرین درخواست هایپراستار'),
             ('golestan', 'آخرین درخواست گلستان'),
         )
     elif role == 'manager':
         branch = Branch.objects.filter(branch_manager__manager_user=request.user).values('branch_name')[0]
         return (
             (request.user, "%s %s"%("آخرین درخواست",branch['branch_name'])),
         )
     else:
         return (
             ('admin', 'آخرین درخواست ادمین'),
             ('sample', 'آخرین درخواست نمونه'),
             ('jannat', 'آخرین درخواست جنت آباد'),
             ('saadat', 'آخرین درخواست سعادت آباد'),
             ('poonak', 'آخرین درخواست پونک'),
             ('hyper', 'آخرین درخواست هایپراستار'),
             ('golestan', 'آخرین درخواست گلستان'),
         )

 def queryset(self, request, queryset):

     if self.value() == 'admin':
         r = Request.objects.filter(request_branch__id=1).latest('id')
         return queryset.filter(Q(request_request__request_branch__id=1)&Q(request_request__id=r.id))
     elif self.value() == 'sample':
         # return queryset.filter(request_branch__id=2)
         r = Request.objects.filter(request_branch__id=2).latest('id')
         return queryset.filter(Q(request_request__request_branch__id=2) & Q(request_request__id=r.id))
     elif self.value() == 'poonak':
         # return queryset.filter(request_branch__id=3)
         r = Request.objects.filter(request_branch__id=3).latest('id')
         return queryset.filter(Q(request_request__request_branch__id=3) & Q(request_request__id=r.id))
     elif self.value() == 'jannat':
         r = Request.objects.filter(request_branch__id=4).latest('id')
         return queryset.filter(Q(request_request__request_branch__id=4) & Q(request_request__id=r.id))
     elif self.value() == 'saadat':
         r = Request.objects.filter(request_branch__id=5).latest('id')
         return queryset.filter(Q(request_request__request_branch__id=5) & Q(request_request__id=r.id))
     elif self.value() == 'golestan':
         r = Request.objects.filter(request_branch__id=6).latest('id')
         return queryset.filter(Q(request_request__request_branch__id=6) & Q(request_request__id=r.id))
     elif self.value() == 'hyper':
         r = Request.objects.filter(request_branch__id=7).latest('id')
         return queryset.filter(Q(request_request__request_branch__id=7) & Q(request_request__id=r.id))
     else:
         return queryset.filter()

class RequestProductAdmin(admin.ModelAdmin):
 # resource_class = RequestProductResource
 list_display = ['id','getrequest_id','branch','request_product','amount','request_amount_sent','request_unit_sent','request_unit','request_description','date','state','add_variance']#,'request_delivered']
 form = AmountForm

 ordering = ['-request_request__request_date']

 fields = ('request_product','request_amount','request_unit','request_amount_sent','request_date','request_time','request_operator')
 # readonly_fields=('')

 def sum(modeladmin, request, queryset):
     s = queryset.aggregate(Sum('request_amount'))
     modeladmin.message_user(request, "جمع : % 6.2f" % s['request_amount__sum'])

 sum.short_description = "جمع مقدار"

 actions = [sum]

 class Meta:
     to_encoding = 'utf-8'

 def get_export_filename(self, file_format):
     print(self)
     filename = "%s.%s" % ("branch_request",
                           file_format.get_extension())
     return filename

 inlines=(RequestProductVarianceInline,)

 def add_variance(self, obj):
     state = RequestProduct.objects.filter(id=obj.id).values(
         'request_request__request_received')[0]
     if state['request_request__request_received'] == '1' or state['request_request__request_received'] == 'closed':
         link = '<a style="padding:5px;border-radius:5px;background: #b65e41;color:white;" href="/admin/AmadoWHApp/requestproduct/%i/change/">کلیک کنید</a>' % obj.id
         return mark_safe(link)
     else:
         link = '<a style="opacity: 0.5;cursor:not-allowed !important;pointer-events: none;padding:5px;border-radius:5px;background-color:gray;color:white;" href="/admin/AmadoWHApp/requestproduct/%i/change/">امکان پذیر نیست</a>' % obj.id
         return mark_safe(link)

 def branch(self,obj):
     return RequestProduct.objects.filter(id=obj.id).values('request_request__request_branch__branch_name')[0]['request_request__request_branch__branch_name']

 def state(self,obj):
     if RequestProduct.objects.filter(id=obj.id).values('request_request__request_received')[0]['request_request__request_received'] == '0':
         return 'درانتظار تایید'
     elif RequestProduct.objects.filter(id=obj.id).values('request_request__request_received')[0]['request_request__request_received'] == '1':
         return 'تایید شده'
     else:
         return 'رد شده'

 def amount(self,u):
     if u.request_unit:
        return '% 12.1f %s'%(u.request_amount,u.request_unit)
     else:
        return '% 12.1f %s'%(u.request_amount,u.request_product.product_unit.unit_name)
        

 # def date(self,obj):
 #     return RequestProduct.objects.filter(id=obj.id).values('request_request__request_date')[0]['request_request__request_date']
 def date(self,obj):
     date = RequestProduct.objects.filter(id=obj.id).values('request_request__request_date')[0][
         'request_request__request_date']
     time = RequestProduct.objects.filter(id=obj.id).values('request_request__request_time')[0]['request_request__request_time']
     return '%s ساعت %s'%(date,time)

 def getrequest_id(self,obj):
     id = RequestProduct.objects.filter(id=obj.id).values('request_request__id')[0]['request_request__id']
     code = RequestProduct.objects.filter(id=obj.id).values('request_request__request_code')[0]['request_request__request_code']
     link = '<a href="../request/%s/change/">%s</a>'%(id,code)
     # return link;
     return mark_safe(link)

 amount.short_description = 'مقدار'
 amount.admin_order_field = 'request_amount'
 state.short_description = 'وضعیت سفارش کلی'
 state.admin_order_field = 'request_request__request_received'
 getrequest_id.admin_order_field = 'request_request'
 getrequest_id.short_description = 'شماره درخواست'
 branch.short_description = 'شعبه درخواست دهنده'
 branch.admin_order_field = 'request_request__request_branch'
 date.short_description = 'تاریخ ثبت درخواست'
 date.admin_order_field = 'request_request__request_date'
 date.state = 'وضعیت'
 add_variance.short_description='ثبت مغایرت'



 list_filter = [BranchLastFilter,'request_unit','request_request__request_branch',DateFilter,'request_product__product_name']
 search_fields = ['request_product__product_name','request_request__request_code']

 def get_queryset(self, request):
     qs = super(RequestProductAdmin, self).get_queryset(request)
     user = request.user
     role = request.user.groups.all()[0].name
     if role == 'manager':
         branch = Branch.objects.filter(branch_manager__manager_user=user).values('id')[0]
         return qs.filter( request_request__request_branch=branch['id'])
     elif role == 'accountant':
         branch = Branch.objects.exclude(id__in=[1, 2]).values('id')
         return qs.filter(request_request__request_branch__in=branch)
     else:
         return qs


 def get_readonly_fields(self, request, obj=None):

     if request.user.is_superuser:
         return list([])

     if obj != None and obj.request_request.request_received != 'waiting' and obj.request_request.request_received != '0':
         
        
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result


     if obj != None and (obj.request_request.request_received == 'waiting' or obj.request_request.request_received == '0'):
         if request.user.has_perm('AmadoWHApp.can_see_requestp'):
             result = list(set(
                 [field.name for field in self.opts.local_fields] +
                 [field.name for field in self.opts.local_many_to_many]
             ))
             result.remove('id')
             return result
         else:
             return list([])

     if obj == None :
         return list([])

     return list([])

     ############################################################

     # role = request.user.groups.all()[0].name
     # if role == 'accountant':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     # if role == 'manager' and obj != None :
     #     if obj.request_request.request_received != '0':
     #         if obj.request_request.request_received == '1':
     #             result = list(set(
     #                 [field.name for field in self.opts.local_fields]
     #             ))
     #             result.remove('id')
     #             return result
     #         else:
     #             result = list(set(
     #                 [field.name for field in self.opts.local_fields] +
     #                 [field.name for field in self.opts.local_many_to_many]
     #             ))
     #             result.remove('id')
     #             return result
     #     else:
     #         return ['request_operator','request_date','request_time']
     # if role == 'amado':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     # return list([])

 def has_delete_permission(self, request, obj=None):
     if request.user.is_superuser:
         return True

     # print(request.user.has_perm('AmadoWHApp.delete_request'))

     if request.user.has_perm('AmadoWHApp.delete_requestproduct') and request.POST and request.POST.get('action') == 'delete_selected':
         ids = request.POST.getlist('_selected_action')
         for i in ids:
             r = RequestProduct.objects.filter(id=int(i)).values('request_request__request_received')
             r = r[0]['request_request__request_received']
             if r == '1' or r == '2' or r == ' confirmed' or r == 'rejected':
                 return False
         return False

     if obj != None and obj.request_request.request_received != '0':
         return False

     if request.user.has_perm('delete_requestproduct') and obj != None:
         return True;

     return False

# def save_model(self, request, instance, form, change):
#     instance.request_operator = request.user


class RequestProductVarianceAdmin(admin.ModelAdmin):
 list_display = ['getrequest_id','request_product','amount','amountrec','request_type','request_operator','branch','date','datev']


 autocomplete_fields = ['request_product']
    
 def date(self, obj):
     return '%s ساعت %s'%(RequestProductVariance.objects.filter(id=obj.id).values('request_product__request_request__request_date')[0][
         'request_product__request_request__request_date'],RequestProductVariance.objects.filter(id=obj.id).values('request_product__request_request__request_time')[0][
         'request_product__request_request__request_time'])

 def datev(self, obj):
     return '%s ساعت %s'%(RequestProductVariance.objects.filter(id=obj.id).values('request_date')[0][
         'request_date'],RequestProductVariance.objects.filter(id=obj.id).values('request_time')[0][
         'request_time'])


 def branch(self, obj):
     return RequestProductVariance.objects.filter(id=obj.id).values('request_product__request_request__request_branch__branch_name')[0][
         'request_product__request_request__request_branch__branch_name']

 def getrequest_id(self,obj):
     id = RequestProductVariance.objects.filter(id=obj.id).values('request_product__request_request__id')[0]['request_product__request_request__id']
     code = RequestProductVariance.objects.filter(id=obj.id).values('request_product__request_request__request_code')[0]['request_product__request_request__request_code']
     link = '<a href="../request/%s/change/">%s</a>'%(id,code)
     # return link;
     return mark_safe(link)

 def amount(self, obj):
     if obj.request_product.request_unit:
        unit = obj.request_product.request_unit
     else:
        unit = obj.request_product.request_product.product_unit
     return '% 12.1f %s'%(RequestProductVariance.objects.filter(id=obj.id).values('request_product__request_amount')[0][
         'request_product__request_amount'],unit)

 search_fields = ['request_product__request_product__product_name']
 list_filter = ['request_product__request_request__request_branch']    

 def amountrec(self, obj):
     if obj.request_unit:
            unit = obj.request_unit
     elif obj.request_product.request_unit:
            unit = obj.request_product.request_unit
     else:
            unit = obj.request_product.request_product.product_unit

     return '% 12.1f %s'%(obj.request_amount_received,unit)
 amountrec.short_description = 'مقدار دریافتی'

 getrequest_id.admin_order_field = 'request_product__request_amount'
 getrequest_id.short_description = 'شماره درخواست'

 amount.admin_order_field = 'request_product__request_request'
 amount.short_description = 'میزان درخواستی'

 branch.short_description = 'شعبه درخواست دهنده'
 branch.admin_order_field = 'request_product__request_request__request_branch__branch_name'
 date.short_description = 'تاریخ ثبت درخواست'
 date.admin_order_field = 'request_product__request_request__request_date'
 datev.short_description = 'تاریخ ثبت مغایرت'
 datev.admin_order_field = 'request_date'

 def get_queryset(self, request):
     qs = super(RequestProductVarianceAdmin, self).get_queryset(request)
     user = request.user
     role = request.user.groups.all()[0].name
     if role == 'manager':
         branch = Branch.objects.filter(branch_manager__manager_user=user).values('id')[0]
         return qs.filter(request_product__request_request__request_branch=branch['id'])
     elif role == 'accountant':
         branch = Branch.objects.exclude(id__in=[1, 2]).values('id')
         return qs.filter(request_product__request_request__request_branch__in=branch)
     else:
         return qs

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if obj == None:
         return list([])
     if request.user.has_perm('AmadoWHApp.can_see_requestpvar'):
         result = list(set(
                 [field.name for field in self.opts.local_fields] +
                 [field.name for field in self.opts.local_many_to_many]
             ))
         result.remove('id')
         return result
     return list([])
     # role = request.user.groups.all()[0].name
     # if role == 'accountant':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     # if role == 'manager' and obj != None:
     #     state = RequestProductVariance.objects.filter(id=obj.id).values('request_product__request_request__request_received')[0]
     #     if state['request_product__request_request__request_received'] != '1':
     #         result = list(set(
     #             [field.name for field in self.opts.local_fields]
     #         ))
     #         result.remove('id')
     #         return result
     #     else:
     #         return list([])
     # if role == 'amado':
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result
     # return list([])

 # has_delete_permission()

 def save_model(self, request, instance, form, change):
     role = request.user.groups.all()[0].name
     if role != 'admin':
         instance.request_operator = request.user


# class MessageRelationshipInline(admin.TabularInline):
#     model = Message.message_replies.through
#     fk_name = 'from_relation'
#     fields = ('from_relation',)

class MessageAdmin(admin.ModelAdmin):
 # inlines=(MessageRelationshipInline,)

 list_display = ('id','message_date','message_user','message_group','message_subject','message_answered')

 fields = ('message_subject','message_text','message_group','message_reply')

 readonly_fields = ('message_date',)


 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])
     if request.user.has_perm('AmadoWHApp.can_see_message'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     if obj != None and obj.message_answered :
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     if obj != None and request.user.has_perm('AmadoWHApp.can_reply_message'):
         return list(['message_subject', 'message_text', 'message_group'])
     elif not request.user.has_perm('AmadoWHApp.can_reply_message'):
         return list(['message_reply'])

     if obj == None:
         return list(['message_reply'])

     return list([])

 def get_queryset(self, request):
     qs = super(MessageAdmin, self).get_queryset(request)
     user = request.user

     role = request.user.groups.all()[0].name
     if role == 'accountant':
         # messages = Message.objects.filter(message_group='انبار/حسابداری').values('id')[0]
         return qs.filter(message_group='warehouse')
     elif role == 'manager':
         return qs.filter(message_user=user)
     else:  # admin
         return qs

 def save_model(self, request, instance, form,change):
     user = request.user
     # user = Branch.objects.get(branch_manager__manager_user=user).values
     instance = form.save(commit=False)

     if not change:
         instance.message_user = user
         instance.message_reply=''
     elif len(instance.message_reply)>0:
         instance.message_answered = True
     instance.save()
     form.save_m2m()
     return instance

# class ShopDetailInline(admin.TabularInline):
#     model = ShopDetail
#     extra = 1
#     # form = RAmountForm
#     # fields = ('product', 'unit','amount',)

#     # def add_view(self, request, form_url='', extra_context=None):
#     #     if not request.user.is_superuser:
#     #         self.exclude = ('activa',)
#     #     return super(ShopDetailInline, self).add_view(request, form_url='', extra_context=None)

#     def get_fields(self, request, obj=None):
#         if obj == None:
#             return ('product', 'unit','amount','wh_amount','purchase_durability','last_price',)
#         else:
#             if obj.status == 'received' or obj.status == '3':
#                 return ('product', 'unit', 'amount','rc_amount','rc_date',)
#             else:
#                 return ('product', 'unit', 'amount', 'wh_amount','purchase_durability', 'last_price',)

#     autocomplete_fields = ['product']


#     def get_readonly_fields(self, request, obj=None):
#         if request.user.is_superuser:
#             return list([])

#         if obj == None:
#             return list([])

#         if obj.status == 'confirmed' or obj.status == 'declined' :
#             result = list(set(
#                 [field.name for field in self.opts.local_fields] +
#                 [field.name for field in self.opts.local_many_to_many]
#             ))
#             result.remove('id')
#             return result

#         if obj.status == 'received':
#             result = list(set(
#                 [field.name for field in self.opts.local_fields] +
#                 [field.name for field in self.opts.local_many_to_many]
#             ))
#             result.remove('id')
#             result.remove('rc_amount')
#             result.remove('rc_date')
#             return result

#         if request.user.has_perm('AmadoWHApp.can_can_see_shopdet'):
#             result = list(set(
#                 [field.name for field in self.opts.local_fields] +
#                 [field.name for field in self.opts.local_many_to_many]
#             ))
#             result.remove('id')
#             return result

#         return list([])

# class ShopRequestAdmin(admin.ModelAdmin):
#     inlines=(ShopDetailInline,)


#     list_display = ['id','from_date','supplier','status','submit_user','submit_date','confirm_user']




#     def get_readonly_fields(self, request, obj=None):
#         if request.user.is_superuser:
#             return list([])

#         if obj == None:
#             return list(['status','submit_user','submit_date','confirm_user','confirm_date'])

#         if obj.status == 'confirmed' or obj.status == 'declined' or obj.status == 'received':
#             result = list(set(
#                 [field.name for field in self.opts.local_fields] +
#                 [field.name for field in self.opts.local_many_to_many]
#             ))
#             result.remove('id')
#             return result

#         if request.user.has_perm('AmadoWHApp.can_can_see_shopdet'):
#             result = list(set(
#                 [field.name for field in self.opts.local_fields] +
#                 [field.name for field in self.opts.local_many_to_many]
#             ))
#             result.remove('id')
#             return result

#         return list(['status', 'submit_user', 'submit_date', 'confirm_user', 'confirm_date'])

#     def save_model(self, request, instance, form, change):

#         user = request.user
#         role = request.user.groups.all()[0].name
#         if not change:

#             if not request.user.is_superuser:
#                 instance.submit_user = request.user
#                 instance.submit_date = jdatetime.datetime.now()

#         instance = form.save(commit=False)

#         instance.save()
#         form.save_m2m()
#         return instance


#     def confirm(self, request, qs):
#         role = request.user.groups.all()[0].name
#         if not request.user.has_perm('AmadoWHApp.can_confirm_shopreq'):
#             messages.error(request, "شما اجازه تایید ندارید")
#             return
#         flag = False
#         for q in qs:
#             if q.status == 'received':
#                 flag = True
#         if not flag:
#             for q in qs:
#                 q.status = 'confirmed'
#                 q.confirm_user = request.user
#                 q.confirm_date = jdatetime.datetime.now()
#                 q.save()
#             self.message_user(request, "%i خرید تایید شد" % qs.count())
#             return qs
#         else:
#             messages.error(request, "امکان تایید برخی یا همه پرداخت ها وجود ندارد")

#     confirm.short_description = 'تایید خرید های انتخاب شده'

#     def decline(self, request, qs):
#         if not request.user.has_perm('AmadoWHApp.can_confirm_shopreq'):
#             messages.error(request, "شما اجازه رد ندارید")
#             return
#         flag = False
#         for q in qs:
#             if q.status == 'received':
#                 flag = True
#         if not flag:
#             for q in qs:
#                 q.status = 'declined'
#                 q.confirm_user = request.user
#                 q.confirm_date = jdatetime.datetime.now()
#                 q.save()
#             self.message_user(request, "%i خرید رد شد" % qs.count())
#             return qs
#         else:
#             messages.error(request, "امکان رد برخی یا همه پرداخت ها وجود ندارد")

#     decline.short_description = 'رد خرید های انتخاب شده'

#     def receive(self, request, qs):
#         flag = False
#         for q in qs:
#             if q.status != 'confirmed':
#                 flag = True
#         if not flag:
#             for q in qs:
#                 q.status = 'received'
#                 q.pay_user = request.user
#                 q.pay_date = jdatetime.datetime.now()
#                 q.save()
#             self.message_user(request, "%i خرید دریافت شد" % qs.count())
#             return qs
#         else:
#             messages.error(request, "امکان دریافت برخی یا همه خرید ها وجود ندارد")

#     receive.short_description = 'تغییر وضعیت خرید به دریافت شده'

#     actions = [confirm,decline,receive]


class ShopDetailInline(admin.TabularInline):
 model = ShopDetail
 extra = 0
 def get_fields(self, request, obj=None):
    if not request.user.is_superuser:
        return list(['product','definitive_product','unit','amount','last_price'])
    else:
        return ('product','definitive_product', 'unit', 'amount', 'wh_amount','purchase_durability', 'last_price', )
# def get_fields(self, request, obj=None):
#     if obj == None:
#         return ('product','definitive_product', 'unit','amount','wh_amount','purchase_durability','last_price',)
#     else:
#         if obj.status == 'received' or obj.status == '3':
#             return ('product','definitive_product', 'unit', 'amount','rc_amount','rc_date',)
#         else:
#             return ('product','definitive_product', 'unit', 'amount', 'wh_amount','purchase_durability', 'last_price', )

 autocomplete_fields = ['product']


 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if obj == None:
         return list([])

     # if obj.status == 'confirmed' or obj.status == 'declined' :
     #     result = list(set(
     #         [field.name for field in self.opts.local_fields] +
     #         [field.name for field in self.opts.local_many_to_many]
     #     ))
     #     result.remove('id')
     #     return result

     if obj.status == 'done':
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         result.remove('rc_amount')
         result.remove('rc_date')
         return result

     if request.user.has_perm('AmadoWHApp.can_can_see_shopdet'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     return list([])


class ShopFilter(admin.SimpleListFilter):
 title = ('وضعیت')
 parameter_name = 'status'

 def choices(self, cl):
     for lookup, title in self.lookup_choices:
         yield {
             'selected': self.value() == lookup,
             'query_string': cl.get_query_string({
                 self.parameter_name: lookup,
             }, []),
             'display': title,
         }

 def lookups(self, request, model_admin):
     return (
         ('all', 'همه'),
         ('notdone', 'انجام نشده'),
         ('submitted', 'ثبت شده/در انتظار تایید'),
         ('confirmed', 'تایید شده/در انتظار خرید'),
         ('done', 'خرید شده/در انتظار دریافت'),
         ('declined', 'رد شده'),
         ('received', 'دریافت شده'),

     )

 def queryset(self, request, queryset):
     if self.value() == None:
         r = queryset.exclude(Q(status='done')|Q(status='received')).order_by('from_date')
     elif self.value() == 'notdone':
         r = queryset.exclude(Q(status='done')|Q(status='received')).order_by('from_date')
     elif self.value() == 'submitted':
         r = queryset.filter(status='submitted').order_by('from_date')
     elif self.value() == 'confirmed':
         r = queryset.filter(status='confirmed').order_by('from_date')
     elif self.value() == 'done':
         r = queryset.filter(status='done').order_by('from_date')
     elif self.value() == 'declined':
         r = queryset.filter(status='declined').order_by('from_date')
     elif self.value() == 'received':
         r = queryset.filter(status='received').order_by('from_date')
     else:
         r = queryset

     return r

class ShopPaymentInline(admin.TabularInline):
 autocomplete_fields = ['checkp', 'fund', 'cash']
 model = RelationShip
 extra = 1


class ShopRequestAdmin(admin.ModelAdmin):
 inlines=(ShopDetailInline,ShopPaymentInline)
# inlines=[ShopPaymentInline]

 list_per_page = 100
    

 def save_related(self, request, form, formsets, change):
     super(ShopRequestAdmin, self).save_related(request, form, formsets, change)
     dets = ShopDetail.objects.filter(shop=form.instance)
     data = []
     for d in dets:
         data.append(
             {
                 'id':d.product.id,
                 'cost':d.last_price,
                 'date':d.shop.from_date.strftime('%Y-%m-%d')
             }
         )

#     resp = requests.post(
#         "http://amadowh.ir/ac/report/setprice",
#         headers={
#             "Accept": "application/json"
#         },
#         data={'data':json.dumps(data)})

 list_display = ['see','getid', 'date', 'supplier','summary','tot_cost','finish_date', 'getstatus', 'submit_user', 'to_day', 'confirm_user']
 list_filter = [ShopFilter]

 autocomplete_fields = ['supplier']


 search_fields =['id','supplier__supplier_name','supplier__supplier_company']


 def get_search_results(self, request, queryset, search_term):
     defqueryset = queryset
     queryset, use_distinct = super(ShopRequestAdmin, self).get_search_results(request, queryset, search_term)

     try:
         # search_term_as_int = int(search_term)
         s = ShopDetail.objects.filter(Q(product__product_name__contains=search_term)&Q(shop__in=defqueryset)).values('shop__id')
         ids = []
         for ss in s:
             ids.append(ss['shop__id'])

         queryset |= self.model.objects.filter(id__in=ids)
     except:
         pass
     return queryset, use_distinct

 def getid(self, obj):
     return obj.pk

 getid.short_description = 'شناسه'
 getid.admin_order_field = 'id'

 def finish_date(self,obj):
     d = obj.from_date
     detail = ShopDetail.objects.filter(shop=obj)[0]
     p = detail.purchase_durability
     if p != 0:
         d = d+datetime.timedelta(p-2)
         return d.strftime('%Y-%m-%d')
     return 'اطلاعاتی در دسترس نیست'

 finish_date.short_description = 'پیشبینی تاریخ خرید دوباره'

 def see(self, obj):
     return mark_safe('<a href="./%i/change">مشاهده </a>' % obj.id)

 see.short_description = 'لینک'

 ordering = ['-from_date']

 class Media:
     css = {
         'all': ('shopcss.css',)
     }

 def tot_cost(self,obj):
     details = ShopDetail.objects.filter(shop=obj)
     s = 0
     for d in details:
         s += d.amount*d.last_price

     return int(s)

 def summary(self,obj):
     ol = '<ul>'
     str = ''
     details = ShopDetail.objects.filter(shop=obj)
     if details.count() > 5:
         details = details[:5]
         str += '...'
     if details.count() > 1:
         for d in details:
             ol += '<li>'
             try:
                ol += '%s (%i %s)'%(d.product.product_name,d.amount,d.unit.unit_name)
             except:
                ol += '%s (%i %s)'%(d.product.product_name,d.amount,'')
             ol += '</li>'

         ol+='</ul>'+str

         return mark_safe(ol)
     else:
         d = details[0]
         try:
                return '%s (%i %s)'%(d.product.product_name,d.amount,d.unit.unit_name)
         except:
                return '%s (%i %s)'%(d.product.product_name,d.amount,'')

 summary.short_description = 'خلاصه خرید'

 tot_cost.short_description = 'تخمین هزینه خرید(تومان)'

 def to_day(self,obj):
     return obj.submit_date.strftime('%Y-%m-%d')

 to_day.short_description = 'تاریخ ثبت'
 to_day.admin_order_field = 'submit_date'

 def date(self, obj):

     days = (
         (0, 'شنبه'),
         (1, 'یکشنبه'),
         (2, 'دوشنبه'),
         (3, 'سه شنبه'),
         (4, 'چهارشنبه'),
         (5, 'پنجشنبه'),
         (6, 'جمعه'),
     )

     l = '%s - %s' % (obj.from_date, days[obj.from_date.weekday()][1])
     if obj.status == 'received' or obj.status == 3:
         return l
     t = jdatetime.datetime.today().strftime('%Y-%m-%d')
     if obj.from_date.strftime('%Y-%m-%d') < t:
         link = '<span style="padding:0 5px;border-radius:5px;background: #f25252;" >%s</span>' % l
     elif obj.from_date.strftime('%Y-%m-%d') == t:
         link = '<span style="padding:0 5px;border-radius:5px;background: #f9e36b;" >%s</span>' % l
     else:
         link = '<span style="padding:0 5px;border-radius:5px;background: #98f970;" >%s</span>' % l

     return mark_safe(link)

 date.short_description = 'تاریخ خرید'
 date.admin_order_field = ['from_date']

 change_list_template = 'shop_change_list.html'


 def getstatus(self, obj):

     if obj.status == 'submitted':
         link = '<span style="padding:5px;border-radius:5px;background: #fcf8e3;" ><i class="fas fa-clock"></i></span>'
     elif obj.status == 'confirmed':
         link = '<span style="padding:5px;border-radius:5px;background: #d9edf7;" ><i class="fas fa-check-circle"></i></span>'
     elif obj.status == 'declined':
         link = '<span style="padding:5px;border-radius:5px;background: #f2dede;" ><i class="fas fa-times-circle"></i></span>'
     elif obj.status == 'done':
         link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" ><i class="fas fa-check-double"></i></span>'
     else:
         link = '<span style="padding:5px;border-radius:5px;background: lightfrey;" ><i class="fas fa-truck"></i></span>'

     return mark_safe(link)

 getstatus.short_description = "وضعیت"


 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if obj == None:
         return list(['status','submit_user','submit_date','confirm_user','confirm_date'])

     if obj.status == 'done':
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     if request.user.has_perm('AmadoWHApp.can_can_see_shopdet'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result
     if request.user.username == 'kimiaee':
         return list(['submit_user', 'submit_date', 'confirm_user', 'confirm_date'])

     return list(['status', 'submit_user', 'submit_date', 'confirm_user', 'confirm_date'])

 def save_model(self, request, instance, form, change):

     user = request.user
     role = request.user.groups.all()[0].name
     if not change:

         if not request.user.is_superuser:
             instance.submit_user = request.user
             instance.submit_date = jdatetime.datetime.now()

     instance = form.save(commit=False)

     instance.save()
     form.save_m2m()
     return instance


 def confirm(self, request, qs):
     role = request.user.groups.all()[0].name
     if not request.user.has_perm('AmadoWHApp.can_confirm_shopreq'):
         messages.error(request, "شما اجازه تایید ندارید")
         return
     flag = False
     for q in qs:
         if q.status == 'received':
             flag = True
     if not flag:
         for q in qs:
             q.status = 'confirmed'
             q.confirm_user = request.user
             q.confirm_date = jdatetime.datetime.now()
             q.save()
         self.message_user(request, "%i خرید تایید شد" % qs.count())
         return qs
     else:
         messages.error(request, "امکان تایید برخی یا همه پرداخت ها وجود ندارد")

 confirm.short_description = 'تایید خرید های انتخاب شده'

 def decline(self, request, qs):
     if not request.user.has_perm('AmadoWHApp.can_confirm_shopreq'):
         messages.error(request, "شما اجازه رد ندارید")
         return
     flag = False
     for q in qs:
         if q.status == 'received':
             flag = True
     if not flag:
         for q in qs:
             q.status = 'declined'
             q.confirm_user = request.user
             q.confirm_date = jdatetime.datetime.now()
             q.save()
         self.message_user(request, "%i خرید رد شد" % qs.count())
         return qs
     else:
         messages.error(request, "امکان رد برخی یا همه پرداخت ها وجود ندارد")

 decline.short_description = 'رد خرید های انتخاب شده'

 def receive(self, request, qs):
     flag = False
     for q in qs:
         if q.status != 'done':
             flag = True
     if not flag:
         for q in qs:
             q.status = 'received'
             q.pay_user = request.user
             q.pay_date = jdatetime.datetime.now()
             q.save()
         self.message_user(request, "%i خرید دریافت شد" % qs.count())
         return qs
     else:
         messages.error(request, "امکان دریافت برخی یا همه خرید ها وجود ندارد")

 receive.short_description = 'تغییر وضعیت خرید به دریافت شده'

 def done(self, request, qs):
     flag = False
     for q in qs:
         if q.status != 'confirmed':
             flag = True
     if not flag:
         for q in qs:
             q.status = 'done'
             q.pay_user = request.user
             q.pay_date = jdatetime.datetime.now()
             q.save()
         self.message_user(request, "%i خرید انجام شد" % qs.count())
         return qs
     else:
         messages.error(request, "امکان انجام برخی یا همه خرید ها وجود ندارد")

 done.short_description = 'تغییر وضعیت خرید به انجام شده'

 actions = [confirm,decline,done,receive]


class BranchWarehouseProductInline(admin.TabularInline):
 model=BranchWarehouseProduct
# extra = Product.objects.filter(product_branch_warehouse=True).count()
 extra = 0

 def get_formset(self, request, obj=None, **kwargs):
     if obj is None:
            
         if request.user.has_perm('AmadoWHApp.can_see_special_products'):
            ps = Product.objects.filter(product_branch_warehouse=True).values('id','product_name','product_second_unit__unit_name')     
            kwargs['extra'] = ps.count()
         else :
            ps = Product.objects.filter(Q(product_branch_warehouse=True)&~Q(id__in=[434,377,441,439,271,348,440,418,378,272,322,442,356,353,443,430,444,276,270])).values('id','product_name','product_second_unit__unit_name')  
            
            kwargs['extra'] = ps.count()
         
#         kwargs['extra'] = 0
         return super(BranchWarehouseProductInline, self).get_formset(request, obj, **kwargs)

     kwargs['extra'] = 0
     return super(BranchWarehouseProductInline, self).get_formset(request, obj, **kwargs)

 exclude=()

 fields = ['product','amount','getunit','description',]

 autocomplete_fields = ['product',]


 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list(['getunit'])

     if obj == None:
         return list(['getunit'])

     if request.user.has_perm('AmadoWHApp.can_see_brawarpro'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]+['getunit']
         ))
         result.remove('id')
         return result

     if obj.status == 'registered' or obj.status == '0':
         return list(['getunit'])
     else:
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]+['getunit']
         ))
         result.remove('id')
         return result

     return list(['getunit'])



class BranchWarehouseAdmin(admin.ModelAdmin):
 inlines=[BranchWarehouseProductInline]

 list_filter = ['branch']

# list_display = ['see','getid','date','status','branch','submit_user','getdate','description','link','link2']
 list_display = ['see','getid','date','status','branch','submit_user','getdate','description','link']

 def link(self,obj):
#    if obj.status == 'confirmed' or obj.status == 'byadmin':
    return mark_safe('<a target=_blank style="padding:5px;border-radius:5px;background: #b65e41;color:white;"   href="../../../report/branchvar/%i/">مشاهده مغایرت روزانه شعبه</a>'%obj.id)
#    else:
#        return mark_safe('<a style="padding:5px;border-radius:5px;background: grey;color:white;color: currentColor;cursor: not-allowed;opacity: 0.5;text-decoration: none;">مشاهده مغایرت روزانه شعبه</a>')

 link.short_description = 'مغایرت'

 def link2(self, obj):
    if obj.status == 'confirmed' or obj.status == 'byadmin':
        return mark_safe(
            '<a target=_blank style="padding:5px;border-radius:5px;background: #b65e41;color:white;"   href="../../../report/branchvarsum/%i/">مشاهده مغایرت تجمعی شعبه</a>' % obj.id)
    else:
        return mark_safe(
            '<a style="padding:5px;border-radius:5px;background: grey;color:white;color: currentColor;cursor: not-allowed;opacity: 0.5;text-decoration: none;">مشاهده مغایرت روزانه شعبه</a>')

 link2.short_description = 'مغایرت'
    
 def getdate(self,obj):
     return obj.submit_date.strftime('روز %d-%m-%Y ساعت %H:%M')

 getdate.short_description = 'زمان ثبت'
 getdate.admin_order_field = 'submit_date'

 def add_view(self, request, form_url='', extra_context=None):
     extra_context = extra_context or {}
     
     if request.user.has_perm('AmadoWHApp.can_see_special_products'):
        ps = Product.objects.filter(product_branch_warehouse=True).values('id','product_name','product_second_unit__unit_name')       
        extra_context['products'] = list(ps)
        extra_context['count'] = ps.count()
     else :
        ps = Product.objects.filter(Q(product_branch_warehouse=True)&~Q(id__in=[434,377,441,439,271,348,440,418,378,272,322,442,356,353,443,430,444,276,270])).values('id','product_name','product_second_unit__unit_name')      
        
       
        
        extra_context['products'] = list(ps)
        extra_context['count'] = ps.count()
        
        print(extra_context['count'])
        
     
     return super(BranchWarehouseAdmin, self).change_view(
         request, None, form_url, extra_context=extra_context,
     )

 change_form_template = 'warehouse_change_form.html'

 def confirm(self, request, qs):
     if not request.user.has_perm('AmadoWHApp.can_confirm_branchwh'):
         messages.error(request, "شما اجازه تایید ندارید")
         return

     for q in qs:
         q.status = 'confirmed'
         q.confirm_user = request.user
         q.confirm_date = jdatetime.datetime.now()
         q.save()
     self.message_user(request, "%i موجودی تایید شد" % qs.count())
     return qs

 confirm.short_description = 'تایید موجودی های انتخاب شده'

 actions = ['confirm']

 def getid(self, obj):
     return obj.pk

 getid.short_description = 'شناسه'
 getid.admin_order_field = 'id'

 def see(self, obj):
     return mark_safe('<a href="./%i/change">مشاهده </a>' % obj.id)

 see.short_description = 'لینک'

 # list_filter = [ShopFilter]

 ordering = ['-date']

 def to_day(self,obj):
     return obj.submit_date.strftime('%Y-%m-%d')

 to_day.short_description = 'تاریخ ثبت'
 to_day.admin_order_field = 'submit_date'


 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if obj == None:
         return list(['branch','submit_user','submit_date','status','confirm_user','confirm_date'])

     if request.user.has_perm('AmadoWHApp.can_see_brawar'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     if obj.status == 'registered':
         return list(['branch','submit_user','submit_date','status','confirm_user','confirm_date'])
     else:
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     return list(['branch', 'submit_user', 'submit_date','status','confirm_user','confirm_date'])

 def save_model(self, request, instance, form, change):

     user = request.user
     role = request.user.groups.all()[0].name
     if not change:

         if not request.user.is_superuser:
             instance.submit_user = request.user
             instance.submit_date = jdatetime.datetime.now()
             instance.branch = Branch.objects.get(branch_manager__manager_user=request.user)

     instance = form.save(commit=False)

     instance.save()
     form.save_m2m()
     return instance

 def get_queryset(self, request):
     user = request.user
     role = request.user.groups.all()[0].name

     qs = super(BranchWarehouseAdmin, self).get_queryset(request)

     if role == 'manager':
         b = Branch.objects.get(branch_manager__manager_user=request.user)
         return qs.filter(branch=b)
     return qs

class Recipe23Inline2 (admin.TabularInline):
 extra = 1
 model = Recipe23
 autocomplete_fields = ['recipe_parent_product']

class AmadoFoodAdmin(admin.ModelAdmin):
 list_display = ['id','name','current_price','previous_price','product_is_active']
 search_fields = ['name']
    
 list_filter = ['product_is_active']    
    
 inlines = [Recipe23Inline2]
    


 def get_model_perms(self, request):
     if request.user.is_superuser or not request.user.has_perm('AmadoWHApp.can_see_food'):
         perms = admin.ModelAdmin.get_model_perms(self, request)
         return perms
     return {}


class FoodSaleProductInline(admin.TabularInline):
 model=FoodSaleProduct
 extra = AmadoFood.objects.filter(product_is_active=True).count()
 def get_formset(self, request, obj=None, **kwargs):
     ## Put in your condition here and assign extra accordingly
     if obj is None:
         return super(FoodSaleProductInline, self).get_formset(request, obj, **kwargs)

     count = AmadoFood.objects.filter(product_is_active=True).count()

     kwargs['extra'] = 0
     return super(FoodSaleProductInline, self).get_formset(request, obj, **kwargs)

 exclude=()

 autocomplete_fields = ['product',]

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if obj == None:
         return list([])

     if obj.is_closed:
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     if request.user.has_perm('AmadoWHApp.can_see_productfoodsales'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     return list([])


class FoodSaleAdmin(admin.ModelAdmin):
 inlines = [FoodSaleProductInline]

 list_display = ['see','getid','getdate','branch','get_totf','status','submit_date']
 list_filter = ['branch']

 def add_view(self, request, form_url='', extra_context=None):
     extra_context = extra_context or {}
     ps = AmadoFood.objects.filter(product_is_active=True).values('id','name')
     extra_context['products'] = list(ps)
     extra_context['count'] = ps.count()
     return super(FoodSaleAdmin, self).change_view(
         request, None, form_url, extra_context=extra_context,
     )

 change_form_template = 'foodsale_change_form.html'

 ordering = ['-date']

 def get_tot(self,obj):
     ds = FoodSaleProduct.objects.filter(sale=obj)
     tot=0
     for d in ds:
         tot += (d.amount*d.product.current_price)

     return tot

 get_tot.short_description = 'کل درآمد فروش'

 def get_totf(self,obj):
     ds = FoodSaleProduct.objects.filter(sale=obj)
     tot = 0
     for d in ds:
         tot += d.amount

     return tot

 get_totf.short_description = 'تعداد کل غذای فروخته شده'

 def getid(self, obj):
     return obj.pk

 getid.short_description = 'شناسه'
 getid.admin_order_field = 'id'

 def see(self, obj):
     return mark_safe('<a href="./%i/change">مشاهده </a>' % obj.id)

 see.short_description = 'لینک'


 def getdate(self, obj):

     days = (
         (0, 'شنبه'),
         (1, 'یکشنبه'),
         (2, 'دوشنبه'),
         (3, 'سه شنبه'),
         (4, 'چهارشنبه'),
         (5, 'پنجشنبه'),
         (6, 'جمعه'),
     )

     l = '%s - %s' % (obj.date, days[obj.date.weekday()][1])

     return l

 getdate.short_description = 'تاریخ فروش'
 getdate.admin_order_field = 'date'

 def status(self,obj):
     if obj.is_closed:
         return 'بسته می باشد'

     return 'برای ویرایش باز می باشد'

 status.short_description = 'وضعیت'

 def close(self, request, qs):
     role = request.user.groups.all()[0].name
     if not request.user.has_perm('AmadoWHApp.can_close_foodsales'):
         messages.error(request, "شما اجازه بستن ندارید")
         return
     flag = False
     for q in qs:
         if q.is_closed:
             flag = True
     if not flag:
         for q in qs:
             q.is_closed = True
             q.confirm_user = request.user
             q.confirm_date = jdatetime.datetime.now()
             q.save()
         self.message_user(request, "%i فروش بسته شد" % qs.count())
         return qs
     else:
         messages.error(request, "امکان بستن برخی یا همه فروش ها وجود ندارد")

 close.short_description = 'بستن فروش های انتخاب شده'

 actions = [close]

 def get_readonly_fields(self, request, obj=None):
     if request.user.is_superuser:
         return list([])

     if obj == None:
         return list(['is_closed','branch','submit_user','submit_date','confirm_user','confirm_date'])

     if obj.is_closed:
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     if request.user.has_perm('AmadoWHApp.can_see_foodsales'):
         result = list(set(
             [field.name for field in self.opts.local_fields] +
             [field.name for field in self.opts.local_many_to_many]
         ))
         result.remove('id')
         return result

     return list(['is_closed','branch', 'submit_user', 'submit_date', 'confirm_user', 'confirm_date'])

 def get_queryset(self, request):

     qs = super(FoodSaleAdmin, self).get_queryset(request)
     role = request.user.groups.all()[0].name
     if role == 'manager':
         b = Branch.objects.get(branch_manager__manager_user=request.user)
         return qs.filter(branch=b)
     return qs

 def save_model(self, request, instance, form, change):
     user = request.user
     role = request.user.groups.all()[0].name
     if not change:

         if not request.user.is_superuser:
             instance.submit_user = request.user
             instance.submit_date = jdatetime.datetime.now()
             instance.branch = Branch.objects.get(branch_manager__manager_user=request.user)

     instance = form.save(commit=False)

     instance.save()
     form.save_m2m()
     return instance

class FSPAdmin(admin.ModelAdmin):
 list_display = ['id','product','sale','amount']

 search_fields = ['product__name']
 list_filter = ['product','sale__branch']

class GroupAdmin(admin.ModelAdmin):
 filter_horizontal = ['permissions']

class UserAdmin(admin.ModelAdmin):
 filter_horizontal = ['user_permissions']    

from AmadoWH.mysite import site


from django.contrib.admin.views.main import ChangeList
from django_jalali.admin.filters import JDateFieldListFilter

class ShopDetailAdmin(admin.ModelAdmin):
 list_display = ['id','get_date','get_supplier','get_pname','last_price','get_amount','get_price']

 list_per_page = 200
    
 def get_supplier(self,obj):
    return obj.shop.supplier

 get_supplier.short_description = 'تامین کننده'
 get_supplier.admin_order_field = 'shop__supplier'

 def get_pname(self,obj):
     return obj.product.product_name;

 get_pname.short_description = 'محصولات'
 get_pname.admin_order_field = 'product'

 def get_amount(self,obj):
     return '%i %s'%(obj.amount,obj.unit)

 get_amount.admin_order_field = 'amount'
 get_amount.short_description = 'میزان/مقدار'

 def get_price(self,obj):
     if obj.last_price >0:
         return int(obj.amount*obj.last_price)
     else:
         return 'اطلاعاتی در دسترس نیست'

 get_price.short_description = 'قیمت (تومان)'

 def get_date(self,obj):
     return obj.shop.from_date.strftime('%Y-%m-%d')

 change_list_template = 'supplier_change_list.html'

 get_date.short_description = 'تاریخ'
 get_date.admin_order_field = 'shop__from_date'

 ordering = ['-shop__from_date']

 list_filter = ['shop__supplier','product',('shop__from_date', JDateFieldListFilter)]

 class Media:
     js = (
         'https://ajax.googleapis.com/ajax/libs/jquery/2.2.3/jquery.min.js',
         )

 def get_model_perms(self, request):
     if request.user.is_superuser :
         perms = admin.ModelAdmin.get_model_perms(self, request)
         return perms
     return {}



 def get_changelist(self, request):
     class MyChangeList(ChangeList):
         def get_results(self, *args, **kwargs):
             super(MyChangeList, self).get_results(*args, **kwargs)
             # rs = self.result_list.aggregate(tomato_sum=Sum('get_price'))
             sum = 0
             for r in self.result_list:
                 sum += r.amount*r.last_price
             self.tomato_count = int(sum)
             ps = ShopDetail.objects.all().values('product__id')
             self.products = RawProduct.objects.filter(id__in=[ps]).values('id','product_name').order_by('product_name')
             self.suppliers = Supplier.objects.all().values('id','supplier_name','supplier_company').order_by('supplier_name')
     return MyChangeList


site.site_header = 'انبارداری آمادو'
site.site_title = 'انبارداری آمادو'
site.index_title = 'سیستم سفارشات آمادو'


class LogAdmin(admin.ModelAdmin):
 search_fields = ['user__first_name','user__last_name']
 list_display= ['id','user','content_type','object_id','get_action','action_time','object_repr','__str__']
 list_filter=['content_type','action_time','user','action_flag',]
 list_per_page = 100

 def get_action(self,obj):
     if obj.action_flag == 1:
         return 'افزودن'
     if obj.action_flag == 2:
         return 'تغییر'
     if obj.action_flag == 3:
         return 'حذف'

 get_action.short_description = 'نشانه عمل'
 get_action.admin_order_field = 'action_flag'
    
    
class Recipe12Inline1 (admin.TabularInline):
 extra = 1
 model = Recipe12
 autocomplete_fields = ['recipe_child_product']    

class RawProductAdmin(admin.ModelAdmin):
 list_display = ['id','product_name','product_is_active']
 search_fields = ['product_name','id']
    
 inlines = [UnitToUnitInline,Recipe12Inline1]
    
 list_filter = ['product_is_active']

 def get_fields(self, request, obj=None):
     if not request.user.is_superuser:
        return list(['product_name'])
     else:
        return list(['product_name'])
        

 def get_search_results(self, request, queryset, search_term):
     if not request.user.is_superuser :
         queryset, use_distinct = super().get_search_results(request, queryset, search_term)
         queryset &= self.model.objects.filter(product_is_active=True)
         return queryset, use_distinct
     else:
         queryset, use_distinct = super().get_search_results(request, queryset, search_term)
         return queryset, use_distinct

    
class Recipe23Admin(admin.ModelAdmin):
    list_display = ['id','recipe_child_product','recipe_amount','recipe_unit','recipe_parent_product']
    search_fields = ['recipe_child_product__name']    
    
    
class Recipe12Admin(admin.ModelAdmin):
    list_display = ['id','recipe_child_product','recipe_amount','recipe_unit','recipe_parent_product']
#    search_fields = ['recipe_child_product__product_name']    
        
class FoodSaleProductAdmin(admin.ModelAdmin):
    list_display=['product','amount','get_date']
    def get_date(self,obj):
        return obj.sale.date
    list_filter=[('sale__date', JDateFieldListFilter),'product']
    search_fields=['product__name']
    
   
site.register(Unit,UnitAdmin)
site.register(FoodSaleProduct,FoodSaleProductAdmin)
site.register(Warehouse,WarehouseAdmin)
site.register(Supplier,SupplierAdmin)
site.register(ProductCategory,ProductCategoryAdmin)
site.register(Product,ProductAdmin)
site.register(Manager,ManagerAdmin)
site.register(Branch,BranchAdmin)
site.register(Warehouse_Product,Warehouse_ProductAdmin)
site.register(Request,RequestAdmin)
site.register(RequestProduct,RequestProductAdmin)
site.register(RequestProductVariance,RequestProductVarianceAdmin)
site.register(Message,MessageAdmin)
# admin.site.register(SalesCategory)

site.register(ShopRequest,ShopRequestAdmin)
site.register(ShopDetail,ShopDetailAdmin)
site.register(BranchWarehouse,BranchWarehouseAdmin)

site.register(RawProduct,RawProductAdmin)

site.register(DefinitiveProduct)

site.register(Recipe12,Recipe12Admin)
site.register(Recipe23,Recipe23Admin)

site.register(LogEntry,LogAdmin)

from django.contrib.auth.models import Permission,User,Group

site.register(Permission)
site.register(User,UserAdmin)
site.register(Group,GroupAdmin)
site.register(FoodSale,FoodSaleAdmin)
site.register(AmadoFood,AmadoFoodAdmin)

site.register(Price)
site.register(UnitToUnit)
#site.register(FoodSaleProduct,FSPAdmin)
