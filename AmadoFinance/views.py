from django.shortcuts import render
from django.db.models import IntegerField

from django.http import HttpResponse, JsonResponse
from django.db.models import Sum,Q,Count,F
from django.template import loader
import jdatetime
import requests
from django.shortcuts import redirect
import random
import string

from AmadoFinance.models import *
import AmadoWHApp
from AmadoAccounting.models import Person, WorkDetail
from AmadoWHApp.models import ShopDetail, Product, Price
import pprint

def view_cash(request):



    json = []
    for p in Person.objects.filter(id__in=[11,8,23,38,27]):
        wd = WorkDetail.objects.filter(Q(work__date__lte='1397-05-21')&Q(work__date__gte='1397-05-01')&Q(person=p)).order_by('work__date').values('work_status','work__date')
        json.append({'person':p.name,'details':wd})


    c = {'json': json}
    template = loader.get_template('temp.html')
    return HttpResponse(template.render(c, request))

    # import xlwt
    # from django.http import HttpResponse, JsonResponse
    #
    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition'] = u'attachment; filename=cash_%s.xls' % jdatetime.datetime.today().strftime(
    #     '%Y-%m-%d')
    # wb = xlwt.Workbook(encoding='utf-8')
    # ws = wb.add_sheet("واریزی")
    #
    # row_num = 0
    #
    # columns = [
    #     (u"نام فرد", 6000),
    #     (u"1", 3000),
    #     (u"2", 3000),
    #     (u"3", 3000),
    #     (u"4", 3000),
    #     (u"5", 3000),
    #     (u"6", 3000),
    #     (u"7", 3000),
    #     (u"8", 3000),
    #     (u"9", 3000),
    #     (u"10", 3000),
    #     (u"11", 3000),
    #     (u"12", 3000),
    #     (u"13", 3000),
    #     (u"14", 3000),
    #     (u"15", 3000),
    #     (u"16", 3000),
    #     (u"17", 3000),
    #     (u"18", 3000),
    #     (u"19", 3000),
    #     (u"20", 3000),
    #
    # ]
    #
    # # font_style = xlwt.XFStyle()
    # # font_style.font.bold = True
    # # font_style.num_format_str = '#,##0'
    # # font_style.font.height = 300
    #
    #
    # # ws.write_merge(0, 0, 0, 6, 'تاریخ روز: %s' % jdatetime.datetime.today().strftime('%Y/%m/%d'), font_style)
    #
    # font_style = xlwt.XFStyle()
    # font_style.font.bold = True
    # font_style.num_format_str = '#,##0'
    # font_style.font.height = 300
    #
    #
    #
    # row_num += 1
    #
    # for col_num in range(len(columns)):
    #     ws.write(row_num, col_num, columns[col_num][0], font_style)
    #     # set column width
    #     ws.col(col_num).width = columns[col_num][1]
    #
    # font_style = xlwt.XFStyle()
    # font_style.alignment.wrap = 2
    # font_style.num_format_str = '#,##0'
    # font_style.font.height = 250
    #
    #
    # for obj in Person.objects.filter(id__in=[11,8,23,38,27]):
    #     row_num += 1
    #     status = ''
    #     if obj.payment_status == 'registered':
    #         status = 'ثبت شده/در انتظار تایید'
    #     elif obj.payment_status == 'confirmed':
    #         status = 'تایید شده/در انتظار پرداخت'
    #     elif obj.payment_status == 'rejected':
    #         status = 'رد شده'
    #     else:
    #         status = 'پرداخت شده/در انتظار تسویه'
    #
    #     title = ''
    #     if obj.payment_title:
    #         title = '%s - %s' % (obj.payment_cause, obj.payment_title)
    #     else:
    #         title = '%s' % obj.payment_cause
    #
    #     row = [
    #         obj.person_name,
    #         WorkDetail.objects.filter(Q(work__date__lte='1397-05-21')&Q(work__date__gte='1397-05-01')).values('work_status')
    #     ]
    #
    #     ws.write(row_num, 0, row[0], font_style)
    #     ws.write(row_num, 1, row[1], font_style)
    #     ws.write(row_num, 2, row[2], font_style)
    #     ws.write(row_num, 3, row[3], font_style)
    #     ws.write(row_num, 4, row[4], font_style)
    #     ws.write(row_num, 5, row[5], font_style)
    #     ws.write(row_num, 6, row[6], font_style)
    #     ws.write(row_num, 7, xlwt.Formula('HYPERLINK("%s","مشاهده")' % (row[6])), font_style)
    #
    # wb.save(response)
    # return response


    return JsonResponse({'result':'hi'})

#def supplier_report(request):
#    if not request.user.has_perm('sessions.can_see_supplier_payment_report'):
#        return redirect('/admin/login/?next=/admin/')
#
#    try:
#        from_date = jdatetime.datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d')
#    except:
#        from_date = jdatetime.datetime.strptime('1300-01-01', '%Y-%m-%d')
#
#    try:
#        to_date = jdatetime.datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d')
#    except:
#        to_date = jdatetime.datetime.strptime('1500-01-01', '%Y-%m-%d')
#
#
#    this_year = jdatetime.datetime.today().year
#    
#    
#    if request.GET.get('supplier'):
#        
#        try:
#            cash = CashPayment.objects.filter(Q(supplier=int(request.GET.get('supplier')))&Q(payment_due_date__lte=to_date)&Q(payment_due_date__gte=from_date)).extra(select={'date': 'payment_due_date', 'cost': 'payment_cost'}).values(
#                'id', 'date', 'cost', 'payment_account_type', 'payment_account', 'payment_account_bank__bank_name',
#                'payment_account_person')
#            check = CheckPayment.objects.filter(Q(supplier=int(request.GET.get('supplier')))&Q(check_due_date__lte=to_date)&Q(check_due_date__gte=from_date)).extra(select={'date': 'check_due_date', 'cost': 'payment_cost'}).values(
#                'id', 'date', 'cost', 'check_bank__bank_name', 'check_number')
#                
#            shops = ShopDetail.objects.filter(Q(shop__supplier=int(request.GET.get('supplier')))&Q(shop__from_date__lte=to_date)&Q(shop__from_date__gte=from_date)) \
#                .order_by('shop__from_date', 'shop__id') \
#                .values('shop__id','shop__supplier', 'shop__from_date') \
#                .annotate(
#                cost=Sum(F('amount') * F('last_price'), output_field=IntegerField()))
#        except:
#            data = {
#            'payments':[],
#            'sum':0,
#            'suppliers':Supplier.objects.all().order_by('supplier_name'),
#            'until_from_date_sum':0,
#            'until_this_year_sum':0,
#            'this_year':'%i'%this_year
#            }
#
#            template = loader.get_template('supplier_report_change_list.html')
#            return HttpResponse(template.render(data, request))
#
#    else:
#        data = {
#            'payments':[],
#            'sum':0,
#            'suppliers':Supplier.objects.all().order_by('supplier_name'),
#            'until_from_date_sum':0,
#            'until_this_year_sum':0,
#            'this_year':'%i'%this_year
#            }
#
#        template = loader.get_template('supplier_report_change_list.html')
#        return HttpResponse(template.render(data, request))
#        
#        # cash = CashPayment.objects.all().extra(select={'date': 'payment_due_date', 'cost': 'payment_cost'}).values(
#        #     'id', 'date', 'cost', 'payment_account_type', 'payment_account', 'payment_account_bank__bank_name',
#        #     'payment_account_person')
#        # check = CheckPayment.objects.all().extra(select={'date': 'check_due_date', 'cost': 'payment_cost'}).values(
#        #     'id', 'date', 'cost', 'check_bank__bank_name', 'check_number')
#
#    cash = cash.filter(Q(payment_due_date__gte=from_date)&Q(payment_due_date__lte=to_date))
#    check = check.filter(Q(check_due_date__gte=from_date)&Q(check_due_date__lte=to_date))
#
#
#    
#
#    until_this_year_sum = 0
#    until_from_date_sum = 0
#
#    cash = list(cash)
#    s = 0
#
#    try:
#
#        until_from_date_sum += CashPayment.objects.filter(Q(payment_due_date__lt=from_date)&Q(supplier=int(request.GET.get('supplier')))).aggregate(sum=Sum('payment_cost'))['sum']
#    except:
#        until_from_date_sum = 0
#
#    try:
#        until_from_date_sum += CheckPayment.objects.filter(
#            Q(check_due_date__lt=from_date) & Q(supplier=int(request.GET.get('supplier')))).aggregate(
#            sum=Sum('payment_cost'))['sum']
#    except:
#        until_from_date_sum = 0
#
#
#
#    try:
#        for c in CashPayment.objects.filter(Q(supplier=int(request.GET.get('supplier')))):
#            if c.payment_due_date.year < this_year:
#                until_this_year_sum += c.payment_cost
#    except:
#        until_this_year_sum = 0
#
#    try:
#        for c in CheckPayment.objects.filter(Q(supplier=int(request.GET.get('supplier')))):
#            if c.check_due_date.year < this_year:
#                until_this_year_sum += c.payment_cost
#    except:
#        until_this_year_sum = 0
#
#
#    shop_sum=0
#    for shop in shops:
#        shop['date'] = shop.pop('shop__from_date')
#        shop['id'] = shop.pop('shop__id')
#        shop['date'] = shop['date'].strftime('%Y/%m/%d')
#        shop['payment'] = False
#        shop['payment_account_type'] = None
#        shop['payment_account_bank__bank_name'] = None
#        shop['payment_account_person'] = None
#        shop['desc'] = ''
#        shop_sum += shop['cost']
#        shop['link'] = '../../AmadoWHApp/shoprequest/%i/change'%shop['id']
#
#
#    for c in cash:
#        date = jdatetime.date.fromgregorian(date=c['date'])
#        c['date'] = date.strftime('%Y/%m/%d')
#
#        c['payment'] = True
#
#        c['type'] = 'واریز نقدی'
#        if c['payment_account_type'] == 'card':
#            c['desc'] = 'واریز به کارت %s بانک %s به نام %s'%(c['payment_account'],c['payment_account_bank__bank_name'] or '',c['payment_account_person'])
#        elif c['payment_account_type'] == 'card':
#            c['desc'] = 'واریز به شماره حساب %s بانک %s به نام %s' % (
#            c['payment_account'], c['payment_account_bank__bank_name'] or '', c['payment_account_person'])
#        elif c['payment_account_type'] == 'shaba':
#            c['desc'] = 'حواله پایا به شماره %s بانک %s به نام %s' % (
#                c['payment_account'], c['payment_account_bank__bank_name'] or '', c['payment_account_person'])
#        else:
#            c['desc'] = 'عملیات پوز'
#
#        c['link'] = '../../AmadoFinance/cashpayment/%i/change' % c['id']
#
#        s += c['cost']
#
#    check = list(check)
#    for c in check:
#        date = jdatetime.date.fromgregorian(date=c['date'])
#        c['date'] = date.strftime('%Y/%m/%d')
#
#        c['payment'] = True
#
#        c['type'] = 'چک'
#        if c['check_bank__bank_name']:
#            c['desc'] = 'چک به شماره %s بانک %s سررسید %s'%(c['check_number'],c['check_bank__bank_name'],c['date'])
#        else:
#            c['desc'] = 'نقدی'
#
#        c['link'] = '../../AmadoFinance/checkpayment/%i/change' % c['id']
#
#        s += c['cost']
#
#    cash = cash+check+list(shops)
#    
#    def getdate(json):
#        return json['date']
#    
#    cash.sort(key=getdate)
#
#
#
#    data = {
#            'payments':cash,
#            'sum':s,
#            'suppliers':Supplier.objects.all(),
#            'until_from_date_sum':until_from_date_sum,
#            'until_this_year_sum':until_this_year_sum,
#            'this_year':'%i'%this_year,
#            'sums':shops,
#            'shop_sum' : shop_sum,
#            'difference':shop_sum-s
#    }
#
#    template = loader.get_template('supplier_report_change_list.html')
#    return HttpResponse(template.render(data, request))
#
def supplier_report(request):
    if not request.user.has_perm('sessions.can_see_supplier_payment_report'):
        return redirect('/admin/login/?next=/admin/')

    try:
        from_date = jdatetime.datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d')
    except:
        from_date = jdatetime.datetime.strptime('1300-01-01', '%Y-%m-%d')

    try:
        to_date = jdatetime.datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d')
    except:
        to_date = jdatetime.datetime.strptime('1500-01-01', '%Y-%m-%d')


    this_year = jdatetime.datetime.today().year


    if request.GET.get('supplier'):

        try:
            cash = RecedeImage.objects.filter(
                Q(payment_due_date__lte=to_date)&
                Q(payment_due_date__gte=from_date)&
                ((Q(factor__supplier=int(request.GET.get('supplier')))|Q(checkp__supplier=int(request.GET.get('supplier'))))) &
                Q(cost__gt=0)).order_by('payment_due_date').values('factor__id','factor__payment_account_type',
                                                                                         'factor__payment_account','factor__payment_account_bank__bank_name',
                                                                                         'factor__payment_account_person',
                                                                   'checkp__id','checkp__check_bank__bank_name','checkp__check_number','checkp__check_due_date'
                                                                   ,'payment_due_date','cost','image_title')

            shops = ShopDetail.objects.filter(Q(shop__supplier=int(request.GET.get('supplier')))
            &Q(shop__from_date__lte=to_date)&
                Q(shop__from_date__gte=from_date)) \
                .order_by('shop__from_date', 'shop__id') \
                .values('shop__id','shop__supplier', 'shop__from_date') \
                .annotate(
                cost=Sum(F('amount') * F('last_price'), output_field=IntegerField()))

        except:
            data = {
                'payments': [],
                'sum': 0,
                'suppliers': Supplier.objects.all(),
                'until_from_date_sum': 0,
                'until_this_year_sum': 0,
                'this_year': '%i' % this_year
            }

            template = loader.get_template('supplier_report_change_list.html')
            return HttpResponse(template.render(data, request))

    else:

        data = {
            'payments': [],
            'sum': 0,
            'suppliers': Supplier.objects.all(),
            'until_from_date_sum': 900,
            'until_this_year_sum': 0,
            'this_year': '%i' % this_year
        }

        template = loader.get_template('supplier_report_change_list.html')
        return HttpResponse(template.render(data, request))

    until_this_year_sum = 0
    until_from_date_sum = 0

    cash = list(cash)
    s = 0

    try:
        until_from_date_sum += cash.filter(Q(payment_due_date__lt=from_date))\
            .aggregate(sum=Sum('cost'))['sum']
    except:
        until_from_date_sum = 0


    try:
        for c in cash:
            if c.payment_due_date.year < this_year:
                until_this_year_sum += c.cost
    except:
        until_this_year_sum = 0


    shop_sum=0
    for shop in shops:
        shop['payment_due_date'] = shop.pop('shop__from_date')
        x = shop.pop('shop__id')
        shop['factor__id'] = x
        shop['payment'] = False
        shop['factor__payment_account_type'] = None
        shop['factor__payment_account_bank__bank_name'] = None
        shop['factor__payment_account_person'] = None
        shop['desc'] = ''
        shop_sum += shop['cost']
        shop['link'] = '../../AmadoWHApp/shoprequest/%i/change'%shop['factor__id']


    for c in cash:

        c['payment'] = True

        if c['factor__id']:

            c['type'] = 'واریز نقدی'
            if c['factor__payment_account_type'] == 'card':
                c['desc'] = 'واریز به کارت %s بانک %s به نام %s'%(c['factor__payment_account'],c['factor__payment_account_bank__bank_name'] or '',c['factor__payment_account_person'])
            elif c['factor__payment_account_type'] == 'card':
                c['desc'] = 'واریز به شماره حساب %s بانک %s به نام %s' % (
                c['factor__payment_account'], c['factor__payment_account_bank__bank_name'] or '', c['factor__payment_account_person'])
            elif c['factor__payment_account_type'] == 'shaba':
                c['desc'] = 'حواله پایا به شماره %s بانک %s به نام %s' % (
                    c['factor__payment_account'], c['factor__payment_account_bank__bank_name'] or '', c['factor__payment_account_person'])
            else:
                c['desc'] = 'عملیات پوز'

            c['link'] = '../../AmadoFinance/cashpayment/%i/change' % c['factor__id']
        else:
            c['type'] = 'چک'
            if c['checkp__check_bank__bank_name']:
                c['desc'] = 'چک به شماره %s بانک %s سررسید %s' % (
                c['checkp__check_number'], c['checkp__check_bank__bank_name'], c['checkp__check_due_date'])
            else:
                c['desc'] = 'نقدی'

            c['link'] = '../../AmadoFinance/checkpayment/%i/change' % c['checkp__id']

        s += c['cost']


    cash = cash+list(shops)

    def getdate(json):
        return json['payment_due_date']



    cash.sort(key=getdate)

    data = {
            'payments':cash,
            'sum':s,
            'suppliers':Supplier.objects.all(),
            'until_from_date_sum':until_from_date_sum,
#            'until_from_date_sum':10000,
            'until_this_year_sum':until_this_year_sum,
            'this_year':'%i'%this_year,
            'sums':shops,
            'shop_sum' : shop_sum,
            'difference':shop_sum-s
    }

    template = loader.get_template('supplier_report_change_list.html')
    return HttpResponse(template.render(data, request))