from unittest import loader
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Q, Count, Case, When, F

from ActualCost.models import *
from AmadoWHApp.models import *
from AmadoAccounting.models import *
from AmadoFinance.models import *

@csrf_exempt
def calc_ac_l2(request):
    ids = request.POST['ids']#text TODO
    ids = ids.split(',')
    ids = list(map(int, ids))

    from_date = request.POST['from_date']
    to_date = request.POST['to_date']

    def get_cost_share(amount,parent_recipe_unit,shop_unit,last_price,parent):
        pass
        if parent_recipe_unit == shop_unit:
            return amount*last_price
        else:
            try:
                u = UnitToUnit.objects.get((Q(raw_product=parent)&Q(first_unit=parent_recipe_unit)&Q(second_unit=shop_unit)))
                price = last_price * u.ration
            except:
                try:
                    u = UnitToUnit.objects.get(((Q(raw_product=parent)&Q(second_unit=parent_recipe_unit)&Q(first_unit=shop_unit))))
                    price = last_price / u.ration
                except:
                    return JsonResponse({'res':parent.product_name,'u1':parent_recipe_unit.unit_name,'u2':shop_unit.unit_name})
                

            return price * amount


    def get_product_count(product):
        r = RequestProduct.objects.filter(Q(request_request__request_date__lte=to_date)&Q(request_request__request_date__gte=from_date)&
                                      Q(request_product=product)).values('request_unit','request_unit_sent')\
            .annotate(sum=Sum('request_amount'),sum2=Sum('request_amount_sent'))

        count = 0

        r1 = r.filter(~Q(request_unit_sent=None)&~Q(request_amount_sent=None))# sent amount & sent unit
        r2 = r.filter(Q(request_unit_sent=None)&~Q(request_amount_sent=None))# sent amount & product unit
        r3 = r.filter(Q(request_unit_sent=None)&Q(request_unit=None))# req amount and product unit
        r4 = r.filter(Q(request_unit_sent=None)&~Q(request_unit=None))# req amount and req unit

        try:
            count += r2[0]['sum2'] * product.product_unit_ratio
        except:
            count += 0

        try:
            count += r3[0]['sum'] * product.product_unit_ratio
        except:
            count += 0



        for rr in r1:
            if rr['request_unit_sent'] == product.product_second_unit.id:
                count += rr['sum2']
            elif rr['request_unit_sent'] == product.product_unit.id:
                count += rr['sum2']*product.product_unit_ratio
            else:
                try:
                    u = UnitToUnit.objects.get(
                        (Q(product=product) & Q(first_unit=rr['request_unit_sent']) & Q(second_unit=product.product_second_unit)))
                    count += rr['sum2'] * u.ration
                except:
                    u = UnitToUnit.objects.get(
                        (Q(product=product) & Q(first_unit__id=rr['request_unit_sent']) & Q(
                            second_unit=product.product_second_unit)))
                    count += rr['sum2'] / u.ration

        for rr in r4:
            if rr['request_unit'] == product.product_second_unit.id:
                count += rr['sum']
            elif rr['request_unit'] == product.product_unit.id:
                count += rr['sum'] * product.product_unit_ratio
            else:
                try:
                    u = UnitToUnit.objects.get(
                        (Q(product=product) & Q(first_unit__id=rr['request_unit']) & Q(
                            second_unit=product.product_second_unit)))
                    count += rr['sum'] * u.ration
                except:
                    u = UnitToUnit.objects.get(
                        (Q(product=product) & Q(first_unit__id=rr['request_unit']) & Q(
                            second_unit=product.product_second_unit)))
                    count += rr['sum'] / u.ration



        # turn_to_second_unit(r)

        # print(r)
        return count,product.product_second_unit


    json = []
    
    for p in Product.objects.filter(id__in=ids):
        # Parent

        # returns based on second unit, because requests might be based on that
        
        DetailActualCost.objects.filter(actual_cost__product=p).delete()
        
        tot_count,tot_unit = get_product_count(p)
        if tot_count == 0:
            continue


            
        # indirect costs should be divided by kinds of products eff = (indCost/count)/tot_count => eff = indCost/(tot_count*count)
        tot_count = tot_count*(Recipe12.objects.all().values('recipe_child_product').distinct().count())    
            
        ac = ActualCost(product=p, unit=tot_unit, price=0,from_date=from_date,to_date=to_date)
        ac.save()
        

        pp = Parameter.objects.get(id=1).parameter_is_active
#        sp = Parameter.objects.get(id=2).parameter_is_active
#        rp = Parameter.objects.get(id=3).parameter_is_active
#        bp = Parameter.objects.get(id=4).parameter_is_active
#        np = Parameter.objects.get(id=5).parameter_is_active
#        op = Parameter.objects.get(id=6).parameter_is_active


        pWeight = 0
        if pp:
            # Recipe is based on first unit price will be based on second unit
            for r in Recipe12.objects.filter(recipe_child_product=p):
                parent = r.recipe_parent_product
                amount = r.recipe_amount
                parent_recipe_unit = r.recipe_unit

                last_shop = ShopDetail.objects.filter(Q(last_price__gt=0)&Q(product=parent) & Q(shop__from_date__lte=to_date)).order_by(
                    'shop__from_date').last()
                try:
                    last_price = last_shop.last_price
                    shop_unit = last_shop.unit
                    x = get_cost_share(amount, parent_recipe_unit, shop_unit, last_price, parent)
                except:
                    last_price = 0
                    shop_unit = None
                    x = 0

                # x = int(x/p.product_unit_ratio)

                try:
                    # pWeight += int(x/p.product_unit_ratio)
                    pWeight += x
                except:
                    ac.delete()
                    return x
                dac1 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=1), effect=x,
                                        title=parent.product_name)
                dac1.save()
            # pWeight = int(pWeight)  # turn to tot_unit(second unit)

            
#        sWeight = 0
#        if sp:
#            # Salary only amade sazi
#            sal_sum = SalaryDetail.objects.filter(
#                Q(salary__branch=8) & Q(payment_status='paid') & Q(salary__month__gte=from_date) & Q(
#                    salary__month__lte=to_date)).aggregate(sum=Sum('pardakhti'))['sum'] or 0
#            sWeight = sal_sum / tot_count
#            dac2 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=2), effect=sWeight)
#            dac2.save()
#
#            
#        rWeight = 0
#        if rp:
#            # Repairs only amade sazi
#            rWeight = RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
#                                                 Q(factor__payment_due_date__gte=from_date) &
#                                                 Q(payment_due_date__lte=to_date) &
#                                                 Q(payment_due_date__gte=from_date) &
#                                                 (Q(def_account=8) | Q(factor__cost_center=6)) &
#                                                 Q(factor__over_account=21)).aggregate(sum=Sum('cost'))['sum'] or 0
#
#            rWeight += CheckPayment.objects.filter(Q(check_due_date__lte=to_date) &
#                                                   Q(check_due_date__lte=from_date) &
#                                                   (Q(cost_center=6) &
#                                                    (Q(check_payment_type=8) | Q(over_account=21)))).aggregate(
#                sum=Sum('payment_cost'))['sum'] or 0
#            rWeight = rWeight / tot_count
#            dac3 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=3), effect=rWeight)
#            dac3.save()
#
#            
#        bWeight = 0
#        if bp:
#            # Bills
#            bWeight = RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
#                                                 Q(factor__payment_due_date__gte=from_date) &
#                                                 Q(payment_due_date__lte=to_date) &
#                                                 Q(payment_due_date__gte=from_date) &
#                                                 (Q(def_account=8) | Q(factor__cost_center=6)) &
#                                                 (Q(factor__over_account=10) | Q(factor__over_account=11) | Q(
#                                                     factor__over_account=12) | Q(factor__over_account=16))).aggregate(
#                sum=Sum('cost'))['sum'] or 0
#
#            bWeight = bWeight / tot_count
#            dac4 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=4), effect=bWeight)
#            dac4.save()
#
#            
#        nWeight = 0
#        if np:
#            # Rents
#            nWeight = RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
#                                                 Q(factor__payment_due_date__gte=from_date) &
#                                                 Q(payment_due_date__lte=to_date) &
#                                                 Q(payment_due_date__gte=from_date) &
#                                                 (Q(def_account=8) | Q(factor__cost_center=6)) &
#                                                 (Q(factor__over_account=3) | Q(factor__over_account=4))).aggregate(
#                sum=Sum('cost'))['sum'] or 0
#
#            nWeight += CheckPayment.objects.filter(Q(check_due_date__lte=to_date) &
#                                                   Q(check_due_date__lte=from_date) &
#                                                   (Q(cost_center=6) &
#                                                    (Q(check_payment_type=7) | Q(over_account=3) | Q(
#                                                        over_account=4)))).aggregate(
#                sum=Sum('payment_cost'))['sum'] or 0
#            nWeight = nWeight / tot_count
#            dac5 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=5), effect=nWeight)
#            dac5.save()
#
#            # print(sWeight+rWeight+bWeight+nWeight,tot_unit)
#
#            
#        oWeight = 0
#        if op:
#            # Other Costs
#            oWeight = RecedeImage.objects.filter(Q(fund__payment_due_date__lte=to_date) &
#                                                 Q(fund__payment_due_date__gte=from_date) &
#                                                 Q(payment_due_date__lte=to_date) &
#                                                 Q(payment_due_date__gte=from_date) &
#                                                 (Q(def_account=8) | Q(fund__cost_center=6))).aggregate(sum=Sum('cost'))[
#                          'sum'] or 0
#            oWeight += RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
#                                                  Q(factor__payment_due_date__gte=from_date) &
#                                                  Q(payment_due_date__lte=to_date) &
#                                                  Q(payment_due_date__gte=from_date) &
#                                                  (Q(def_account=8) | Q(fund__cost_center=6)) &
#                                                  (Q(factor__over_account=2) | Q(factor__over_account=5) | Q(
#                                                      factor__over_account=13) | Q(factor__over_account=14))).aggregate(
#                sum=Sum('cost'))['sum'] or 0
#
#            oWeight += CheckPayment.objects.filter(Q(check_due_date__lte=to_date) &
#                                                   Q(check_due_date__lte=from_date) &
#                                                   (Q(cost_center=6) &
#                                                    (Q(check_payment_type=3) | Q(over_account=3) | Q(over_account=13) | Q(
#                                                        over_account=14) | Q(over_account=17)))).aggregate(
#                sum=Sum('payment_cost'))['sum'] or 0
#
#            # Over Head Products
#
#            oWeight = oWeight / tot_count
#            dac6 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=6), effect=oWeight)
#            dac6.save()
#
#
#            
#        tot_price = pWeight + sWeight + rWeight + bWeight + nWeight + oWeight
        tot_price = pWeight
        ac.price = tot_price
        ac.save()
    
        json.append({'product':p.product_name,'res':int(pWeight),'unit':tot_unit.unit_name})


    return JsonResponse({'res':json})

@csrf_exempt
def calc_ac_l3(request):
    ids = request.POST['ids']#text TODO

    ids = ids.split(',')
    ids = list(map(int, ids))

    from_date = request.POST['from_date']
    to_date = request.POST['to_date']

    def get_cost_share(amount,parent_recipe_unit,price_unit,last_price,parent):
        pass
        if parent_recipe_unit == price_unit:
            return amount*last_price
        else:
            try:
                u = UnitToUnit.objects.get((Q(product=parent)&Q(first_unit=parent_recipe_unit)&Q(second_unit=price_unit)))
                price = last_price * u.ration
            except:
                try:
                    u = UnitToUnit.objects.get(((Q(product=parent)&Q(second_unit=parent_recipe_unit)&Q(first_unit=price_unit))))
                    price = last_price * u.ration
                except:
                
                    return JsonResponse({'res':parent.product_name,'u1':parent_recipe_unit.unit_name,'u2':price_unit.unit_name})

            return price * amount


    def turn_to_second_unit(requests):

        # requests.filter

        return 0

    def get_product_count(product):
        r = RequestProduct.objects.filter(Q(request_request__request_date__lte=to_date)&Q(request_request__request_date__gte=from_date)&
                                      Q(request_product=product)).values('request_unit','request_unit_sent')\
            .annotate(sum=Sum('request_amount'),sum2=Sum('request_amount_sent'))

        count = 0

        r1 = r.filter(~Q(request_unit_sent=None)&~Q(request_amount_sent=None))# sent amount & sent unit
        r2 = r.filter(Q(request_unit_sent=None)&~Q(request_amount_sent=None))# sent amount & product unit
        r3 = r.filter(Q(request_unit_sent=None)&Q(request_unit=None))# req amount and product unit
        r4 = r.filter(Q(request_unit_sent=None)&~Q(request_unit=None))# req amount and req unit

        try:
            count += r2[0]['sum2'] * product.product_unit_ratio
        except:
            count += 0

        try:
            count += r3[0]['sum'] * product.product_unit_ratio
        except:
            count += 0



        for rr in r1:
            if rr['request_unit_sent'] == product.product_second_unit.id:
                count += rr['sum2']
            elif rr['request_unit_sent'] == product.product_unit.id:
                count += rr['sum2']*product.product_unit_ratio
            else:
                try:
                    u = UnitToUnit.objects.get(
                        (Q(product=product) & Q(first_unit=rr['request_unit_sent']) & Q(second_unit=product.product_second_unit)))
                    count += rr['sum2'] * u.ration
                except:
                    u = UnitToUnit.objects.get(
                        (Q(product=product) & Q(first_unit__id=rr['request_unit_sent']) & Q(
                            second_unit=product.product_second_unit)))
                    count += rr['sum2'] / u.ration

        for rr in r4:
            if rr['request_unit'] == product.product_second_unit.id:
                count += rr['sum']
            elif rr['request_unit'] == product.product_unit.id:
                count += rr['sum'] * product.product_unit_ratio
            else:
                try:
                    u = UnitToUnit.objects.get(
                        (Q(product=product) & Q(first_unit__id=rr['request_unit']) & Q(
                            second_unit=product.product_second_unit)))
                    count += rr['sum'] * u.ration
                except:
                    u = UnitToUnit.objects.get(
                        (Q(product=product) & Q(first_unit__id=rr['request_unit']) & Q(
                            second_unit=product.product_second_unit)))
                    count += rr['sum'] / u.ration



        # turn_to_second_unit(r)

        # print(r)
        return count,product.product_second_unit.unit_name


    for p in AmadoFood.objects.filter(id__in=ids):
        # Parent

        tot_count = FoodSaleProduct.objects.filter(Q(sale__date__lte=to_date)&Q(sale__date__gte=from_date)).aggregate(sum=Sum('amount'))['sum'] or 0
        # print(tot_count)
        
        ac = ActualCost(food=p, unit=Unit.objects.get(id=5))
        ac.save()



        pp = Parameter.objects.get(id=1).parameter_is_active
        sp = Parameter.objects.get(id=2).parameter_is_active
        rp = Parameter.objects.get(id=3).parameter_is_active
        bp = Parameter.objects.get(id=4).parameter_is_active
        np = Parameter.objects.get(id=5).parameter_is_active
        op = Parameter.objects.get(id=6).parameter_is_active
        hp = Parameter.objects.get(id=7).parameter_is_active

        pWeight = 0
        if pp:
            for r in Recipe23.objects.filter(recipe_child_product=p):
                parent = r.recipe_parent_product
                amount = r.recipe_amount
                parent_recipe_unit = r.recipe_unit

                last = ActualCost.objects.filter(product=parent).order_by('date').last()  # TODO
                if last == None:
                    x = 0
                else:
                    price_unit = last.unit
                    last_price = last.price
                    x = get_cost_share(amount, parent_recipe_unit, price_unit, last_price, parent)

                # print(parent.product_name)
                # print(x)
                # print('///////////////')
                pWeight += x
                dac1 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=1), effect=x,
                                        title=parent.product_name)
                dac1.save()

            pWeight = int(pWeight)

        sWeight = 0
        
        if sp:
            # Salary only amade sazi
            sal_sum = SalaryDetail.objects.filter(
                Q(payment_status='paid') & Q(salary__month__gte=from_date) & Q(
                    salary__month__lte=to_date)).aggregate(sum=Sum('pardakhti'))['sum'] or 0
            sWeight = sal_sum / tot_count
            dac2 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=2), effect=sWeight)
            dac2.save()

        rWeight = 0
        if rp:
            # Repairs only amade sazi
            rWeight = RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
                                                 Q(factor__payment_due_date__gte=from_date) &
                                                 Q(payment_due_date__lte=to_date) &
                                                 Q(payment_due_date__gte=from_date) &
#                                                 ~(Q(def_account=8) | Q(factor__cost_center=6)) &
                                                 Q(factor__over_account=21)).aggregate(sum=Sum('cost'))['sum'] or 0

            rWeight += CheckPayment.objects.filter(Q(check_due_date__lte=to_date) &
                                                   Q(check_due_date__lte=from_date) &
                                                   (
#                                                       ~Q(cost_center=6)&
                                                    (Q(check_payment_type=8) | Q(over_account=21)))
                                                  ).aggregate(
                sum=Sum('payment_cost'))['sum'] or 0
            rWeight = rWeight / tot_count
            dac3 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=3), effect=rWeight)
            dac3.save()


        bWeight = 0
        if bp:
            # Bills
            bWeight = RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
                                                 Q(factor__payment_due_date__gte=from_date) &
                                                 Q(payment_due_date__lte=to_date) &
                                                 Q(payment_due_date__gte=from_date) &
#                                                 ~(Q(def_account=8) | Q(factor__cost_center=6)) &
                                                 (Q(factor__over_account=10) | Q(factor__over_account=11) | Q(
                                                     factor__over_account=12) | Q(factor__over_account=16))).aggregate(
                sum=Sum('cost'))['sum'] or 0

            bWeight = bWeight / tot_count
            dac4 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=4), effect=bWeight)
            dac4.save()

        nWeight = 0
        if np:
            # Rents
            nWeight = RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
                                                 Q(factor__payment_due_date__gte=from_date) &
                                                 Q(payment_due_date__lte=to_date) &
                                                 Q(payment_due_date__gte=from_date) &
#                                                 ~(Q(def_account=8) | Q(factor__cost_center=6)) &
                                                 (Q(factor__over_account=3) | Q(factor__over_account=4))).aggregate(
                sum=Sum('cost'))['sum'] or 0
            nWeight += CheckPayment.objects.filter(Q(check_due_date__lte=to_date) &
                                                   Q(check_due_date__gte=from_date) &
                                                   ~Q(check_bank=None) &
                                                   (
#                                                       ~Q(cost_center=6) &
                                                    (Q(check_payment_type=7) | Q(over_account=3) | Q(
                                                        over_account=4)))).aggregate(
                sum=Sum('payment_cost'))['sum'] or 0
            nWeight = nWeight / tot_count
            dac5 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=5), effect=nWeight)
            dac5.save()

            # print(sWeight+rWeight+bWeight+nWeight,tot_unit)


        oWeight = 0
        if op:
            # Other Costs
            oWeight = RecedeImage.objects.filter(Q(fund__payment_due_date__lte=to_date) &
                                                 Q(fund__payment_due_date__gte=from_date) &
                                                 Q(payment_due_date__lte=to_date) &
                                                 Q(payment_due_date__gte=from_date)
#                                                 &
#                                                 ~(Q(def_account=8) | Q(fund__cost_center=6))
                                                ).aggregate(sum=Sum('cost'))[
                          'sum'] or 0

            oWeight += RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
                                                  Q(factor__payment_due_date__gte=from_date) &
                                                  Q(payment_due_date__lte=to_date) &
                                                  Q(payment_due_date__gte=from_date) &
#                                                  ~(Q(def_account=8) | Q(factor__cost_center=6)) &
                                                  (Q(factor__over_account=2) | Q(factor__over_account=5) | Q(
                                                      factor__over_account=13) | Q(factor__over_account=14))).aggregate(
                sum=Sum('cost'))['sum'] or 0

            oWeight += CheckPayment.objects.filter(Q(check_due_date__lte=to_date) &
                                                   Q(check_due_date__gte=from_date) &
                                                   (
#                                                       ~Q(cost_center=6) &
                                                    (Q(check_payment_type=3) | Q(over_account=13) | Q(
                                                        over_account=14)))).aggregate(
                sum=Sum('payment_cost'))['sum'] or 0

            oWeight = oWeight / tot_count
            dac6 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=6), effect=oWeight)
            dac6.save()

        # Over Head Products

        hWeight = 0
        if hp:
            hWeight = RecedeImage.objects.filter(Q(factor__payment_due_date__lte=to_date) &
                                                 Q(factor__payment_due_date__gte=from_date) &
                                                 Q(payment_due_date__lte=to_date) &
                                                 Q(payment_due_date__gte=from_date) &
                                                 (Q(factor__over_account=24))).aggregate(
                sum=Sum('cost'))['sum'] or 0

            hWeight += CheckPayment.objects.filter(Q(check_due_date__lte=to_date) &
                                                   Q(check_due_date__gte=from_date) &
                                                   (
                                                       (Q(check_payment_type=6) | Q(over_account=24)))).aggregate(
                sum=Sum('payment_cost'))['sum'] or 0

            hWeight = hWeight / tot_count
            dac7 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=7), effect=oWeight)
            dac7.save()

        tot_price = pWeight+sWeight+rWeight+bWeight+nWeight+oWeight+hWeight
        ac.price = tot_price
        ac.save()
        
        
#        dac2 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=2), effect=sWeight)
#        dac2.save()
#
#        dac3 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=3), effect=rWeight)
#        dac3.save()
#
#        dac4 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=4), effect=bWeight)
#        dac4.save()
#
#        dac5 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=5), effect=nWeight)
#        dac5.save()
#
#        dac6 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=6), effect=oWeight)
#        dac6.save()
#
#        dac7 = DetailActualCost(actual_cost=ac, parameter=Parameter.objects.get(id=7), effect=oWeight)
#        dac7.save()

    return JsonResponse({'res':int(pWeight+sWeight+rWeight+bWeight+nWeight+oWeight+hWeight),'unit':'عدد'})

def calch(request):
    products = Recipe23.objects.filter(recipe_parent_product__product_is_active=True).values('recipe_parent_product', 'recipe_parent_product__product_name').order_by(
        'recipe_parent_product__product_name').distinct()
    foods = AmadoFood.objects.filter(Q(current_price__gt=0)&Q(product_is_active=True)).order_by('name')
    template = loader.get_template('home.html')
    return HttpResponse(template.render({'products':list(products),'foods':list(foods)}, request))