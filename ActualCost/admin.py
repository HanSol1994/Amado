import copy
from django.contrib import admin
from ActualCost.models import *
from AmadoFinance.models import *
from django.contrib import messages
import jdatetime
from django import forms
from xlwt import Workbook as _WB_, Font, XFStyle, Borders, Alignment
from AmadoWH.mysite import site
from django.db.models import Q, Sum,F


class WasteProductAdmin(admin.ModelAdmin):
    autocomplete_fields =['product']
    search_fields = ['name']

class WasteDetailInline(admin.TabularInline):
    fields = ['product','amount','unit','fee','center']

    model=WasteSaleProduct
    extra = 1
    autocomplete_fields = ['product']

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            return list()

        if obj == None:
            return list()

        if request.user.has_perm('ActualCost.can_see_waste_sale'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        if obj.status == 'registered' or obj.status == 'rejected':
            if request.user.has_perm('ActualCost.can_change_status'):
                return list()
            else:
                return list()

        elif obj.status == 'confirmed':
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        else:#paid
            result = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result
            
class CurrencyFormCash(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CurrencyFormCash, self).__init__(*args, **kwargs)

    class Meta:
        exclude = ()
        model = CashPayment
        widgets = {
            'cost': forms.NumberInput(attrs={'step': 0, 'min': 0, 'size': '100', 'localization': True}),
        }            
            
class RecedeImageInline(admin.TabularInline):
    model = RecedeImage
    extra = 1
    form = CurrencyFormCash
    fields = ('image_title', 'cost','payment_due_date', 'image', 'factor_image')
    readonly_fields = ('factor_image',)
    
class WasteSaleAdmin(admin.ModelAdmin):
    inlines = [WasteDetailInline,RecedeImageInline]

    list_display = ['id','sale_date','buyer','status','sale_cost','recides','rem']

    def sale_cost(self,obj=None):


        ss = WasteSaleProduct.objects.filter(sale=obj).aggregate(s=Sum(F('fee')*F('amount')))

        return int(ss['s'])

    sale_cost.short_description = 'جمع کل (ریال)'


    def recides(self,obj=None):
        ss = RecedeImage.objects.filter(waste_sell=obj).aggregate(s=Sum('cost'))

        if ss['s']:
            return int(ss['s'])
        return '-'

    recides.short_description = 'جمع واریزی (ریال)'

    def rem(self,obj=None):
        ss1 = WasteSaleProduct.objects.filter(sale=obj).aggregate(s=Sum(F('fee') * F('amount')))
        if ss1['s']:
            ss1 = int(ss1['s'])
        else:
            ss1 = 0
        ss2 = RecedeImage.objects.filter(waste_sell=obj).aggregate(s=Sum('cost'))
        if ss2['s']:
            ss2 = int(ss2['s'])
        else:
            ss2 = 0



        return ss1-ss2

    rem.short_description = 'مانده واریزی (ریال)'

    fields = ['sale_date','buyer','payment_date','account','status','submit_user','submit_date','confirm_user','confirm_date']

    autocomplete_fields = ['buyer','account']

    def save_model(self, request, instance, form, change):
        user = request.user
        if not change:
            role = request.user.groups.all()[0].name
            if role != 'admin':
                instance.submit_user = request.user
                instance.status = 'registered'

        instance = form.save(commit=False)

        instance.save()

        return instance

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            return list()

        if obj == None:
            return list(['submit_user', 'submit_date', 'confirm_user', 'confirm_date','status'])

        if request.user.has_perm('ActualCost.can_see_waste_sale'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        if obj.status == 'registered' or obj.status == 'rejected':
            if request.user.has_perm('ActualCost.can_change_status'):
                return list(['submit_user', 'submit_date', 'confirm_user', 'confirm_date'])
            else:
                return list(['submit_user', 'submit_date', 'confirm_user', 'confirm_date', 'status'])

        elif obj.status == 'confirmed':
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            if request.user.has_perm('ActualCost.can_change_status'):
                result.remove('status')
            return result

        else:#paid
            result = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

    def confirm(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('ActualCost.can_confirm_sell_waste'):
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
            self.message_user(request, "%i فروش تایید شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان تایید برخی یا همه فروش ها وجود ندارد")

    confirm.short_description = 'تایید فروش های انتخاب شده'

    def decline(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('ActualCost.can_confirm_sell_waste'):
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
            self.message_user(request, "%i فروش رد شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان رد برخی یا همه فروش ها وجود ندارد")

    decline.short_description = 'رد پرداخت های انتخاب شده'

    def pay(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('ActualCost.can_pay_sell_waste'):
            messages.error(request, "شما اجازه پرداخت فروش را ندارید")
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
            messages.error(request, "امکان پرداخت برخی یا همه فروش ها وجود ندارد")

    pay.short_description = 'پرداخت فروش های انتخاب شده'
    
    def export_xls(modeladmin, request, queryset):
        import xlwt
        from django.http import HttpResponse, JsonResponse

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=factor.xls'
        wb = xlwt.Workbook(encoding='utf-8')

        for sale in queryset:
            buyer = sale.buyer

            ws = wb.add_sheet("فاکتور")

            ws.cols_right_to_left = 1


            today = jdatetime.datetime.today().strftime('%Y/%m/%d')

            row_num = 0

            columns = [
                (u"ردیف", 1500),
                (u"شرح", 7000),
                (u"تعداد", 3500),
                (u"فی واحد (ریال)", 8000),
                (u"قیمت کل (ریال)", 8000),
            ]

            header_style = xlwt.XFStyle()
            header_style.num_format_str = '#,##0'
            header_style.font.height = 200

            al = Alignment()
            al.horz = Alignment.HORZ_CENTER
            al.vert = Alignment.VERT_CENTER
            header_style.alignment = al

            borders = xlwt.Borders()
            borders.left = 0
            borders.right = 0
            borders.top = 0
            borders.bottom = 0
            borders.left_colour = 0x00
            borders.right_colour = 0x00
            borders.top_colour = 0x00
            borders.bottom_colour = 0x00

            header_style.borders = borders

            ws.row(0).height_mismatch = True
            ws.row(0).height = 40 * 10
            ws.row(1).height_mismatch = True
            ws.row(1).height = 40 * 10

            ws.row(2).height_mismatch = True
            ws.row(2).height = 70 * 10

            ws.col(0).width = columns[0][1]
            ws.col(1).width = columns[1][1]
            ws.col(2).width = columns[2][1]
            ws.col(3).width = columns[3][1]
            ws.col(4).width = columns[4][1]



            ws.write_merge(0, 0, 0, 4, 'فاکتور فروش فست فود آمادو' , header_style)

            ws.write(1,1, 'صورت حساب: %s'%(buyer), header_style)
            ws.write_merge(1, 1, 2, 3, 'توسط: %s'%request.user, header_style)
            ws.write(1, 4, 'تاریخ: %s' % (today), header_style)

            header_style = xlwt.XFStyle()
            header_style.font.bold = True
            header_style.font.height = 400

            header_style2 = xlwt.XFStyle()
            header_style2.font.height = 250

            al = Alignment()
            al.horz = Alignment.HORZ_CENTER
            al.vert = Alignment.VERT_CENTER
            header_style.alignment = al
            header_style2.alignment = al

            borders2 = xlwt.Borders()
            borders2.left = 1
            borders2.right = 1
            borders2.top = 1
            borders2.bottom = 1

            header_style.borders = borders2
            header_style2.borders = borders2

            header_style2.font.colour_index = xlwt.Style.colour_map['white']
            header_style.font.colour_index = xlwt.Style.colour_map['white']


            pattern = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = 63
            header_style2.pattern = pattern
            header_style.pattern = pattern


            ws.write(2,0,'ردیف',header_style2)
            ws.write(2,1,'شرح',header_style)
            ws.write(2,2,'تعداد',header_style)
            ws.write(2,3,'فی واحد(ریال)',header_style)
            ws.write(2,4,'قیمت کل(ریال)',header_style)



            simple_style  = xlwt.XFStyle()
            simple_style.font.height = 270
            simple_style.borders = borders2
            simple_style.num_format_str = '#,##0'
            simple_style.alignment = al

            row_num = 3

            sum = 0

            for product in WasteSaleProduct.objects.filter(sale=sale):
                ws.row(row_num).height_mismatch = True
                ws.row(row_num).height = 50 * 10

                ws.write(row_num,0,row_num-2,simple_style)
                ws.write(row_num,1,product.product.name,simple_style)
                ws.write(row_num,2,product.amount,simple_style)
                ws.write(row_num,3,product.fee,simple_style)
                ws.write(row_num,4,product.fee*product.amount,simple_style)

                sum += (product.fee*product.amount)

                row_num += 1

            simple_style.font.height = 270
            simple_style.num_format_str = '#,##0'

            al.horz = Alignment.HORZ_CENTER
            al.vert = Alignment.VERT_CENTER

            simple_style.alignment = al

            def wordifyfa(num, level):

                if not num:
                    return ""

                if num < 0:
                    num = num * -1;
                    return "منفی " + wordifyfa(num, level);

                if num == 0:
                    if level == 0:
                        return "صفر";
                    else:
                        return "";

                result = ""
                yekan = [" یک ", " دو ", " سه ", " چهار ", " پنج ", " شش ", " هفت ", " هشت ", " نه "]
                dahgan = [" بیست ", " سی ", " چهل ", " پنجاه ", " شصت ", " هفتاد ", " هشتاد ", " نود "]
                sadgan = [" یکصد ", " دویست ", " سیصد ", " چهارصد ", " پانصد ", " ششصد ", " هفتصد ", " هشتصد ",
                          " نهصد "]
                dah = [" ده ", " یازده ", " دوازده ", " سیزده ", " چهارده ", " پانزده ", " شانزده ", " هفده ",
                       " هیجده ",
                       " نوزده "];

                if level > 0:
                    result += " و ";
                    level -= 1;

                if num < 10:
                    result += yekan[num - 1];
                elif num < 20:
                    result += dah[num - 10];
                elif num < 100:
                    result += dahgan[int(num / 10) - 2] + wordifyfa(num % 10, level + 1);
                elif num < 1000:
                    result += sadgan[int(num / 100) - 1] + wordifyfa(num % 100, level + 1);
                elif num < 1000000:
                    result += wordifyfa(int(num / 1000), level) + " هزار " + wordifyfa(num % 1000, level + 1);
                elif num < 1000000000:
                    result += wordifyfa(int(num / 1000000), level) + " میلیون " + wordifyfa(num % 1000000,
                                                                                                      level + 1);
                elif num < 1000000000000:
                    result += wordifyfa(int(num / 1000000000), level) + " میلیارد " + wordifyfa(
                        num % 1000000000,
                        level + 1);
                elif num < 1000000000000000:
                    result += wordifyfa(int(num / 1000000000000), level) + " تریلیارد " + wordifyfa(
                        num % 1000000000000, level + 1);

                return result;

            borders3 = copy.deepcopy(borders2)
            borders3.left = 0
            borders3.right = 0
            borders3.bottom = 0
            simple_style.borders = borders3

            ws.write(row_num, 4, xlwt.Formula('SUM(E4:E%i)' % (row_num)), simple_style)

            al2 = copy.deepcopy(al)
            al2.horz = Alignment.HORZ_LEFT
            al2.vert = Alignment.VERT_CENTER



            simple_style.alignment = al2





            ws.write_merge(row_num,row_num,1,2,'مبلغ به حروف: %s ریال'%(wordifyfa(sum,0)),simple_style)
            ws.write(row_num, 3, 'مبلغ کل:', simple_style)





        wb.save(response)
        return response

    export_xls.short_description = u"پرینت فاکتور"

    actions =['confirm','pay','export_xls']

    
class WasteSaleProductAdmin(admin.ModelAdmin):
    list_display = ['id','product','amount','fee','unit','center','sale']
    
class DetailActualCostAdmin(admin.ModelAdmin):
    list_display = ['id','actual_cost','parameter','title','effect','is_active']
    list_filter = ['parameter']
    search_fields = ['actual_cost__product__product_name', 'actual_cost__food__name']
    
    
    def deactivate(modeladmin, request, queryset):

        for obj in queryset:
            ac = obj.actual_cost
            ac.price = ac.price - obj.effect
            ac.save()
            obj.is_active = False
            obj.save()
            
    def activate(modeladmin, request, queryset):

        for obj in queryset:
            ac = obj.actual_cost
            ac.price = ac.price + obj.effect
            ac.save()
            obj.is_active = True
            obj.save()

    deactivate.short_description = 'غیرفعال کردن'
    activate.short_description = 'فعال کردن'

    actions = ['deactivate','activate']


    def save_model(self, request, instance, form, change):
        if change:
            old = DetailActualCost.objects.get(id=instance.id)
            if old.effect != instance.effect:
                diff = old.effect-instance.effect
                ac = instance.actual_cost
                ac.price = ac.price - diff
                ac.save()
            elif old.is_active == True and instance.is_active == False:
                    ac = instance.actual_cost
                    ac.price = ac.price - instance.effect
                    ac.save()
            elif old.is_active == False and instance.is_active == True:
                ac = instance.actual_cost
                ac.price = ac.price + instance.effect
                ac.save()
            else:
                pass
        else:
            ac = instance.actual_cost
            ac.price = ac.price + instance.effect 
            ac.save()


        instance = form.save(commit=False)

        instance.save()
        form.save_m2m()
        return instance
    
class DACInline(admin.TabularInline):
    model=DetailActualCost
    extra = 1
    
    

class ActualCostAdmin(admin.ModelAdmin):
    list_display = ['id','__str__','price','unit','date']
    search_fields = ['product__product_name', 'food__name']
    inlines = [DACInline]
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if change:
                old = DetailActualCost.objects.get(id=instance.id)
                if old.effect != instance.effect:
                    diff = old.effect-instance.effect
                    ac = instance.actual_cost
                    ac.price = ac.price - diff
                    ac.save()
                elif old.is_active == True and instance.is_active == False:
                    ac = instance.actual_cost
                    ac.price = ac.price - instance.effect
                    ac.save()
                elif old.is_active == False and instance.is_active == True:
                    ac = instance.actual_cost
                    ac.price = ac.price + instance.effect
                    ac.save()
                else:
                    pass
            else:
                ac = instance.actual_cost
                ac.price = ac.price + instance.effect
                ac.save()
            instance.save()
            
            
        formset.save_m2m()
    
site.register(WasteProduct,WasteProductAdmin)
site.register(WasteSale,WasteSaleAdmin)
site.register(WasteSaleProduct,WasteSaleProductAdmin)
site.register(Cost)
site.register(Property)
site.register(OverAccount)
site.register(DefinitiveAccount)
site.register(ActualCost,ActualCostAdmin)
site.register(DetailActualCost,DetailActualCostAdmin)
site.register(Parameter)