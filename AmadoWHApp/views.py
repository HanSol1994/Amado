from django.http import HttpResponse,JsonResponse
from .models import *
from django.db.models import Sum,Q,Count,Case,When,F
from django.template import loader
import jdatetime
import requests
from django.shortcuts import redirect
import random
import string
from django.contrib.auth.models import User

def report(request):
   
    
#    import os
#    import pandas as pd
#
#    foods = pd.read_csv(os.path.join(os.path.dirname(__file__),'lvl2.csv'))
#    for a in foods.iterrows():
#        print(a[1][0])
#        p = Product.objects.get(id=int(a[1][0]))
#        r = RawProduct.objects.get(id=int(a[1][1]))
#        unit = Unit.objects.get(id=int(a[1][2]))
#        amount = float(a[1][3])
#        recipe = Recipe12(recipe_child_product=p,recipe_parent_product=r,recipe_amount=amount,recipe_unit=unit)
#        recipe.save()
            
    
#    import os
#    import pandas as pd
#    
#    foods = pd.read_csv(os.path.join(os.path.dirname(__file__),'cost_pid.csv'))
#    for a in foods.iterrows():
#        p = Product.objects.get(id=int(a[1]['pid']))
#        price = Price(cost=int(a[1]['cost']),date='1397-08-26',product=p)
#        price.save()
    
#
#    Recipe23.objects.all().delete()
#
#    foods = pd.read_csv(os.path.join(os.path.dirname(__file__),'foods_a.csv'))
#    for a in foods.iterrows():
#        food = AmadoFood.objects.get(id=int(a[1]['food_id']))
#        product = Product.objects.get(id=int(a[1]['pid']))
#        unit = Unit.objects.get(id=int(a[1]['unit']))
#        r = Recipe23(recipe_child_product=food,recipe_parent_product=product,recipe_amount=a[1]['amount'],recipe_unit=unit)
#        r.save()
    
#    for v in RequestProductVariance.objects.filter(id__in=[720,721,722,723,724,725]):
#        v.request_time = '15:45:00'
#        v.request_date = '1397-07-27'
#        v.save()

    
    # for sd in ShopDetail.objects.all():
    #     p = sd.product
    #     try:
    #         np = RawProduct.objects.filter(product_name=p.product_name)[0]
    #         sd.productr = np
    #         sd.save()
    #     except:
    #         print(p)
    
    # for p in ShopDetail.objects.all():
    #     newp = RawProduct.objects.get_or_create(product_name=p.product.product_name,product_is_active=p.product.product_is_active)

    # for p in CashPayment.objects.all():
    #     if p.payment_factor:
    #         f = FactorImage(factor=p,image=p.payment_factor)
    #         f.save()
    #
    #     if p.payment_recede:
    #         r = RecedeImage(factor=p, image=p.payment_recede)
    #         r.save()

    # import os
    # import pandas as pd
    # from django.conf import settings
    #
    # df = pd.read_csv(os.path.join(settings.PROJECT_ROOT, 'cash.csv'), sep=',', header=None,keep_default_na=False)
    #
    # for i in range(0,300):
    #     date = df.loc[i][0]
    #     recipient = df.loc[i][1]
    #     person = df.loc[i][2]
    #     cause = df.loc[i][3]
    #     number = df.loc[i][4]
    #     type = df.loc[i][5]
    #     bank = df.loc[i][6]
    #     cost = df.loc[i][7]
    #     status = df.loc[i][8]
    #
    #
    #
    #     pc,f  = PaymentCategory.objects.get_or_create(cat_name=cause)
    #
    #     r,f = RecipientCompany.objects.get_or_create(recipient_name=recipient)
    #     admin =User.objects.get(username='admin')
    #
    #     if bank!='':
    #         b,f = Bank.objects.get_or_create(bank_name=bank)
    #         c = CashPayment(payment_account_bank=b,payment_recipient=r,payment_due_date=date,payment_account=number,payment_cost=cost,
    #                          payment_cause=pc,payment_account_type=type,payment_account_person=person
    #                          ,payment_add_user=admin,payment_add_date='1397-04-01 16:30:00'
    #                          ,payment_confirm_user=admin,payment_confirm_date='1397-04-01 16:30:00'
    #                          ,payment_pay_user=admin,payment_pay_date='1397-04-01 16:30:00'
    #                          ,payment_status=status
    #                          )
    #     else:
    #         c = CashPayment(payment_recipient=r, payment_due_date=date, payment_account=number,
    #                         payment_cost=cost,
    #                         payment_cause=pc, payment_account_person=person
    #                         , payment_add_user=admin, payment_add_date='1397-04-01 16:30:00'
    #                         , payment_confirm_user=admin, payment_confirm_date='1397-04-01 16:30:00'
    #                         , payment_pay_user=admin, payment_pay_date='1397-04-01 16:30:00'
    #                         , payment_status=status
    #                         )
    #     c.save()

        # p = Product.objects.get(product_name=name)
        # t = 'فروش %s اردیبهشت'%name
        # u = Unit.objects.get(unit_name='عدد')
        # p.productoutput_set.create(output_title=t,output_amount=amount,output_unit=u,output_start_date='1397-02-01',output_finish_date='1397-02-31')
        # print(recipient)
        # print(number=='')
        # print(date)
        # print(number)
        # print(cost)
        # print(cause)
        # print(cat)
        # print(status)
        
        
   

    api_key = request.GET.get('k')
    wanted_date = request.GET.get('date')
    today = jdatetime.datetime.strptime(wanted_date, "%Y-%m-%d")
    yesterday = (today + jdatetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    today = today.strftime("%Y-%m-%d")

    if api_key == 'kjdfjwelgihwe' and wanted_date:

        #darkhast ha baraye today, momkene emrooz sabt shode bashe momkene dirshab
        r3 = Request.objects.filter(
                                    Q(request_branch__id=3)&
                                    (
                                        (Q(request_date=today) )


                                     )
                                    ).values('request_code').annotate(count=Count('request_product'))
        # r3 = Request.objects.filter(request_code='9702310301').values('request_code').annotate(count=Count('request_product'))                                    
        r3 = r3.filter().values('request_code').last()


        r4 = Request.objects.filter(
            Q(request_branch__id=4) &
            (
                (Q(request_date=today))

            )
        ).values('request_code').annotate(count=Count('request_product'))
        r4 = r4.filter().values('request_code').last()


        r5 = Request.objects.filter(
            Q(request_branch__id=5) &
            (
                (Q(request_date=today) )

            )
        ).values('request_code').annotate(count=Count('request_product'))
        r5 = r5.filter().values('request_code').last()


        r6 = Request.objects.filter(
            Q(request_branch__id=6) &
            (
                (Q(request_date=today) )

            )
        ).values('request_code').annotate(count=Count('request_product'))
        r6 = r6.filter().values('request_code','request_date','request_time').last()

       
        r7 = Request.objects.filter(
            Q(request_branch__id=7) &
            (
                (Q(request_date=today) )

            )
        ).values('request_code').annotate(count=Count('request_product'))
        r7 = r7.filter().values('request_code').last()


        if r3 == None:
            r3 = {'request_code':'-'}
        if r4 == None:
            r4 = {'request_code':'-'}
        if r5 == None:
            r5 = {'request_code':'-'}
        if r6 == None:
            r6 = {'request_code':'-'}
        if r7 == None:
            r7 = {'request_code':'-'}
            


        products = RequestProduct.objects.filter(
            Q(request_request__request_code=r3['request_code'])|
            Q(request_request__request_code=r4['request_code'])|
            Q(request_request__request_code=r5['request_code'])|
            Q(request_request__request_code=r6['request_code'])|
            Q(request_request__request_code=r7['request_code'])
            ).values('request_product__product_name','request_product__product_unit__unit_name').annotate(amount=Sum('request_amount')).order_by('request_product__product_name')


        template = loader.get_template('report.html')

        count = products.count()

        date = today.replace('-','/')
        
        context = {'date':date,'products': list(products),'count':count,'branch':'شعب'}

        return HttpResponse(template.render(context, request))

    else:
        template = loader.get_template('report.html')
        return HttpResponse(template.render({}, request))


def sendsms(request):
    # for s in ShopDetail.objects.all():
    #     s.last_price = s.last_price*10
    #     s.save()

    # for p in Price.objects.all():
    #     p.cost = p.cost*10
    #     p.save()
    # date = jdatetime.datetime.today().strftime("%Y/%m/%d")
    # td = jdatetime.datetime.today().strftime("%Y-%m-%d")

    # message = 'سفارشات %s' % date
    # message += " http://www.amadowh.ir/report/?k=kjdfjwelgihwe&date="
    # message += td
    
    # # operator = "100020400"
    # operator = "100009"
    # # resp = requests.post(
    # #     "http://37.130.202.188/class/sms/webservice/send_url.php?from=+98" + operator + "&to=+989213283585&msg=" + message + "&uname=nanba&pass=hansol1994",
    # #     headers={
    # #         "Accept": "application/json"
    # #     })
        
    # resp = requests.post(
    #     "http://37.130.202.188/class/sms/webservice/send_url.php?from=+98" + operator + "&to=+989198989371&msg=" + message + "&uname=nanba&pass=hansol1994",
    #     headers={
    #         "Accept": "application/json"
    #     })

    return redirect('../admin/AmadoWHApp/request')

def getform(request):

    request_code = request.GET.get("rc")
    key = request.GET.get("k")

    if request_code and key =='h47g1304817g':

        try:

            branch = Request.objects.filter(Q(request_code=request_code) ).values('request_branch__branch_name')[0]

            products = RequestProduct.objects.filter(Q(request_request__request_code=request_code) ) \
                .values('request_product__product_name', 'request_amount','request_unit','request_unit__unit_name', 'request_product__product_unit__unit_name','request_amount_sent','request_unit_sent__unit_name','request_unit_sent',
                        'request_description').order_by('request_product__product_name')

            template = loader.get_template('report_accountant.html')

            count = products.count()

            date = jdatetime.datetime.today().strftime("%Y/%m/%d")
            req_date = Request.objects.filter(Q(request_code=request_code) ).last().request_date
            req_date = req_date+jdatetime.timedelta(days=1)

            context = {'date': date,'req_date':req_date.strftime("%Y/%m/%d"), 'products': list(products), 'count': count,
                       'branch': branch['request_branch__branch_name'], 'code': request_code}

            return HttpResponse(template.render(context, request))
        except:
            template = loader.get_template('report_accountant.html')
            return HttpResponse(template.render({}, request))
    else:
        template = loader.get_template('report_accountant.html')
        return HttpResponse(template.render({}, request))
        

import json

def get_prices(request):
    products = list(ShopDetail.objects.all().order_by('product__product_name').values('product'))

    j = []
    
    ids = []

    for p in products:
        last = ShopDetail.objects.filter(product__id=p['product']).order_by('shop__from_date').last()
        
        if p['product'] not in ids:
            ids.append(p['product'])
            j.append({
                        
                        'id':p['product'],
                        'name':last.product.product_name,
                        'price':last.last_price,
                        'unit':last.unit.unit_name,
                        'shop__supplier': last.shop.supplier.supplier_name,
                        'shop_date': last.shop.from_date.strftime('%Y-%m-%d'),
                        'shop_id': last.shop.id,
        
                    })
                    
                
            
                
            


    return JsonResponse({'products':json.dumps(j)})

def branchvar(request,id):

    if not request.user.is_authenticated:
        return redirect('../../../../admin/login/?next=/report/branchvar/%i'%id)
#    if not request.user.has_perm('auth.can_see_report'):
#        try:
#            b = BranchWarehouse.objects.get(id=id).branch
#            branch = Branch.objects.get(Q(branch_manager__manager_user=request.user)&Q(id=b.id))
#        except:
#            return redirect('../../../../admin/AmadoWHApp/branchwarehouse/')
#
#    else:
#        pass

#    def turn_to_little_unit(amount,product,unit):
#        if unit is None:
#            # using product default unit
#            if product.product_unit_ratio>1:
#                return amount * product.product_unit_ratio,product.product_second_unit
#            else:
#                return amount , product.product_unit
#
#        if unit == product.product_unit:
#            # using product big unit
#            if product.product_unit_ratio>1:
#                return amount * product.product_unit_ratio,product.product_second_unit
#            else:
#                return amount , product.product_unit
#        elif unit == product.product_second_unit:
#            # using product small unit
#            return amount, product.product_second_unit
#        else:
#            return None

    def turn_to_little_unit(amount,product,unit):
        
        if unit is None or unit == product.product_unit:
                # using product default unit
                if product.product_unit_ratio > 1:
                    return amount * product.product_unit_ratio, product.product_second_unit
                else:
                    return amount, product.product_unit
                
        if unit == product.product_second_unit:
            return amount, product.product_second_unit
        
        try:
            ration = UnitToUnit.objects.get(product=product, first_unit=unit,second_unit=product.product_second_unit).ration

            return amount*ration, product.product_second_unit

            # if unit == product.product_unit:
            #     # using product big unit
            #     if product.product_unit_ratio > 1:
            #         return amount * product.product_unit_ratio, product.product_second_unit
            #     else:
            #         return amount, product.product_unit
            # elif unit == product.product_second_unit:
            #     # using product small unit
            #     return amount, product.product_second_unit
            # else:
            #     return None
        except:
            return None




    result =[]

    bw = BranchWarehouse.objects.get(id=id)
#    if bw.status != 'confirmed' and bw.status != 'byadmin' and not request.user.is_superuser:
#        return redirect('../../../../admin/AmadoWHApp/branchwarehouse/')
    date = bw.date
    last_date = BranchWarehouse.objects.filter(Q(branch=bw.branch)&Q(date__lt=date)).order_by('date').last().date
    branch = bw.branch
    
    
#    related = [{'nkh': [19, 20, 21, 22]},{'ngh':[10,11,12,13]},{'del':[15,16,17]},{'fre':[208,209,210,211,212,213,214]},{'barb':[341,342,364,365]},{'ab':[226,227]},{'chi':[146,219]},{'sir':[145,231]},{'kal':[162,232]}]
#    
    related = [{'nkh': [19, 20, 21, 22]},{'ngh':[10,11,12,13]},{'del':[15,16,17]},{'fre':[208,209,210,211,212,213,214]},{'barb':[341,342,364,365]},{'ab':[226,227]},]

    for w in BranchWarehouseProduct.objects.filter(branch_warehouse=id):
        product = w.product
        last_day = date + jdatetime.timedelta(days=-1)
        
        if product.id in related[1]['ngh']:
            rel = related[1]['ngh']
            rel_name = 'نوشابه قوطی'
        elif product.id in related[0]['nkh']:
            rel = related[0]['nkh']
            rel_name = 'نوشابه خانواده'
        elif product.id in related[2]['del']:
            rel = related[2]['del']
            rel_name = 'هی دی'
        elif product.id in related[3]['fre']:
            rel = related[3]['fre']
            rel_name = 'فرشی'
        elif product.id in related[4]['barb']:
            rel = related[4]['barb']
            rel_name = 'باربیکن'
        elif product.id in related[5]['ab']:
            rel = related[5]['ab']
            rel_name = 'آب معدنی'
#        elif product.id in related[6]['chi']:
#            rel = related[6]['chi']
#            rel_name = 'سس چیلی تای'    
#        elif product.id in related[7]['sir']:
#            rel = related[7]['sir']
#            rel_name = 'سس سیر'        
#        elif product.id in related[8]['kal']:
#            rel = related[8]['kal']
#            rel_name = 'سالاد کلم'        
        else:
            rel =[product.id]
            rel_name = product.product_name

        #today real
        real_amount,wunit = turn_to_little_unit(w.amount,product,product.product_second_unit)

        
        #last warehouse report
        
        try:
            pw = BranchWarehouseProduct.objects.get(Q(branch_warehouse__branch=branch)&Q(branch_warehouse__date=last_date)&Q(product=product))
            pwamount = pw.amount
            pwunit = pw.product.product_second_unit
        except:
            pwamount = 0
            pwunit = product.product_second_unit
            
        last_pw,lpwunit = turn_to_little_unit(pwamount,product,pwunit)    

        #last request
        
        try:
            if product.id in rel:
                r1 = RequestProduct.objects.filter(Q(request_request__request_branch=branch) &
                                               Q(request_request__request_date__gte=last_date) & Q(request_request__request_date__lt=date) &
                                                  Q(request_product__id__in=rel))
                r2 = r1.filter().aggregate(amount=Sum('request_amount'))
                last_req, requnit = turn_to_little_unit(r2['amount'], product, r1[0].request_unit)
                
                r2prime = r1.filter().aggregate(amount=Sum('request_amount_sent'))

                last_req, requnit = turn_to_little_unit(r2['amount'], product, r1[0].request_unit)
                if r2prime['amount'] != None:
                    
                    last_req2, requnit = turn_to_little_unit(r2prime['amount'], product, r1[0].request_unit_sent)

                    last_req = last_req + last_req2 - last_req 
                
            else:    
                r = RequestProduct.objects.get(Q(request_request__request_branch=branch)&
                                               Q(request_request__request_date__gte=last_date) & Q(request_request__request_date__lt=date) &
                                               Q(request_product=product))
                last_req,requnit = turn_to_little_unit(r.request_amount,product,r.request_unit)
                
                
                if r.request_amount_sent:

                    last_req2, requnit = turn_to_little_unit(r.request_amount_sent, product, r.request_unit_sent)

                    last_req = last_req + last_req2 - last_req
                    
                
        except:
            last_req = 0
            requnit = ''

        #yesterday sales
        recipes = Recipe23.objects.filter(Q(recipe_parent_product__in=rel))
        foodSaleAmount = 0.0
        salesDesc = '<ul>'
        for r in recipes:
            try:
                s = FoodSaleProduct.objects.filter(Q(product=r.recipe_child_product)&
                                                Q(sale__date__gt=last_date)&
                                                Q(sale__date__lte=date)&
                                                Q(sale__branch=branch))
                recamount = 0
                for ss in s:
                    recamount += ss.amount
                if recamount > 0:
                    used,uunit = turn_to_little_unit(r.recipe_amount,product,r.recipe_unit)
                    if product.id == 180:
                        used = used * 1.35
#                    elif product.id == 132:
#                        used = used *1.4
                    else:
                        pass
                    foodSaleAmount += (used * recamount)
                    if uunit.id == 1:
                        used = used * 1000
                        uunit = 'گرم'
                    salesDesc = '%s <li>%i %s ( %i %s )</li>'%(salesDesc,recamount,s[0].product,used,uunit)
            except:
                return JsonResponse({'res': 'no2'})
#                pass

        salesDesc = '%s </ul>'%(salesDesc)
        #variances
        try:
            
            if len(rel) > 1:
                r = RequestProduct.objects.filter(Q(request_request__request_branch=branch) &
                                               Q(request_request__request_date__gte=last_date) & 
                                               Q(request_request__request_date__lt=date) & 
#                                                Q(request_request__request_date=last_day) & 
                                                  Q(request_product__in=rel))
                rpv = RequestProductVariance.objects.filter(Q(request_product__in=r)).aggregate(amount=Sum('request_amount_received'))
                var, varunit = turn_to_little_unit(rpv['amount'], product,
                                                r[0].request_unit)
            else:
                r = RequestProduct.objects.get(Q(request_request__request_branch=branch) &
                                               Q(request_request__request_date__gte=last_date) & 
                                               Q(request_request__request_date__lt=date)
                                               & Q(request_product=product))
                rpv = RequestProductVariance.objects.filter(Q(request_product=r)).last()
                

                var,varunit = turn_to_little_unit(rpv.request_amount_received,product,rpv.request_product.request_unit)
        except:
            
            var = None
            varunit = ''
            
#        if not var == None:
##            #estimation
#            estimation = last_pw+last_req-foodSaleAmount+(var-last_req)
#        else:
        estimation = last_pw + last_req - foodSaleAmount

        var_desc = ''
        if not var == None:
            if var < last_req:
                var_desc = '%.2f %s کم'%((last_req-var),varunit)
            else:
                var_desc = '%.2f %s زیاد' %((var-last_req),varunit)
        else:
            var_desc =''

        result.append({
            'product':rel_name,
            'real_amount':'%.2f %s'%(real_amount,wunit),
            'estimation':'%.2f %s'%(estimation,wunit),
            'difference':'%.2f %s'%((real_amount-estimation),wunit),
            'last_amount':'%.2f %s'%(last_pw,lpwunit),
            'request':'%.2f %s'%(last_req,requnit),
            'variance':var_desc,
            'sales':'%.2f %s'%(foodSaleAmount,wunit),
            'sales_desc':salesDesc,
        })


    template = loader.get_template('branchvar.html')
    return HttpResponse(template.render({'res':result,'branch':branch,'d':date.strftime('%Y/%m/%d')}, request))





def branchvarsum(request,id):

    if not request.user.is_authenticated:
        return redirect('../../../../admin/login/?next=/report/branchvar/%i'%id)
    if not request.user.has_perm('auth.can_see_report'):
        try:
            b = BranchWarehouse.objects.get(id=id).branch
            branch = Branch.objects.get(Q(branch_manager__manager_user=request.user)&Q(id=b.id))
        except:
            return redirect('../../../../admin/AmadoWHApp/branchwarehouse/')

    else:
        pass

#    def turn_to_little_unit(amount,product,unit):
#        if unit is None:
#            # using product default unit
#            if product.product_unit_ratio>1:
#                return amount * product.product_unit_ratio,product.product_second_unit
#            else:
#                return amount , product.product_unit
#
#        if unit == product.product_unit:
#            # using product big unit
#            if product.product_unit_ratio>1:
#                return amount * product.product_unit_ratio,product.product_second_unit
#            else:
#                return amount , product.product_unit
#        elif unit == product.product_second_unit:
#            # using product small unit
#            return amount, product.product_second_unit
#        else:
#            return None

    def turn_to_little_unit(amount,product,unit):
        
        if unit is None or unit == product.product_unit:
                # using product default unit
                if product.product_unit_ratio > 1:
                    return amount * product.product_unit_ratio, product.product_second_unit
                else:
                    return amount, product.product_unit
                
        if unit == product.product_second_unit:
            return amount, product.product_second_unit
        
        try:
            ratio = UnitToUnit.objects.get(product=product, first_unit=unit,second_unit=product.product_second_unit).ration

            return amount*ratio, product.product_second_unit

            # if unit == product.product_unit:
            #     # using product big unit
            #     if product.product_unit_ratio > 1:
            #         return amount * product.product_unit_ratio, product.product_second_unit
            #     else:
            #         return amount, product.product_unit
            # elif unit == product.product_second_unit:
            #     # using product small unit
            #     return amount, product.product_second_unit
            # else:
            #     return None
        except:
            return None


    result =[]

    bw = BranchWarehouse.objects.get(id=id)
    if bw.status != 'confirmed' and bw.status != 'byadmin' and not request.user.is_superuser:
        return redirect('../../../../admin/AmadoWHApp/branchwarehouse/')
    date = bw.date
    last_date = BranchWarehouse.objects.filter(Q(date__lt=date)&Q(branch=bw.branch) & Q(status='byadmin')).order_by('date').last().date
    branch = bw.branch
    
    
    related = [{'nkh': [19, 20, 21, 22]},{'ngh':[10,11,12,13]},{'del':[15,16,17]},{'fre':[208,209,210,211,212,213,214]},{'barb':[341,342,364,365]},{'ab':[226,227]}]

    for w in BranchWarehouseProduct.objects.filter(branch_warehouse=id):
        product = w.product
#        last_day = BranchWarehouse.objects.filter(status='byadmin').order_by('date').last().date
        
#        print(last_date,last_day)
        
        if product.id in related[1]['ngh']:
            rel = related[1]['ngh']
            rel_name = 'نوشابه قوطی'
        elif product.id in related[0]['nkh']:
            rel = related[0]['nkh']
            rel_name = 'نوشابه خانواده'
        elif product.id in related[2]['del']:
            rel = related[2]['del']
            rel_name = 'هی دی'
        elif product.id in related[3]['fre']:
            rel = related[3]['fre']
            rel_name = 'فرشی'
        elif product.id in related[4]['barb']:
            rel = related[4]['barb']
            rel_name = 'باربیکن'
        elif product.id in related[5]['ab']:
            rel = related[5]['ab']
            rel_name = 'آب معدنی'
        else:
            rel =[product.id]
            rel_name = product.product_name

        #today real
        real_amount,wunit = turn_to_little_unit(w.amount,product,product.product_second_unit)

        
        #last warehouse report
        
        try:
            pw = BranchWarehouseProduct.objects.get(Q(branch_warehouse__branch=branch)&Q(branch_warehouse__date=last_date)&Q(product=product))
            pwamount = pw.amount
            pwunit = pw.product.product_second_unit
        except:
            pwamount = 0
            pwunit = product.product_second_unit
            
        last_pw,lpwunit = turn_to_little_unit(pwamount,product,pwunit)    

        #last request
        
        try:
            if product.id in rel:
                r1 = RequestProduct.objects.filter(Q(request_request__request_branch=branch) &
                                               Q(request_request__request_date__gte=last_date) & Q(request_request__request_date__lt=date) &
                                                  Q(request_product__id__in=rel))
#                r2 = r1.filter().aggregate(amount=Sum('request_amount_sent'))
#                r3 = r1.filter().aggregate(
#                    amount=Sum(Case(When(request_amount_sent=None, then=F('request_amount')), default=0)))
#
##                print(r1[0].request_unit)
##                print(r1[0].request_unit_sent)
#
#                last_req2 = 0
#                last_req3 = 0
#                requnit = product.product_unit
#                if r2['amount']:
#                    last_req2, requnit = turn_to_little_unit(r2['amount'], product, r1[0].request_unit)


                r2 = r1.filter().values('request_unit_sent').annotate(amount=Sum('request_amount_sent'))

                r3 = r1.filter().aggregate(
                    amount=Sum(Case(When(request_amount_sent=None, then=F('request_amount')), default=0)))

                #                print(r1[0].request_unit)
                #                print(r1[0].request_unit_sent)

                last_req2 = 0
                last_req3 = 0
                requnit = product.product_unit

                for rr2 in r2:
                    if rr2['amount'] != None:

                        try:
                            xunit = Unit.objects.get(id=rr2['request_unit_sent'])
                        except:
                            xunit = None
                        x, requnit = turn_to_little_unit(rr2['amount'], product, xunit)

                        last_req2 += x

                if r3['amount']:
                    last_req3, requnit = turn_to_little_unit(r3['amount'], product, r1[0].request_unit)
    #                last_req3, requnit = turn_to_little_unit(r3['amount'], product, r1[0].request_unit)


                last_req = last_req3 + last_req2


            else:    
                r = RequestProduct.objects.get(Q(request_request__request_branch=branch)&
                                               Q(request_request__request_date__gte=last_date) & Q(request_request__request_date__lt=date) &
                                               Q(request_product=product))
                last_req,requnit = turn_to_little_unit(r.request_amount,product,r.request_unit)


                if r.request_amount_sent:

                    last_req2, requnit = turn_to_little_unit(r.request_amount_sent, product, r.request_unit_sent)

                    last_req = last_req + last_req2 - last_req
                    
                
        except:
            last_req = 0
            requnit = ''

        #yesterday sales
        recipes = Recipe23.objects.filter(Q(recipe_parent_product__in=rel))
        foodSaleAmount = 0.0
        salesDesc = '<ul>'
        for r in recipes:
            try:
                s = FoodSaleProduct.objects.filter(Q(product=r.recipe_child_product)&
                                                Q(sale__date__gt=last_date)&
                                                Q(sale__date__lte=date)&
                                                Q(sale__branch=branch))
                recamount = 0
#                for ss in s:
#                    recamount += ss.amount

                if product.id == 132:
                    for ss in s:
                        if ss.sale.date.strftime('%Y-%m-%d') <= '1397-11-14':
                            recamount += (ss.amount)*1.4
                        else:
                            recamount += ss.amount
                            
                else:
                    for ss in s:
                        recamount += ss.amount
                if recamount > 0:
                    used,uunit = turn_to_little_unit(r.recipe_amount,product,r.recipe_unit)
                    if product.id == 180:
                        used = used * 1.35
#                    elif product.id == 132:
#                        used = used *1.4
                    else:
                        pass
                    foodSaleAmount += (used * recamount)
                    if uunit.id == 1:
                        used = used * 1000
                        uunit = 'گرم'
                    salesDesc = '%s <li>%i %s ( %i %s )</li>'%(salesDesc,recamount,s[0].product,used,uunit)
            except:
                return JsonResponse({'res': 'no2'})
#                pass

        salesDesc = '%s </ul>'%(salesDesc)
        #variances
        try:
            
            if len(rel) > 1:
                r = RequestProduct.objects.filter(Q(request_request__request_branch=branch) &
                                               Q(request_request__request_date__gte=last_date) & 
                                               Q(request_request__request_date__lt=date) & 
#                                                Q(request_request__request_date=last_day) & 
                                                  Q(request_product__in=rel))
                rpv = RequestProductVariance.objects.filter(Q(request_product__in=r)).aggregate(amount=Sum('request_amount_received'))
                var, varunit = turn_to_little_unit(rpv['amount'], product,
                                                r[0].request_unit)
            else:
                r = RequestProduct.objects.get(Q(request_request__request_branch=branch) &
                                               Q(request_request__request_date__gte=last_date) & 
                                               Q(request_request__request_date__lt=date)
                                               & Q(request_product=product))
                rpv = RequestProductVariance.objects.filter(Q(request_product=r)).last()
                

                var,varunit = turn_to_little_unit(rpv.request_amount_received,product,rpv.request_product.request_unit)
        except:
            
            var = None
            varunit = ''
            
#        if not var == None:
##            #estimation
#            estimation = last_pw+last_req-foodSaleAmount+(var-last_req)
#        else:
        estimation = last_pw + last_req - foodSaleAmount

        var_desc = ''
        if not var == None:
            if var < last_req:
                var_desc = '%.2f %s کم'%((last_req-var),varunit)
            else:
                var_desc = '%.2f %s زیاد' %((var-last_req),varunit)
        else:
            var_desc =''

        result.append({
            'product':rel_name,
            'real_amount':'%.2f %s'%(real_amount,wunit),
            'estimation':'%.2f %s'%(estimation,wunit),
            'difference':'%.2f %s'%((real_amount-estimation),wunit),
            'last_amount':'%.2f %s'%(last_pw,lpwunit),
            'request':'%.2f %s'%(last_req,requnit),
            'variance':var_desc,
            'sales':'%.2f %s'%(foodSaleAmount,wunit),
            'sales_desc':salesDesc,
        })


    template = loader.get_template('branchvar.html')
    return HttpResponse(template.render({'res':result,'branch':branch,'d':date.strftime('%Y/%m/%d')}, request))



