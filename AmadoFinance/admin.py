from django.contrib import admin
from django.contrib.auth.models import User
import jdatetime
from django_jalali.db import models as jmodels
from django.utils.safestring import mark_safe
from django import forms
from AmadoFinance.models import Sales, RecipientCompany, Bank, PaymentCategory, CashPayment, CheckPayment, \
    CheckCategory, FactorImage, RecedeImage, \
    FundPayment, Pos, PosSale, InternetSeller, InternetSale, RelationShip, BankAccount,CostCenter
from AmadoWHApp.models import Product, Branch
from django import forms
from django_jalali.admin.filters import JDateFieldListFilter
from django.contrib import messages
from xlwt import Workbook as _WB_, Font, XFStyle, Borders, Alignment
from django.db.models import Q, Sum
from django.shortcuts import redirect
from django.contrib.admin.views.main import ChangeList

import requests

class CurrencyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)
        try:
            self.fields['sales_date'].initial = jdatetime.datetime.today()  # TODO
        except:
            None

    class Meta:
        exclude = ()
        model = Product
        widgets = {
            'sales_cash_cost': forms.NumberInput(attrs={'step': 500, 'min': 0, 'size': '100', 'localization': True}),
            'sales_tot_cash_cost': forms.NumberInput(
                attrs={'step': 500, 'min': 0, 'size': '100', 'localization': True}),
            'sales_delivery_cost': forms.NumberInput(
                attrs={'step': 1000, 'min': 0, 'size': '100', 'localization': True}),
            'cost': forms.NumberInput(attrs={'step': 1000, 'min': 0, 'size': '100', 'localization': True}),
        }


class InternetAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        if request.user.has_perm('AmadoFinance.add_internetseller'):
            perms = admin.ModelAdmin.get_model_perms(self, request)
            return perms
        return {}

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            return list([])

        if request.user.has_perm('AmadoFinance.can_see_wesite_sale'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        return list([])


class PosAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'pos_serial', 'pos_branch', 'pos_bank', 'pos_is_mobil','pos_is_active']
    
    search_fields = ['pos_serial']
    list_filter = ['pos_branch','pos_is_active','pos_is_mobil','pos_bank']

    def save_model(self, request, instance, form, change):
        user = request.user
        if not change:
            
            role = request.user.groups.all()[0].name
            if role != 'admin':
                user = Branch.objects.get(branch_manager__manager_user=user)
                instance.pos_branch = user

        instance = form.save(commit=False)

        instance.save()
        return instance

    def get_queryset(self, request):
        qs = super(PosAdmin, self).get_queryset(request)
        user = request.user
        role = request.user.groups.all()[0].name
        if role == 'manager':
            branch = Branch.objects.filter(branch_manager__manager_user=user).values('id')[0]
            return qs.filter(Q(pos_branch=branch['id'])&Q(pos_is_active=True))
        else:
            return qs

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            return list([])

        if request.user.has_perm('AmadoFinance.can_see_pos_sale'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        return list([])


class PosSaleInline(admin.TabularInline):
    model = PosSale
    extra = 1
    form = CurrencyForm
    autocomplete_fields = ['pos']

    # def get_readonly_fields(self, request, obj=None):

    #     if request.user.is_superuser:
    #         return list([])

    #     if obj == None:
    #         return list([])
    #     else:
    #         if request.user.has_perm('AmadoFinance.can_see_pos_sale'):
    #             result = list(set(
    #                 [field.name for field in self.opts.local_fields] +
    #                 [field.name for field in self.opts.local_many_to_many]
    #             ))
    #             result.remove('id')
    #             return result
    #         return list([])

    #     if request.user.has_perm('AmadoFinance.can_see_pos_sale'):
    #         result = list(set(
    #             [field.name for field in self.opts.local_fields] +
    #             [field.name for field in self.opts.local_many_to_many]
    #         ))
    #         result.remove('id')
    #         return result

    #     return list([])
    
    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser or request.user.username:
            return list([])

        if obj == None:
            return list([])
            
        if request.user.has_perm('AmadoFinance.can_see_pos_sale'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        if obj.sales_status == 'registered' or obj.sales_status == 'tryagain' or obj.sales_status == 'changed':
            return list([])

        # if request.user.has_perm('AmadoFinance.can_see_website_sale'):
        result = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        result.remove('id')
        return result


class InternetInline(admin.TabularInline):
    model = InternetSale
    extra = 1
    form = CurrencyForm
    autocomplete_fields = ['website']
    
    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser or request.user.username:
            return list([])

        if obj == None:
            return list([])
            
        if request.user.has_perm('AmadoFinance.can_see_website_sale'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        if obj.sales_status == 'registered' or obj.sales_status == 'tryagain' or obj.sales_status == 'changed':
            return list([])

        # if request.user.has_perm('AmadoFinance.can_see_website_sale'):
        result = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        result.remove('id')
        return result

    # def get_readonly_fields(self, request, obj=None):

    #     if request.user.is_superuser:
    #         return list([])

    #     if obj == None:
    #         return list([])
    #     else:
    #         if request.user.has_perm('AmadoFinance.can_see_website_sale'):
    #             result = list(set(
    #                 [field.name for field in self.opts.local_fields] +
    #                 [field.name for field in self.opts.local_many_to_many]
    #             ))
    #             result.remove('id')
    #             return result
    #         else:
    #             return list([])

    #     if request.user.has_perm('AmadoFinance.can_see_website_sale'):
    #         result = list(set(
    #             [field.name for field in self.opts.local_fields] +
    #             [field.name for field in self.opts.local_many_to_many]
    #         ))
    #         result.remove('id')
    #         return result

    #     return list([])

class SalesFilter(admin.SimpleListFilter):
    title = ('جمع')
    parameter_name = 'aggregate'

    def lookups(self, request, model_admin):
        return (
            ('days', 'جمع روزانه'),
            ('months', 'جمع ماهانه'),
            ('years', 'جمع سالانه'),
        )

    def queryset(self, request, queryset):
        
        return queryset
        
class MonthFilter(admin.SimpleListFilter):
    title = ('ماه')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        return (
            ('-01-', 'فروردین'),
            ('-02-', 'اردیبهشت'),
            ('-03-', 'خرداد'),
            ('-04-', 'تیر'),
            ('-05-', 'مرداد'),
            ('-06-', 'شهریور'),
            ('-07-', 'مهر'),
            ('-08-', 'آبان'),
            ('-09-', 'آذر'),
            ('-10-', 'دی'),
            ('-11-', 'بهمن'),
            ('-12-', 'اسفند'),
        )

    def queryset(self, request, queryset):
        this_year = jdatetime.date.today().year
        month = self.value()
        if month:
           try:
               return queryset.filter(Q(sales_date__gte=('%i%s01') % (this_year, month)) & Q(
                   sales_date__lte=('%i%s31') % (this_year, month)))
           except:
               try:
                   return queryset.filter(Q(sales_date__gte=('%i%s01') % (this_year, month)) & Q(
                       sales_date__lte=('%i%s30') % (this_year, month)))
               except:
                   return queryset.filter(Q(sales_date__gte=('%i%s01') % (this_year, month)) & Q(
                       sales_date__lte=('%i%s29') % (this_year, month)))
        else:
            r = queryset

        return queryset


class WeekDayFilter(admin.SimpleListFilter):
    title = ('روز هفته')
    parameter_name = 'weekday'

    def lookups(self, request, model_admin):
        return (
            ('0', 'شنبه'),
            ('1', 'یکشنبه'),
            ('2', 'دوشنبه'),
            ('3', 'سه شنبه'),
            ('4', 'چهارشنبه'),
            ('5', 'پنجشنبه'),
            ('6', 'جمعه'),
        )

    def queryset(self, request, queryset):
        weekday = self.value()
        r = queryset

        if weekday:
            for q in queryset:
                if q.sales_date.weekday() != int(weekday):
                    r = r.exclude(id=q.id)
            return r
        else:
            r = queryset

        return queryset
        
class SalesAdmin(admin.ModelAdmin):
    form = CurrencyForm

    list_per_page = 248

    inlines = [PosSaleInline, InternetInline]
    
    change_list_template = 'sales_change_list.html'
    
    ordering = ['-sales_date']

    list_display = ['id','date', 'sales_date', 'sales_branch', 'sales_cash_cost', 'tot_net', 'tot_pos', 'tot',
                    'sales_tot_cash_cost', 'balance',
                    'tot_fish_salon', 'tot_salon', 'tot_fish_del', 'sales_delivery_cost','sales_status']
    list_filter = ('sales_branch',SalesFilter, MonthFilter,WeekDayFilter,('sales_date', JDateFieldListFilter),)

    # change_form_template = 'sales_change_form.html'

    class Media:
        js = (
#        'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
        'salesjs.js',
        'salesexpand.js')
        css = {
            'all': ('salescss.css',)
        }
        
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

        return days[obj.sales_date.weekday()][1]
    date.short_description = 'روز هفته'

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser :
            return list(['balancem', 'totm'])
        if request.user.username=='sadeghi':
            return list(
                ['sales_branch', 'sales_user', 'sales_add_date', 'balancem', 'totm', 'sales_status', 'sales_close_user',
                 'sales_close_date', 'sales_try_user', 'sales_try_date', 'sales_change_user', 'sales_change_date'])

        if obj == None:
            return list(['sales_branch', 'sales_user', 'sales_add_date', 'balancem', 'totm','sales_status','sales_close_user',
                         'sales_close_date','sales_try_user','sales_try_date','sales_change_user','sales_change_date'])

            # result = list(set(
            #     [field.name for field in self.opts.local_fields] +
            #     [field.name for field in self.opts.local_many_to_many]
            # ))
            # result.remove('id')
            # return result
            
        if request.user.has_perm('AmadoFinance.can_see_sales'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        if obj.sales_status == 'registered' or obj.sales_status == 'tryagain' or obj.sales_status == 'changed':
            return list(
                ['sales_branch', 'sales_user', 'sales_add_date', 'balancem', 'totm', 'sales_status', 'sales_close_user',
                 'sales_close_date', 'sales_try_user', 'sales_try_date', 'sales_change_user', 'sales_change_date'])
        # elif obj.sales_status == 'tryagain':
        #
        # elif obj.sales_status == 'changed':

        else:#closed
            result = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

    # def get_readonly_fields(self, request, obj=None):

    #     # for c in CheckPayment.objects.filter(check_cause__cat_name__contains='اجاره'):
    #     #     c.check_payment_type = CheckCategory.objects.get(id=7)
    #     #     c.save()



    #     if request.user.is_superuser:
    #         return list(['balancem', 'totm'])
            
        
            
        
    #     if obj == None:
    #         return list(['sales_branch', 'sales_user', 'sales_add_date', 'balancem', 'totm','sales_status','sales_close_user',
    #                      'sales_close_date','sales_try_user','sales_try_date','sales_change_user','sales_change_date'])
    #     else:
    #         if request.user.has_perm('AmadoFinance.can_see_sales'):
    #             result = list(set(
    #                 [field.name for field in self.opts.local_fields] +
    #                 [field.name for field in self.opts.local_many_to_many]
    #             ))
    #             result.remove('id')
    #             return result
    #         else:
    #             return list(['balancem', 'totm'])
                
    #     if request.user.has_perm('AmadoFinance.can_see_sales'):
    #         result = list(set(
    #             [field.name for field in self.opts.local_fields] +
    #             [field.name for field in self.opts.local_many_to_many]
    #         ))
    #         result.remove('id')
    #         return result

    #     if request.user.has_perm('AmadoFinance.add_sales'):
    #         return ['sales_branch', 'sales_user', 'sales_add_date', 'balancem', 'totm','sales_status','sales_close_user',
    #                      'sales_close_date','sales_try_user','sales_try_date','sales_change_user','sales_change_date']

    #     return list(['sales_status','sales_close_user',
    #                      'sales_close_date','sales_try_user','sales_try_date','sales_change_user','sales_change_date'])

    def tot_fish_del(self, obj):
        return obj.sales_delivery

    tot_fish_del.short_description = 'تعداد کل فیش دلیوری'

    def tot_fish_salon(self, obj):
        return obj.sales_salon

    tot_fish_salon.short_description = 'تعداد کل فیش سالن'

    def tot_salon(self, obj):
        return obj.sales_tot_cash_cost - obj.sales_delivery_cost

    tot_salon.short_description = 'کل فروش سالن(ریال)'

    def tot_pos(self, obj):
        s = PosSale.objects.filter(sale=obj).aggregate(s=Sum('cost'))['s']
        return s

    tot_pos.short_description = 'کل فروش پوز(ریال)'

    def tot_net(self, obj):
        s = InternetSale.objects.filter(sale=obj).aggregate(s=Sum('cost'))['s']
        return s

    tot_net.short_description = 'کل فروش اینترنتی(ریال)'

    def tot(self, obj):

        return obj.sales_cash_cost + self.tot_pos(obj) + self.tot_net(obj)

    tot.short_description = 'جمع کل(ریال)'

    def balance(self, obj):
        return self.tot(obj) - obj.sales_tot_cash_cost

    balance.short_description = 'بالانس(ریال)'

    def get_queryset(self, request):
        qs = super(SalesAdmin, self).get_queryset(request)
        user = request.user
        role = request.user.groups.all()[0].name
        if role == 'manager':
            branch = Branch.objects.filter(branch_manager__manager_user=user).values('id')[0]
            return qs.filter(sales_branch=branch['id'])
        else:
            return qs

    def save_model(self, request, instance, form, change):
        user = request.user
        if not change:
            role = request.user.groups.all()[0].name
            if role != 'admin':
                user = Branch.objects.get(branch_manager__manager_user=user)
                instance.sales_branch = user
                instance.sales_user = request.user

        instance = form.save(commit=False)

        instance.save()

        return instance

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(SalesAdmin, self).response_add(request, obj)

    def after_saving_model_and_related_inlines(self, request, instance):

        days = (
            (0, 'شنبه'),
            (1, 'یکشنبه'),
            (2, 'دوشنبه'),
            (3, 'سه شنبه'),
            (4, 'چهارشنبه'),
            (5, 'پنجشنبه'),
            (6, 'جمعه'),
        )

        name = instance.sales_branch.branch_name.replace(' ', '_')

        message = "فروش شعبه %23"
        message += name
        # print(days[instance.sales_date.weekday()][1])
        message += ' تاریخ %s ' % days[instance.sales_date.weekday()][1]
        message += instance.sales_date.strftime('%Y/%m/%d')

        message += '\n\n'
        message += '1. جمع نقدی: %s ریال' % ("{:,}".format(instance.sales_cash_cost))
        message += '\n\n'
        message += '2. جمع فروش اینترنتی: %s ریال' % ("{:,}".format(self.tot_net(instance)))
        message += '\n\n'
        message += '3. جمع فروش پوز: %s ریال' % ("{:,}".format(self.tot_pos(instance)))

        message += '\n\n'
        message += '<a href="http://amadowh.ir/admin/amadofinance/sales/%i/sales">' % instance.pk
        message += '4. جمع کل: %s ریال' % ("{:,}".format(self.tot(instance)))
        message += '</a>'
        message += '\n\n'
        message += '5. جمع مبلغ فروش: %s ریال' % ("{:,}".format(instance.sales_tot_cash_cost))

        message += '\n\n'
        message += '6. بالانس: %s ریال' % ("{:,}".format(self.balance(instance)))

        message += '\n\n'
        message += '7. تعداد فیش سالن: %s عدد' % self.tot_fish_salon(instance)

        message += '\n\n'
        message += '8. تعداد کنسلی سالن: %s عدد' % instance.sales_salon_cancel

        message += '\n\n'
        message += '9. کل فروش سالن: %s ریال' % ("{:,}".format(self.tot_salon(instance)))

        message += '\n\n'
        message += '10. تعداد فیش دلیوری: %s عدد' % self.tot_fish_del(instance)

        message += '\n\n'
        message += '11. تعداد کنسلی دلیوری: %s عدد' % instance.sales_delivery_cancel

        message += '\n\n'
        message += '12. کل فروش دلیوری: %s ریال' % ("{:,}".format(instance.sales_delivery_cost))

        message += '\n\n'

        # nanba bot
        resp = requests.post(
            "https://api.telegram.org/bot619516108:AAGuhpPV_n-Lm6deISAJ3JsBr-fHuGgxUU8/sendmessage?parse_mode=html&chat_id=-1001355972297&text=" + message,
            headers={
                "Accept": "application/json"
            })
        return instance
        
    def close(self, request, qs):
        if not request.user.has_perm('AmadoFinance.can_close_sales'):
            messages.error(request, "شما اجازه بستن ندارید")
            return
        flag = False
        for q in qs:
            if q.sales_status == 'tryagain':
                flag = True
        if not flag:
            for q in qs:
                q.sales_status = 'closed'
                q.sales_close_user = request.user
                q.sales_close_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i فروش بسته شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان بستن برخی یا همه فروش ها وجود ندارد")
            
    close.short_description = 'بستن فروش های انتخاب شده'
    
    
    def tryagain(self, request, qs):
        if not request.user.has_perm('AmadoFinance.can_close_sales'):
            messages.error(request, "شما اجازه رد ندارید")
            return
        flag = False
        for q in qs:
            if q.sales_status == 'closed':
                flag = True
        if not flag:
            for q in qs:
                q.sales_status = 'tryagain'
                q.sales_try_user = request.user
                q.sales_try_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i فروش برای بررسی رد شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان رد برخی یا همه فروش ها وجود ندارد")
            
    tryagain.short_description = 'رد فروش های انتخاب شده برای بررسی'
    
    actions = [close,tryagain]


class BankAdmin(admin.ModelAdmin):
    search_fields = ['bank_name']

    def get_model_perms(self, request):
        if request.user.is_superuser:
            perms = admin.ModelAdmin.get_model_perms(self, request)
            return perms
        return {}


class PaymentCategoryAdmin(admin.ModelAdmin):
    search_fields = ['cat_name']

    def get_model_perms(self, request):
        if request.user.is_superuser:
            perms = admin.ModelAdmin.get_model_perms(self, request)
            return perms
        return {}


class RecipientCompanyAdmin(admin.ModelAdmin):
    search_fields = ['recipient_name']

    def get_model_perms(self, request):
        if request.user.is_superuser:
            perms = admin.ModelAdmin.get_model_perms(self, request)
            return perms
        return {}


class CheckCatAdmin(admin.ModelAdmin):
    search_fields = ['cat_name']

    def get_model_perms(self, request):
        if request.user.is_superuser:
            perms = admin.ModelAdmin.get_model_perms(self, request)
            return perms
        return {}


class CurrencyFormCash(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CurrencyFormCash, self).__init__(*args, **kwargs)

    class Meta:
        exclude = ()
        model = CashPayment
        widgets = {
            'payment_cost': forms.NumberInput(attrs={'step': 0, 'min': 0, 'size': '100', 'localization': True}),
            'cost': forms.NumberInput(attrs={'step': 0, 'min': 0, 'size': '100', 'localization': True}),
            'check_title': forms.TextInput(attrs={'direction': 'rtl', 'size': 50}),
            'check_number': forms.TextInput(attrs={'direction': 'rtl', 'size': 50}),
            'check_description': forms.Textarea(attrs={'direction': 'rtl', 'rows': 5}),

            'payment_title': forms.TextInput(attrs={'direction': 'rtl', 'size': 50}),
            'payment_account': forms.TextInput(attrs={'direction': 'rtl', 'size': 50}),
            'payment_account_person': forms.TextInput(attrs={'direction': 'rtl', 'size': 50}),
            'payment_description': forms.Textarea(attrs={'direction': 'rtl', 'rows': 5}),
            # 'payment_due_date': forms.TextInput(attrs={'readonly': True}),

        }


class FactorImageInline(admin.TabularInline):
    model = FactorImage
    form = CurrencyFormCash
    extra = 1

    fields = ('image_title', 'cost', 'image', 'factor_image')
    readonly_fields = ('factor_image',)

    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return list([])
    #     if obj != None:
    #         if obj.payment_status == 'paid':
    #             result = list(set(
    #                     [field.name for field in self.opts.local_fields] +
    #                     [field.name for field in self.opts.local_many_to_many]
    #                 ))
    #             result.remove('id')
    #             return result
    #     return list([])


class RecedeImageInline(admin.TabularInline):
    model = RecedeImage
    extra = 1
    form = CurrencyFormCash
    fields = ('image_title', 'cost','payment_due_date','def_account', 'image', 'factor_image')
    readonly_fields = ('factor_image',)


class CashFilter(admin.SimpleListFilter):
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
            ('notpaid', 'پرداخت نشده'),
            ('registered', 'ثبت شده/در انتظار تایید'),
            ('confirmed', 'تایید شده/در انتظار پرداخت'),
            ('rejected', 'رد شده'),
            ('paid', 'پرداخت شده'),


        )

    def queryset(self, request, queryset):
        if self.value() == None:
            r = queryset.exclude(Q(payment_status='paid')|Q(payment_status='rejected')).order_by('payment_due_date')

        elif self.value() == 'notpaid':
            r = queryset.exclude(payment_status='paid').order_by('payment_due_date')
        elif self.value() == 'paid':
            r = queryset.filter(payment_status='paid').order_by('payment_due_date')
        elif self.value() == 'registered':
            r = queryset.filter(payment_status='registered').order_by('payment_due_date')
        elif self.value() == 'confirmed':
            r = queryset.filter(payment_status='confirmed').order_by('payment_due_date')
        elif self.value() == 'rejected':
            r = queryset.filter(payment_status='rejected').order_by('payment_due_date')
        else:
            r = queryset

        return r


class CashRelationInline(admin.TabularInline):
    model = RelationShip
    extra = 1
    autocomplete_fields = ['checkp','fund','purchase']
    
class CashDateFilter(admin.SimpleListFilter):
    title = ('تاریخ')
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return (
            ('today', 'امروز'),
            ('untiltoday', 'تا امروز'),
            ('aftertoday', 'از امروز به بعد'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            r = queryset.filter(payment_due_date = jdatetime.datetime.today().strftime('%Y-%m-%d')).order_by('payment_due_date')
        elif self.value() == 'untiltoday':
            r = queryset.filter(payment_due_date__lte = jdatetime.datetime.today().strftime('%Y-%m-%d')).order_by('payment_due_date')
        elif self.value() == 'aftertoday':
            r = queryset.filter(payment_due_date__gte = jdatetime.datetime.today().strftime('%Y-%m-%d')).order_by('payment_due_date')
        else:
            r = queryset

        return r
    
class CashPaymentAdmin(admin.ModelAdmin):
    list_per_page = 500
    form = CurrencyFormCash
    # list_display = ['see', 'getid', 'date','regdate', 'payment_cost','remainder', 'gettitle', 'payment_account', 'bank', 'payment_recipient',
                    # 'payment_account_person', 'status', 'payment_add_user']
    list_display = ['see', 'getid', 'date', 'payment_cost','remainder', 'gettitle', 'payment_account',
                    'payment_account_person', 'status', 'getadduser']
                    
    def getadduser(self, obj):
        return obj.payment_add_user    
    getadduser.short_description = 'ثبت کننده'
    getadduser.admin_order_field = 'payment_add_user'
    
    def get_changelist(self, request):
        class MyChangeList(ChangeList):
            def remainder(self,obj):
                sum = RecedeImage.objects.filter(factor=obj).aggregate(sum=Sum('cost'))['sum']
                if sum:
                    return obj.payment_cost-sum
                if obj.payment_status != 'paid':
                    return obj.payment_cost
                return 0
            def get_results(self, *args, **kwargs):
                super(MyChangeList, self).get_results(*args, **kwargs)
                # rs = self.result_list.aggregate(tomato_sum=Sum('get_price'))
                sum = 0
                for r in self.result_list:
                    sum += self.remainder(r)
                self.tomato_count = int(sum)

        return MyChangeList          
                    
    def remainder(self,obj):
        sum = RecedeImage.objects.filter(factor=obj).aggregate(sum=Sum('cost'))['sum']
        if sum:
            return obj.payment_cost-sum
        if obj.payment_status != 'paid':
            return obj.payment_cost
        return 0

    remainder.short_description = 'مانده قابل پرداخت(ریال)'
                    
    def regdate(self, obj):

        days = (
            (0, 'شنبه'),
            (1, 'یکشنبه'),
            (2, 'دوشنبه'),
            (3, 'سه شنبه'),
            (4, 'چهارشنبه'),
            (5, 'پنجشنبه'),
            (6, 'جمعه'),
        )

        # l = '%s <br> %s' % (obj.payment_add_date.strftime('%Y-%m-%d %H:%M'),days[obj.payment_add_date.weekday()][1])
        l = obj.payment_add_date.strftime('%Y-%m-%d %H:%M')
        # return mark_safe('<span style="width:50px;direction:rtl" >%s</span>'%l)
        return mark_safe(l)

    regdate.short_description = 'تاریخ ثبت'
    regdate.admin_order_field = 'payment_add_date'
                    
    search_fields = ['payment_cause__cat_name','payment_recipient__recipient_name','payment_title','id']
    
    fields = ['payment_title','payment_due_date','payment_cost','payment_cause','payment_recipient','payment_account','payment_account_type',
              'payment_account_person','payment_account_bank','supplier','cost_center','over_account','accounts','payment_description','payment_add_user','payment_add_date',
              'payment_confirm_user','payment_confirm_date','payment_pay_user','payment_pay_date',
              'payment_change_user','payment_change_date','payment_status']

    ordering = ['payment_due_date']
    
    # fields = ['title', 'parent']

    # class Media:
    #     js = (
    #         # 'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js','payment.js')
    #         'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
    #         '../../AmadoFinance/static/myscript.js',)

    change_list_template = 'my_change_list.html'
    
    class Media:
        js = (
            # 'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js','payment.js')
#            'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
            'myscript.js',
        )
        css = {
            'all': ('salescss.css',)
        }

    # def get_urls(self):
    #     urls = super(CashPaymentAdmin, self).get_urls()
    #     # my_urls = path('',(r'^cashpayment/$', 'status=notpaid'))
    #     return my_urls + urls

    def getid(self, obj):
        return obj.pk

    getid.short_description = 'شناسه'
    getid.admin_order_field = 'id'

    def gettitle(self, obj):
        title = ''
        if obj.payment_title:
            title = '%s - %s' % (obj.payment_cause, obj.payment_title)
        else:
            title = '%s' % obj.payment_cause

        return title

    gettitle.short_description = 'بابت'

    def see(self, obj):
        return mark_safe('<a href="./%i/change">مشاهده </a>' % obj.id)

    see.short_description = 'لینک'

    inlines = [FactorImageInline, RecedeImageInline, CashRelationInline]
#    inlines = [ RecedeImageInline, CashRelationInline]

    autocomplete_fields = ['payment_account_bank', 'payment_cause', 'payment_recipient','check_title','supplier']

    list_filter = [CashFilter,CashDateFilter,'supplier', 'payment_account_bank','cost_center','over_account', ('payment_due_date', JDateFieldListFilter)]

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

        l = '%s - %s' % (obj.payment_due_date, days[obj.payment_due_date.weekday()][1])
        if obj.payment_status == 'paid' or obj.payment_status == 3:
            return l
        t = jdatetime.datetime.today().strftime('%Y-%m-%d')
        if obj.payment_due_date.strftime('%Y-%m-%d') < t:
            link = '<span style="padding:0 5px;border-radius:5px;background: #f25252;" >%s</span>' % l
        elif obj.payment_due_date.strftime('%Y-%m-%d') == t:
            link = '<span style="padding:0 5px;border-radius:5px;background: #f9e36b;" >%s</span>' % l
        else:
            link = '<span style="padding:0 5px;border-radius:5px;background: #98f970;" >%s</span>' % l

        return mark_safe(link)

    date.short_description = 'تاریخ پرداخت'
    date.admin_order_field = 'payment_due_date'

    def bank(self, obj):
        if obj.payment_account_bank:
            return mark_safe('<span style="align=center;">%s</span>' % (obj.payment_account_bank))
        else:
            return 'پوز'

    bank.short_description = 'بانک'

    def status(self, obj):

        if obj.payment_status == 'registered':
            # link = '<span style="padding:5px;border-radius:5px;background: #fcf8e3;" >ثبت شده/در انتظار تایید</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #fcf8e3;" ><i class="fas fa-clock"></i></span>'
        elif obj.payment_status == 'confirmed':
            # link = '<span style="padding:5px;border-radius:5px;background: #d9edf7;" >تایید شده/در انتظار پرداخت</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #d9edf7;" ><i class="fas fa-check-circle"></i></span>'
        elif obj.payment_status == 'rejected':
            # link = '<span style="padding:5px;border-radius:5px;background: #f2dede;" >رد شده</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #f2dede;" ><i class="fas fa-times-circle"></i></span>'
        else:
            # link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" >پرداخت شده</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" ><i class="fas fa-check-double"></i></span>'

        return mark_safe(link)

    status.short_description = "وضعیت"

    # status.order_field = ['payment_status']

    def card(self, obj):
        if obj.payment_account_type == 'card':
            return 'کارت %s' % obj.payment_account
        elif obj.payment_account_type == 'account':
            return 'حساب %s' % obj.payment_account
        elif obj.payment_account_type == 'shaba':
            return 'شبا %s' % obj.payment_account
        else:
            return ''

    card.short_description = "شماره"

    # def confirm_but(self,obj):
    #     return 'hi'

    def confirm(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_confirm_cash'):
            messages.error(request, "شما اجازه تایید ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status == 'paid':
                flag = True
            if FactorImage.objects.filter(factor=q).count() == 0:
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'confirmed'
                q.payment_confirm_user = request.user
                q.payment_confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i پرداخت تایید شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان تایید برخی یا همه پرداخت ها وجود ندارد")

    confirm.short_description = 'تایید پرداخت های انتخاب شده'

    def decline(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_decline_cash'):
            messages.error(request, "شما اجازه رد ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status == 'paid':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'rejected'
                q.payment_confirm_user = request.user
                q.payment_confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i پرداخت رد شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان رد برخی یا همه پرداخت ها وجود ندارد")

    decline.short_description = 'رد پرداخت های انتخاب شده'

    def pay(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_pay_cash'):
            messages.error(request, "شما اجازه انجام پرداخت را ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status != 'confirmed':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'paid'
                q.payment_pay_user = request.user
                q.payment_pay_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i پرداخت پرداخت شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان انجام برخی یا همه پرداخت ها وجود ندارد")

    pay.short_description = 'انجام پرداخت های انتخاب شده'

    def export_xls(modeladmin, request, queryset):
        import xlwt
        from django.http import HttpResponse, JsonResponse

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=cash_%s.xls' % jdatetime.datetime.today().strftime(
            '%Y-%m-%d')
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("واریزی")

        row_num = 0

        columns = [
            (u"تاریخ پرداخت", 3500),
            (u"گیرنده", 6000),
            (u"نماینده", 3500),
            (u"بابت", 10000),
            (u"شماره حساب/کارت", 8000),
            (u"مبلغ پرداختی(ریال)", 4000),
            (u"وضعیت", 6500),
            (u"لینک", 3500),
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300

        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        ws.write_merge(0, 0, 0, 6, 'تاریخ روز: %s' % jdatetime.datetime.today().strftime('%Y/%m/%d'), font_style)

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        row_num += 1

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 2
        font_style.num_format_str = '#,##0'
        font_style.font.height = 250

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        for obj in queryset:
            row_num += 1
            status = ''
            if obj.payment_status == 'registered':
                status = 'ثبت شده/در انتظار تایید'
            elif obj.payment_status == 'confirmed':
                status = 'تایید شده/در انتظار پرداخت'
            elif obj.payment_status == 'rejected':
                status = 'رد شده'
            else:
                status = 'پرداخت شده/در انتظار تسویه'

            title = ''
            if obj.payment_title:
                title = '%s - %s' % (obj.payment_cause, obj.payment_title)
            else:
                title = '%s' % obj.payment_cause

            row = [
                obj.payment_due_date.strftime('%Y/%m/%d'),
                obj.payment_recipient.recipient_name,
                obj.payment_account_person,
                title,
                obj.payment_account,
                obj.payment_cost,
                status,
                'http://amadowh.ir/amadofinance/cashpayment/%i/change' % obj.pk,
            ]
            ws.write(row_num, 0, row[0], font_style)
            ws.write(row_num, 1, row[1], font_style)
            ws.write(row_num, 2, row[2], font_style)
            ws.write(row_num, 3, row[3], font_style)
            ws.write(row_num, 4, row[4], font_style)
            ws.write(row_num, 5, row[5], font_style)
            ws.write(row_num, 6, row[6], font_style)
            ws.write(row_num, 7, xlwt.Formula('HYPERLINK("%s","مشاهده")' % (row[6])), font_style)

        wb.save(response)
        return response

    export_xls.short_description = u"خروجی اکسل"
    
    def duplicate_records(modeladmin, request, queryset):
        if queryset.count() == 1:
            object_ids = []
            for object in queryset:
                object.id = None
                object.save()
                object_ids.append(object.id)

            if len(object_ids) == 1:
                return redirect('./%i/change'%object_ids[0])
        elif queryset.count()>1:
            messages.error(request, "امکان کپی بیش از یک پرداخت وجود ندارد")
        


    duplicate_records.short_description = 'کپی پرداخت انتخاب شده'

    actions = [confirm, decline, pay, export_xls,duplicate_records]

    def get_readonly_fields(self, request, obj=None):
        
        if request.user.is_superuser:
            return list(['accounts'])

        if request.user.has_perm('AmadoFinance.can_always_edit_cash'):
            return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                    'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                    'payment_change_date','accounts' ]

        if not request.user.is_superuser:

            if obj == None:
                if request.user.has_perm('AmadoFinance.can_change_status_cash'):
                    return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                            'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                            'payment_change_date','accounts' ]
                return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date','accounts' ]

            elif obj.payment_status == 'confirmed' or obj.payment_status == 'paid':

                result = list(set(
                    [field.name for field in self.opts.local_fields] +
                    [field.name for field in self.opts.local_many_to_many]+['accounts']
                ))
                if request.user.has_perm('AmadoFinance.can_change_status_cash'):
                    result.remove('payment_status')
                result.remove('id')
                result.remove('supplier')
                return result
            else:
                if request.user.has_perm('AmadoFinance.can_see_cash'):
                    result = list(set(
                        [field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]+['accounts']
                    ))
                    if request.user.has_perm('AmadoFinance.can_change_status_cash'):
                        result.remove('payment_status')
                    result.remove('id')
                    result.remove('supplier')
                    return result
                if request.user.has_perm('AmadoFinance.can_change_status_cash'):
                    return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                            'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                            'payment_change_date','accounts' ]
                return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date','accounts']
        return list(['accounts'])

    def save_model(self, request, instance, form, change):

        user = request.user
        role = request.user.groups.all()[0].name
        if not change:

            if not request.user.is_superuser:
                instance.payment_add_user = request.user
                instance.payment_add_date = jdatetime.datetime.now()
        else:
            if not request.user.is_superuser:
                instance.payment_change_user = request.user
                instance.payment_change_date = jdatetime.datetime.now()

        instance = form.save(commit=False)

        instance.save()
        form.save_m2m()
        return instance

    def get_queryset(self, request):
        qs = super(CashPaymentAdmin, self).get_queryset(request)
        if request.user.username == 'sadeghi':
            return qs.filter(payment_add_date__gte='1397-04-09 00:00:00')
        return qs

        # def has_delete_permission(self, request, obj=None):
        #     if obj != None:
        #         user = request.user
        #         role = request.user.groups.all()[0].name
        #         if role == 'admin':
        #             return True
        #
        #         if (role == 'amado' and obj.payment_status != 'registered') or (role == 'amadoup' and obj.payment_status != 'registered'):
        #             messages.error(request, "امکان حذف این پرداخت وجود ندارد")
        #             return False
        #         else:
        #             return True
        #     else:
        #         return True
        #
        # def _cashpayment_delete(self, request, instance, **kwargs):
        #     if instance.payment_status != 'registered':
        #         messages.error(request, "امکان حذف این پرداخت وجود ندارد")
        #     else:
        #         instance.delete()
        #         self.message_user(request, "پرداخت حذف شد")


class CheckFilter(admin.SimpleListFilter):
    title = ('وضعیت')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('all','همه'),
            ('notpaid', 'پرداخت نشده'),
            ('registered', 'ثبت شده/در انتظار تایید'),
            ('confirmed', 'تایید شده/در انتظار پرداخت'),
            ('rejected', 'رد شده'),
            ('paid', 'پرداخت شده'),
            ('back', 'برگشت خورده'),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == None:
            r = queryset.exclude(Q(payment_status='rejected')|Q(payment_status='paid')|Q(payment_status='back')).order_by('check_due_date')
        elif self.value() == 'notpaid':
            r = queryset.exclude(Q(payment_status='rejected')|Q(payment_status='paid')|Q(payment_status='back')).order_by('check_due_date')
        elif self.value() == 'registered':
            r = queryset.filter(payment_status='registered').order_by('check_due_date')
        elif self.value() == 'confirmed':
            r = queryset.filter(payment_status='confirmed').order_by('check_due_date')
        elif self.value() == 'rejected':
            r = queryset.filter(payment_status='rejected').order_by('check_due_date')
        elif self.value() == 'paid':
            r = queryset.filter(payment_status='paid').order_by('check_due_date')
        elif self.value() == 'back':
            r = queryset.filter(payment_status='back').order_by('check_due_date')
        else:
            r = queryset


        return r

class CheckRelationInline(admin.TabularInline):
    model = RelationShip
    extra = 1
    autocomplete_fields = ['cash','fund','purchase']
    
class CheckPaymentAdmin(admin.ModelAdmin):
    form = CurrencyFormCash
    list_display = ['see', 'getid', 'date', 'type', 'payment_cost', 'gettitle', 'getrecip', 'getcheck_payment_type',
                    'status','getadduser']
                    
    def get_changelist(self, request):
        class MyChangeList(ChangeList):
            def get_results(self, *args, **kwargs):
                super(MyChangeList, self).get_results(*args, **kwargs)
                # rs = self.result_list.aggregate(tomato_sum=Sum('get_price'))
                sum = 0
                for r in self.result_list:
                    sum += r.payment_cost
                self.tomato_count = int(sum)

        return MyChangeList                
                    
    def getrecip(self, obj):
        return obj.check_recipient    
    getrecip.short_description = 'گیرنده'
    getrecip.admin_order_field = 'check_recipient'
    
    def getadduser(self, obj):
        return obj.payment_add_user    
    getadduser.short_description = 'ثبت کننده'
    getadduser.admin_order_field = 'payment_add_user'
    
    def getcheck_payment_type(self, obj):
        return obj.check_payment_type    
    getcheck_payment_type.short_description = 'نوع چک'
    getcheck_payment_type.admin_order_field = 'check_payment_type'
    
                    
    fields = ['check_title','check_number','check_date','check_due_date','payment_cost', 'check_cause', 'check_payment_type', 'check_bank','check_recipient', 'check_again_date',
              'supplier','cost_center','over_account', 'check_description',
              'payment_add_user','payment_add_date','payment_confirm_user','payment_confirm_date','payment_pay_user','payment_pay_date','payment_change_user',
              'payment_change_date','payment_status',
              ]
                    
    inlines = [FactorImageInline,RecedeImageInline,CheckRelationInline]

    ordering = ['check_due_date']

    change_list_template = 'check_change_list.html'

    search_fields = ['id','check_number','check_cause__cat_name','check_recipient__recipient_name']

    def getid(self, obj):
        return obj.pk

    getid.short_description = 'شناسه'
    getid.admin_order_field = 'id'

    def gettitle(self, obj):
        title = ''
        if obj.check_title:
            title = '%s - %s' % (obj.check_cause, obj.check_title)
        else:
            title = '%s' % obj.check_cause

        return title

    gettitle.short_description = 'بابت'

    def get_queryset(self, request):
        qs = super(CheckPaymentAdmin, self).get_queryset(request)
        if request.user.username == 'sadeghi':
            qs = qs.filter(payment_add_date__gte='1397-04-09 00:00:00')
            return qs.exclude(check_payment_type__id__in=[1,9])
        elif request.user.username == 'rahbar' or request.user.username == 'bmanshad' or request.user.username == 'jafari' or request.user.username == 'jafari2':
            return qs.exclude(check_payment_type__id__in=[1,9])

        return qs

    def see(self, obj):
        return mark_safe('<a href="./%i/change">مشاهده</a>' % obj.id)

    see.short_description = 'لینک'

    # inlines = [FactorImageInline, RecedeImageInline]

    autocomplete_fields = ['check_bank', 'check_cause', 'check_recipient', 'check_payment_type','supplier']

    # list_filter = ['payment_status',('payment_due_date',JDateFieldListFilter)]
    list_filter = [CheckFilter,'check_bank','supplier', 'check_payment_type','cost_center','over_account', ('check_due_date', JDateFieldListFilter),'payment_add_user']

    # list_filter = [CheckFilter,'payment_status',('check_due_date',JDateFieldListFilter)]

    def type(self, obj):
        if obj.check_bank:
            return mark_safe(
                '<span style="align=center;">چک به شماره %s - %s</span>' % (obj.check_number, obj.check_bank))
        else:
            return 'نقدی'

    type.short_description = 'نوع تعهد'

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

        l = '%s - %s' % (obj.check_due_date, days[obj.check_due_date.weekday()][1])
        if obj.payment_status == 'paid' or obj.payment_status == 3:
            return l
        t = jdatetime.datetime.today().strftime('%Y-%m-%d')
        if obj.check_due_date.strftime('%Y-%m-%d') < t:
            link = '<span style="padding:0 5px;border-radius:5px;background: #f25252;" >%s</span>' % l
        elif obj.check_due_date.strftime('%Y-%m-%d') == t:
            link = '<span style="padding:0 5px;border-radius:5px;background: #f9e36b;" >%s</span>' % l
        else:
            link = '<span style="padding:0 5px;border-radius:5px;background: #98f970;" >%s</span>' % l

        return mark_safe(link)

    date.short_description = 'تاریخ سررسید'
    date.admin_order_field = 'check_due_date'

    def status(self, obj):
        if obj.payment_status == 'registered':
            # link = '<span style="padding:5px;border-radius:5px;background: #fcf8e3;" >ثبت شده/در انتظار تایید</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #fcf8e3;" ><i class="fas fa-clock"></span>'
        elif obj.payment_status == 'confirmed':
            # link = '<span style="padding:5px;border-radius:5px;background: #d9edf7;" >تایید شده/در انتظار پرداخت</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #d9edf7;" ><i class="fas fa-check-circle"></i></span>'
        elif obj.payment_status == 'rejected':
            # link = '<span style="padding:5px;border-radius:5px;background: #f2dede;" >رد شده</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #f2dede;" ><i class="fas fa-times-circle"></i></span>'
        elif obj.payment_status == 'paid':
            # link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" >پرداخت شده</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" ><i class="fas fa-check-double"></i></span>'
        else:
            # link = '<span style="padding:5px;border-radius:5px;background: #f46242;" >برگشت خورده</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #f46242;" ><i class="fas fa-sync"></i></span>'

        return mark_safe(link)

    status.short_description = "وضعیت"

    
    def decline(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_decline_check'):
            messages.error(request, "شما اجازه رد ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status == 'paid':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'rejected'
                q.payment_confirm_user = request.user
                q.payment_confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i چک رد شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان رد برخی یا همه چک ها وجود ندارد")

    decline.short_description = 'رد چک های انتخاب شده'

    def pay(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_pay_check'):
            messages.error(request, "شما اجازه پرداخت چک را ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status == 'declined':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'paid'
                q.payment_pay_user = request.user
                q.payment_pay_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i چک پرداخت شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان پرداخت برخی یا همه چک ها وجود ندارد")

    pay.short_description = 'پرداخت چک های انتخاب شده'

    def back(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_back_check'):
            messages.error(request, "شما اجازه برگشت زدن این چک را ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status != 'paid':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'back'
                q.payment_pay_user = request.user
                q.payment_pay_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i چک برگشت داده شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان برگشت زدن برخی یا همه چک ها وجود ندارد")

    back.short_description = 'برگشت دادن چک'

    def export_xls(modeladmin, request, queryset):
        queryset = queryset.filter().order_by('check_due_date')
        import xlwt
        from django.http import HttpResponse, JsonResponse

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=check_%s.xls' % jdatetime.datetime.today().strftime(
            '%Y-%m-%d')
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("چک")
        ws.cols_right_to_left = 1

        row_num = 0

        columns = [
            (u"ایام هفته", 5000),
            (u"تاریخ سررسید", 5000),
            (u"نام شعبه", 3500),
            (u"شماره چک", 5000),
            (u"نام دریافت کننده", 5000),
            (u"بابت", 8000),
            (u"نوع هزینه", 6000),
            (u"مبلغ (ریال)", 4000),
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300
        ws.row(1).height_mismatch = True
        ws.row(1).height = 900

        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x00
        borders.right_colour = 0x00
        borders.top_colour = 0x00
        borders.bottom_colour = 0x00
        font_style.borders = borders

        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        ws.write_merge(0, 0, 0, 7, 'تاریخ روز: %s' % jdatetime.datetime.today().strftime('%Y/%m/%d'), font_style)

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        font_style.pattern = pattern
        font_style.borders = borders

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        row_num += 1

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 2
        font_style.num_format_str = '#,##0'
        font_style.font.height = 250
        font_style.borders = borders

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        for obj in queryset:
            row_num += 1


            bank = ''
            number = ''
            if obj.check_bank:
                bank = obj.check_bank.bank_name
                number = obj.check_number

            days = (
                (0, 'شنبه'),
                (1, 'یکشنبه'),
                (2, 'دوشنبه'),
                (3, 'سه شنبه'),
                (4, 'چهارشنبه'),
                (5, 'پنجشنبه'),
                (6, 'جمعه'),
            )

            title = ''
            if obj.check_title:
                title = '%s - %s' % (obj.check_cause, obj.check_title)
            else:
                title = '%s' % obj.check_cause

            row = [
                days[obj.check_due_date.weekday()][1],
                obj.check_due_date.strftime('%Y/%m/%d'),
                bank,
                number,
                obj.check_recipient.recipient_name,
                title,
                obj.check_payment_type.cat_name,
                obj.payment_cost,
            ]
            ws.write(row_num, 0, row[0], font_style)
            ws.write(row_num, 1, row[1], font_style)
            ws.write(row_num, 2, row[2], font_style)
            ws.write(row_num, 3, row[3], font_style)
            ws.write(row_num, 4, row[4], font_style)
            ws.write(row_num, 5, row[5], font_style)
            ws.write(row_num, 6, row[6], font_style)
            ws.write(row_num, 7, row[7], font_style)


        wb.save(response)
        return response

    export_xls.short_description = u"خروجی اکسل"
    
    def duplicate_records(modeladmin, request, queryset):
        if queryset.count() == 1:
            object_ids = []
            for object in queryset:
                object.id = None
                object.save()
                object_ids.append(object.id)

            if len(object_ids) == 1:
                return redirect('./%i/change'%object_ids[0])
        elif queryset.count()>1:
            messages.error(request, 'امکان کپی بیش از یک چک وجود ندارد')



    duplicate_records.short_description = 'کپی چک های انتخاب شده'
    
    def create_cash(self, request, queryset):
        count = queryset.count()
        if count > 1:
            messages.error(request, 'امکان کپی بیش از یک چک وجود ندارد')
            return
        obj = queryset[0]
        if obj.supplier:
            account = ''
            type = ''
            supplier = obj.supplier
            if obj.supplier.supplier_account.last().card:
                account = obj.supplier.supplier_account.last().card
                type = 'card'
            elif obj.supplier.supplier_account[0].account:
                account = obj.supplier.supplier_account.last().account
                type = 'account'
            else:
                account = obj.supplier.supplier_account.last().shaba
                type = 'shaba'


            cash = CashPayment(payment_due_date=obj.check_due_date,payment_cost=obj.payment_cost,payment_recipient=obj.check_recipient,
                               payment_cause = obj.check_cause,
                               payment_account=account,supplier=supplier,payment_account_type=type,
                               payment_account_person=obj.supplier.supplier_account.last().person,
                               payment_account_bank = obj.supplier.supplier_account.last().bank,
                               payment_add_user = request.user,
                               payment_add_date = jdatetime.datetime.now())
            cash.save()
            return redirect('../cashpayment/%i/change' % cash.id)
        else:
            messages.error(request, 'چک انتخاب شده تامین کننده ندارد')

    create_cash.short_description = 'ایجاد پرداخت نقدی از روی چک'
    
    def export_xls_pro(modeladmin, request, queryset):
        queryset = queryset.filter().order_by('check_due_date')
        import xlwt
        from django.http import HttpResponse, JsonResponse

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=check_pro_%s.xls' % jdatetime.datetime.today().strftime(
            '%Y-%m-%d')
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("چک")
        ws.cols_right_to_left = 1

        row_num = 0

        columns = [
            (u"ایام هفته", 5000),
            (u"تاریخ سررسید", 5000),
            (u"نام شعبه", 3500),
            (u"شماره چک", 5000),
            (u"نام دریافت کننده", 5000),
            (u"بابت", 8000),
            (u"نوع هزینه", 6000),
            (u"نقدی (ریال)", 4000),
            (u"چک (ریال)", 4000),
            (u"تخمین فروش (ریال)", 6000),
            (u"فروش واقعی (ریال)", 6000),
            (u"انحراف از برآورد فروش (ریال)", 8000),
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300
        ws.row(1).height_mismatch = True
        ws.row(1).height = 900

        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x00
        borders.right_colour = 0x00
        borders.top_colour = 0x00
        borders.bottom_colour = 0x00
        font_style.borders = borders

        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        ws.write_merge(0, 0, 0, 11, 'تاریخ روز: %s' % jdatetime.datetime.today().strftime('%Y/%m/%d'), font_style)

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        font_style.pattern = pattern
        font_style.borders = borders

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        row_num += 1

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 2
        font_style.num_format_str = '#,##0'
        font_style.font.height = 250
        font_style.borders = borders

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al



        font_style_red = xlwt.XFStyle()
        font_style_red.alignment.wrap = 2
        font_style_red.num_format_str = '#,##0'
        font_style_red.font.height = 250
        font_style_red.borders = borders
        font_style_red.alignment = al
        font_style_red.font.colour_index = xlwt.Style.colour_map['red']


        days = (
            (0, 'شنبه'),
            (1, 'یکشنبه'),
            (2, 'دوشنبه'),
            (3, 'سه شنبه'),
            (4, 'چهارشنبه'),
            (5, 'پنجشنبه'),
            (6, 'جمعه'),
        )

        estimation = (
            (0, 160000000),
            (1, 160000000),
            (2, 160000000),
            (3, 160000000),
            (4, 180000000),
            (5, 250000000),
            (6, 250000000),
        )

        today = jdatetime.date.today()


        first_date = queryset[0].check_due_date
        last_date = queryset.reverse()[0].check_due_date
        cur_date = first_date
        prev_date = cur_date + +jdatetime.timedelta(days=-1)


        for obj in queryset:
            cur_date = obj.check_due_date


            try:
                check_sale = CheckPayment.objects.filter(check_due_date=cur_date).values('check_due_date').annotate(sum=Sum('payment_cost'))[0]['sum']
            except:
                check_sale = None

            print(check_sale)

            style = font_style

            if (cur_date-prev_date).days > 1:#no checks

                for i in range(1,(cur_date-prev_date).days):
                    row_num += 1

                    try:
                        real_sale = Sales.objects.filter(sales_date=first_date).values('sales_date').annotate(sum=Sum('sales_tot_cash_cost'))[0]['sum']
                    except:
                        real_sale = None


                    style = font_style
                    if (today-cur_date).days > 0 and check_sale and estimation[first_date.weekday()][1] < check_sale:
                        style = font_style_red

                    ws.write(row_num, 0, days[first_date.weekday()][1], style)
                    ws.write(row_num, 1, first_date.strftime('%Y/%m/%d'), style)

                    ws.write(row_num, 2, None, style)
                    ws.write(row_num, 3, None, style)
                    ws.write(row_num, 4, None, style)
                    ws.write(row_num, 5, None, style)
                    ws.write(row_num, 6, None, style)
                    ws.write(row_num, 7, None, style)
                    ws.write(row_num, 8, None, style)


                    ws.write(row_num, 9, estimation[first_date.weekday()][1], style)
                    ws.write(row_num, 10, real_sale, style)
                    ws.write(row_num, 11, xlwt.Formula('K%i-J%i'%(row_num+1,row_num+1)), style)
                    first_date = first_date + jdatetime.timedelta(days=1)  # real days

            row_num += 1
            try:
                real_sale = Sales.objects.filter(sales_date=first_date).values('sales_date').annotate(sum=Sum('sales_tot_cash_cost'))[0]['sum']
            except:
                real_sale = None


            bank = ''
            number = ''
            if obj.check_bank:
                bank = obj.check_bank.bank_name
                number = obj.check_number


            title = ''
            if obj.check_title:
                title = '%s - %s' % (obj.check_cause, obj.check_title)
            else:
                title = '%s' % obj.check_cause



            row = [
                days[obj.check_due_date.weekday()][1],
                obj.check_due_date.strftime('%Y/%m/%d'),
                bank,
                number,
                obj.check_recipient.recipient_name,
                title,
                obj.check_payment_type.cat_name,
                obj.payment_cost,#cash or chash
                obj.payment_cost,#check
                estimation[obj.check_due_date.weekday()][1],
                real_sale,
                'K%i-J%i'%(row_num+1,row_num+1),
            ]

            style = font_style

            if (today-cur_date).days>0 and check_sale and estimation[first_date.weekday()][1] < check_sale:
                style = font_style_red

            ws.write(row_num, 0, row[0], style)
            ws.write(row_num, 1, row[1], style)
            ws.write(row_num, 2, row[2], style)
            ws.write(row_num, 3, row[3], style)
            ws.write(row_num, 4, row[4], style)
            ws.write(row_num, 5, row[5], style)
            ws.write(row_num, 6, row[6], style)
            if obj.check_bank:
                ws.write(row_num, 8, row[8], style)
                ws.write(row_num, 7, None, style)
            else:
                ws.write(row_num, 7, row[7], style)
                ws.write(row_num, 8, None, style)

            if prev_date != cur_date:
                ws.write(row_num, 9, row[9], style)
                ws.write(row_num, 10, row[10], style)
                ws.write(row_num, 11, xlwt.Formula(row[11]), style)
                first_date = first_date + jdatetime.timedelta(days=1)  # real days
            else:
                ws.write(row_num, 9, None, style)
                ws.write(row_num, 10, None, style)
                ws.write(row_num, 11, None, style)


            prev_date = cur_date#check days




        wb.save(response)
        return response

    export_xls_pro.short_description = u"خروجی اکسل پیشرفته"
    
    def confirm(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_confirm_check'):
            messages.error(request, "شما اجازه تایید ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status == 'paid':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'confirmed'
                q.payment_confirm_user = request.user
                q.payment_confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i چک تایید شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان تایید برخی یا همه چک ها وجود ندارد")

    confirm.short_description = 'تایید چک های انتخاب شده'

    # actions = [confirm, decline, pay, back, export_xls,duplicate_records]
    actions = [decline, pay, back, export_xls,export_xls_pro,duplicate_records,create_cash]

    def get_readonly_fields(self, request, obj=None):
        role = request.user.groups.all()[0].name

        if request.user.is_superuser:
            return list([])

        if request.user.has_perm('AmadoFinance.can_always_edit_check'):
            return ['check_again_date', 'payment_add_user', 'payment_add_date',
                    'payment_confirm_user', 'payment_confirm_date', 'payment_pay_user', 'payment_pay_date',
                    'payment_change_user', 'payment_change_date']

        if request.user.username == 'samsol':
            return ['check_again_date', 'payment_add_user', 'payment_add_date',
                    'payment_confirm_user', 'payment_confirm_date', 'payment_pay_user', 'payment_pay_date',
                    'payment_change_user', 'payment_change_date']

        if not request.user.is_superuser:
            if obj == None:
                if request.user.has_perm('AmadoFinance.can_change_status_check'):
                    return ['check_again_date', 'payment_add_user', 'payment_add_date',
                            'payment_confirm_user', 'payment_confirm_date', 'payment_pay_user', 'payment_pay_date',
                            'payment_change_user', 'payment_change_date']
                return ['check_again_date', 'payment_status', 'payment_add_user', 'payment_add_date',
                        'payment_confirm_user', 'payment_confirm_date', 'payment_pay_user', 'payment_pay_date',
                        'payment_change_user', 'payment_change_date']

            elif obj.payment_status == 'paid' or obj.payment_status == 'confirmed':
                result = list(set(
                    [field.name for field in self.opts.local_fields] +
                    [field.name for field in self.opts.local_many_to_many]
                ))
                if request.user.has_perm('AmadoFinance.can_change_status_check'):
                    result.remove('payment_status')
                result.remove('id')
                result.remove('supplier')
                return result
            elif obj.payment_status == 'back':
                result = list(set(
                    [field.name for field in self.opts.local_fields] +
                    [field.name for field in self.opts.local_many_to_many]
                ))
                if request.user.has_perm('AmadoFinance.can_change_status_check'):
                    result.remove('payment_status')
                result.remove('id')
                result.remove('supplier')
                result.remove('check_again_date')
                return result

            else:
                if request.user.has_perm('AmadoFinance.can_see_check'):
                    result = list(set(
                        [field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]
                    ))
                    if request.user.has_perm('AmadoFinance.can_change_status_check'):
                        result.remove('check_status')
                    result.remove('id')
                    result.remove('supplier')
                    return result
                if request.user.has_perm('AmadoFinance.can_change_status_check'):
                    return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                            'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                            'payment_change_date', 'check_again_date']
                return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date', 'check_again_date']
        return list([])

    def save_model(self, request, instance, form, change):
        user = request.user
        role = request.user.groups.all()[0].name
        if not change:

            if role != 'admin':
                instance.payment_add_user = request.user
                instance.payment_add_date = jdatetime.datetime.now()
        else:
            if role != 'admin':
                instance.payment_change_user = request.user
                instance.payment_change_date = jdatetime.datetime.now()

        instance = form.save(commit=False)

        instance.save()
        form.save_m2m()
        return instance
        #
        # # def has_delete_permission(self, request, obj=None):
        # #     if obj != None:
        # #         user = request.user
        # #         role = request.user.groups.all()[0].name
        # #         if role == 'admin':
        # #             return True
        # #
        # #         if (role == 'amado' and obj.payment_status != 'registered') or (role == 'amadoup' and obj.payment_status != 'registered'):
        # #             messages.error(request, "امکان حذف این پرداخت وجود ندارد")
        # #             return False
        # #         else:
        # #             return True
        # #     else:
        # #         return True
        # #
        # # def _cashpayment_delete(self, request, instance, **kwargs):
        # #     if instance.payment_status != 'registered':
        # #         messages.error(request, "امکان حذف این پرداخت وجود ندارد")
        # #     else:
        # #         instance.delete()
        # #         self.message_user(request, "پرداخت حذف شد")


class FundFilter(admin.SimpleListFilter):
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
            ('notpaid', 'پرداخت نشده'),
            ('registered', 'ثبت شده/در انتظار تایید'),
            ('confirmed', 'تایید شده/در انتظار پرداخت'),
            ('rejected', 'رد شده'),
            ('paid', 'پرداخت شده'),
            ('closed', 'تسویه شد'),

        )

    def queryset(self, request, queryset):
        if self.value() == None:
            r = queryset.exclude(Q(payment_status='paid')|Q(payment_status='closed')).order_by('payment_due_date')
        elif self.value() == 'notpaid':
            r = queryset.exclude(Q(payment_status='paid')|Q(payment_status='closed')).order_by('payment_due_date')
        elif self.value() == 'paid':
            r = queryset.filter(payment_status='paid').order_by('payment_due_date')
        elif self.value() == 'registered':
            r = queryset.filter(payment_status='registered').order_by('payment_due_date')
        elif self.value() == 'confirmed':
            r = queryset.filter(payment_status='confirmed').order_by('payment_due_date')
        elif self.value() == 'rejected':
            r = queryset.filter(payment_status='rejected').order_by('payment_due_date')
        elif self.value() == 'closed':
            r = queryset.filter(payment_status='closed').order_by('payment_due_date')
        else:
            r = queryset

        # if request.user.username == 'sadeghi':
        #     r = r.filter(payment_add_date__gte='1397-04-02 00:00:00').order_by('payment_due_date')
        #     # r= r.exclude(Q(payment_status='paid'))
        #     return r

        return r

        # if self.value() == 'notpaid':
        #     r = FundPayment.objects.exclude(payment_status='paid').order_by('payment_due_date')
        #     return r

        # else:
        #     return queryset.filter()

class FundRelationInline(admin.TabularInline):
    model = RelationShip
    extra = 1
    autocomplete_fields = ['cash','checkp','purchase']

class FundPaymentAdmin(admin.ModelAdmin):
    form = CurrencyFormCash
    list_display = ['see', 'getid', 'date', 'payment_cost','remainder', 'gettitle', 'payment_account', 'bank', 
    # 'payment_recipient',
                    'getrecip','payment_account_person', 'status', 
                    'getadduser'
                    # 'payment_add_user'
                    ]
                    
    def remainder(self,obj):
        sum = RecedeImage.objects.filter(fund=obj).aggregate(sum=Sum('cost'))['sum']
        if sum:
            return obj.payment_cost-sum
        if obj.payment_status != 'paid':
            return obj.payment_cost
        return 0                
    remainder.short_description = 'مانده تنخواه'

                    
    def getrecip(self, obj):
        return obj.payment_recipient    
    getrecip.short_description = 'گیرنده'
    getrecip.admin_order_field = 'payment_recipient'
    
    def getadduser(self, obj):
        return obj.payment_add_user    
    getadduser.short_description = 'ثبت کننده'
    getadduser.admin_order_field = 'payment_add_user'
                    
    search_fields = ['id','payment_cause__cat_name','payment_recipient__recipient_name','payment_title']
    
    fields = ['payment_title','payment_due_date', 'payment_cost', 'payment_cause', 'payment_recipient', 'payment_account',
              'payment_account_type',
              'payment_account_person', 'payment_account_bank','cost_center','over_account', 'payment_description', 'payment_add_user',
              'payment_add_date',
              'payment_confirm_user', 'payment_confirm_date', 'payment_pay_user', 'payment_pay_date',
              'payment_change_user', 'payment_change_date', 'payment_status']

    change_list_template = 'my_change_list.html'
    ordering = ['-payment_due_date']

    def getid(self, obj):
        return obj.pk

    getid.short_description = 'شناسه'
    getid.admin_order_field = 'id'

    def gettitle(self, obj):
        title = ''
        if obj.payment_title:
            title = '%s - %s' % (obj.payment_cause, obj.payment_title)
        else:
            title = '%s' % obj.payment_cause

        return title

    gettitle.short_description = 'بابت'

    def get_queryset(self, request):
        qs = super(FundPaymentAdmin, self).get_queryset(request)
        if request.user.username == 'sadeghi':
            return qs.filter(payment_add_date__gte='1397-04-09 00:00:00')
        return qs

    def export_xls(modeladmin, request, queryset):
        import xlwt
        from django.http import HttpResponse, JsonResponse

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=fund_%s.xls' % jdatetime.datetime.today().strftime(
            '%Y-%m-%d')
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("تنخواه")

        row_num = 0

        columns = [
            (u"تاریخ پرداخت", 3500),
            (u"گیرنده", 6000),
            (u"نماینده", 3500),
            (u"بابت", 10000),
            (u"شماره حساب/کارت", 8000),
            (u"مبلغ پرداختی(ریال)", 4000),
            (u"وضعیت", 6500),
            (u"لینک", 3500),
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300

        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        ws.write_merge(0, 0, 0, 6, 'تاریخ روز: %s' % jdatetime.datetime.today().strftime('%Y/%m/%d'), font_style)

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        row_num += 1

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 2
        font_style.num_format_str = '#,##0'
        font_style.font.height = 250

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al

        for obj in queryset:
            row_num += 1
            status = ''
            if obj.payment_status == 'registered':
                status = 'ثبت شده/در انتظار تایید'
            elif obj.payment_status == 'confirmed':
                status = 'تایید شده/در انتظار پرداخت'
            elif obj.payment_status == 'rejected':
                status = 'رد شده'
            elif obj.payment_status == 'paid':
                status = 'پرداخت شده/در انتظار تسویه'
            else:
                status = 'تسویه شد'

            title = ''
            if obj.payment_title:
                title = '%s - %s' % (obj.payment_cause, obj.payment_title)
            else:
                title = '%s' % obj.payment_cause

            row = [
                obj.payment_due_date.strftime('%Y/%m/%d'),
                obj.payment_recipient.recipient_name,
                obj.payment_account_person,
                title,
                obj.payment_account,
                obj.payment_cost,
                status,
                'http://amadowh.ir/amadofinance/funpayment/%i/change' % obj.pk,
            ]
            ws.write(row_num, 0, row[0], font_style)
            ws.write(row_num, 1, row[1], font_style)
            ws.write(row_num, 2, row[2], font_style)
            ws.write(row_num, 3, row[3], font_style)
            ws.write(row_num, 4, row[4], font_style)
            ws.write(row_num, 5, row[5], font_style)
            ws.write(row_num, 6, row[6], font_style)
            ws.write(row_num, 7, xlwt.Formula('HYPERLINK("%s","مشاهده")' % (row[6])), font_style)

        wb.save(response)
        return response

    export_xls.short_description = u"خروجی اکسل"

    def see(self, obj):
        return mark_safe('<a href="./%i/change">مشاهده </a>' % obj.id)

    see.short_description = 'لینک'

    def bank(self, obj):
        if obj.payment_account_bank:
            return mark_safe('<span style="align=center;">%s</span>' % (obj.payment_account_bank))
        else:
            return 'پوز'

    bank.short_description = 'بانک'

    inlines = [FactorImageInline, RecedeImageInline, FundRelationInline]

    autocomplete_fields = ['payment_account_bank', 'payment_cause', 'payment_recipient']

    list_filter = [FundFilter,  'payment_account_bank','cost_center','over_account', ('payment_due_date', JDateFieldListFilter)]

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

        l = '%s - %s' % (obj.payment_due_date, days[obj.payment_due_date.weekday()][1])
        # l = '%s %s' % (obj.payment_due_date, days[obj.payment_due_date.weekday()][1])
        if obj.payment_status == 'paid' or obj.payment_status == 3:
            return l
        t = jdatetime.datetime.today().strftime('%Y-%m-%d')
        if obj.payment_due_date.strftime('%Y-%m-%d') < t:
            link = '<span style="padding:0 5px;border-radius:5px;background: #f25252;" >%s</span>' % l
        elif obj.payment_due_date.strftime('%Y-%m-%d') == t:
            link = '<span style="padding:0 5px;border-radius:5px;background: #f9e36b;" >%s</span>' % l
        else:
            link = '<span style="padding:0 5px;border-radius:5px;background: #98f970;" >%s</span>' % l

        return mark_safe(link)

    date.short_description = 'تاریخ واریز'
    date.admin_order_field = 'payment_due_date'

    def status(self, obj):
        if obj.payment_status == 'registered':
            # link = '<span style="padding:5px;border-radius:5px;background: #fcf8e3;" >ثبت شده/در انتظار تایید</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #fcf8e3;" ><i class="fas fa-clock"></span>'
        elif obj.payment_status == 'confirmed':
            # link = '<span style="padding:5px;border-radius:5px;background: #d9edf7;" >تایید شده/در انتظار پرداخت</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #d9edf7;" ><i class="fas fa-check-circle"></i></span>'
        elif obj.payment_status == 'rejected':
            # link = '<span style="padding:5px;border-radius:5px;background: #f2dede;" >رد شده</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #f2dede;" ><i class="fas fa-times-circle"></i></span>'
        elif obj.payment_status == 'paid':
            # link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" >پرداخت شده/در انتظار تسویه</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" ><i class="fas fa-check-double"></i></span>'
        else:
            # link = '<span style="padding:5px;border-radius:5px;background: lightgray;" >تسویه شد</span>'
            link = '<span style="padding:5px;border-radius:5px;background: lightgray;" ><i class="fas fa-door-closed"></i></span>'

        return mark_safe(link)

    status.short_description = "وضعیت"

    # status.order_field = ['payment_status']

    def card(self, obj):
        if obj.payment_account_type == 'card':
            return 'کارت %s' % obj.payment_account
        elif obj.payment_account_type == 'account':
            return 'حساب %s' % obj.payment_account
        elif obj.payment_account_type == 'shaba':
            return 'شبا %s' % obj.payment_account
        else:
            return ''

    card.short_description = "شماره"

    # def confirm_but(self,obj):
    #     return 'hi'

    def confirm(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_confirm_fund'):
            messages.error(request, "شما اجازه تایید ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status == 'paid':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'confirmed'
                q.payment_confirm_user = request.user
                q.payment_confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i پرداخت تایید شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان تایید برخی یا همه پرداخت ها وجود ندارد")

    confirm.short_description = 'تایید پرداخت های انتخاب شده'

    def decline(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_decline_cash'):
            messages.error(request, "شما اجازه رد ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status == 'paid':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'rejected'
                q.payment_confirm_user = request.user
                q.payment_confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i پرداخت رد شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان رد برخی یا همه پرداخت ها وجود ندارد")

    decline.short_description = 'رد پرداخت های انتخاب شده'

    def pay(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_pay_fund'):
            messages.error(request, "شما اجازه انجام پرداخت را ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status != 'confirmed':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'paid'
                q.payment_pay_user = request.user
                q.payment_pay_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i پرداخت پرداخت شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان انجام برخی یا همه پرداخت ها وجود ندارد")

    pay.short_description = 'انجام پرداخت های انتخاب شده'

    def close(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_close_fund'):
            messages.error(request, "شما اجازه تسویه تنخواه را ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status != 'paid':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'closed'
                q.payment_pay_user = request.user
                q.payment_pay_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i تنخواه تسویه شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان تسویه برخی یا همه تنخواه ها وجود ندارد")

    close.short_description = 'تسویه تنخواه های انتخاب شده'
    
    def duplicate_records(modeladmin, request, queryset):
        if queryset.count() == 1:
            object_ids = []
            for object in queryset:
                object.id = None
                object.save()
                object_ids.append(object.id)

            if len(object_ids) == 1:
                return redirect('./%i/change' % object_ids[0])
        elif queryset.count() > 1:
            messages.error(request, 'امکان کپی بیش از یک تنخواه وجود ندارد')

    duplicate_records.short_description = 'کپی تنخواه های انتخاب شده'

    actions = [confirm, decline, pay, close, export_xls,duplicate_records]

    def get_readonly_fields(self, request, obj=None):

        # if obj != None and obj.payment_status =='paid':
        #     s=0
        #     for f in FactorImage.objects.filter(fund=obj):
        #       s += f.cost
        #     if s>=obj.payment_cost:
        #         obj.payment_status = 'closed'
        #         obj.save()
        
        if request.user.is_superuser:
            return list([])

        if request.user.has_perm('AmadoFinance.can_always_edit_fund'):
            return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                    'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                    'payment_change_date', ]

        if not request.user.is_superuser:
            if obj == None:
                if request.user.has_perm('AmadoFinance.can_change_status_cash'):
                    return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                            'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                            'payment_change_date', ]
                return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date', ]

            elif obj.payment_status == 'closed' or obj.payment_status == 'confirmed' or obj.payment_status == 'paid':
                result = list(set(
                    [field.name for field in self.opts.local_fields] +
                    [field.name for field in self.opts.local_many_to_many]
                ))
                if request.user.has_perm('AmadoFinance.can_change_cause_fund'):
                    result.remove('payment_cause')
                    result.remove('payment_title')
                if request.user.has_perm('AmadoFinance.can_change_status_cash'):
                    result.remove('payment_status')
                result.remove('id')
                return result
            else:
                if request.user.has_perm('AmadoFinance.can_see_fund'):
                    result = list(set(
                        [field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]
                    ))
                    if request.user.has_perm('AmadoFinance.can_change_status_fund'):
                        result.remove('payment_status')
                    result.remove('id')
                    return result
                if request.user.has_perm('AmadoFinance.can_change_status_fund'):
                    return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                            'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                            'payment_change_date', ]
                return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date']
        return list()

    def save_model(self, request, instance, form, change):

        user = request.user
        role = request.user.groups.all()[0].name
        if not change:

            if not request.user.is_superuser:
                instance.payment_add_user = request.user
                instance.payment_add_date = jdatetime.datetime.now()
        else:
            if not request.user.is_superuser:
                instance.payment_change_user = request.user
                instance.payment_change_date = jdatetime.datetime.now()

        instance = form.save(commit=False)

        instance.save()
        form.save_m2m()
        return instance

        # def has_delete_permission(self, request, obj=None):
        #     if obj != None:
        #         user = request.user
        #         role = request.user.groups.all()[0].name
        #         if role == 'admin':
        #             return True
        #
        #         if (role == 'amado' and obj.payment_status != 'registered') or (role == 'amadoup' and obj.payment_status != 'registered'):
        #             messages.error(request, "امکان حذف این پرداخت وجود ندارد")
        #             return False
        #         else:
        #             return True
        #     else:
        #         return True
        #
        # def _cashpayment_delete(self, request, instance, **kwargs):
        #     if instance.payment_status != 'registered':
        #         messages.error(request, "امکان حذف این پرداخت وجود ندارد")
        #     else:
        #         instance.delete()
        #         self.message_user(request, "پرداخت حذف شد")


class RecedeImageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if request.user.is_superuser:
            perms = admin.ModelAdmin.get_model_perms(self, request)
            return perms
        return {}


class FactorImageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if request.user.is_superuser:
            perms = admin.ModelAdmin.get_model_perms(self, request)
            return perms
        return {}

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['person','card','account','shaba','bank']
    search_fields = ['card','account','shaba','person','bank__bank_name']


from AmadoWH.mysite import site

site.register(Sales, SalesAdmin)
site.register(RecipientCompany, RecipientCompanyAdmin)
site.register(Bank, BankAdmin)
site.register(RecedeImage, RecedeImageAdmin)
site.register(FactorImage, FactorImageAdmin)
site.register(CheckCategory, CheckCatAdmin)
site.register(PaymentCategory, PaymentCategoryAdmin)
site.register(CashPayment, CashPaymentAdmin)
site.register(FundPayment, FundPaymentAdmin)
site.register(CheckPayment, CheckPaymentAdmin)
site.register(Pos, PosAdmin)
site.register(InternetSeller, InternetAdmin)
site.register(BankAccount,BankAccountAdmin)
site.register(CostCenter)
