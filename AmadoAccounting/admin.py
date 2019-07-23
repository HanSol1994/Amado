from django.contrib import admin
import jdatetime
from django.contrib import messages
from AmadoAccounting.models import *
from AmadoWHApp.models import Branch
from django.db.models import Q,Sum,Count
from django.http import HttpResponse, JsonResponse
from django_jalali.admin.filters import JDateFieldListFilter
import xlwt 
from xlwt import Workbook as _WB_, Font, XFStyle, Borders, Alignment, Formula
import datetime
import copy
from django.utils.safestring import mark_safe
from django import forms
import xlsxwriter
from io import BytesIO
from django.http import StreamingHttpResponse
from django.contrib.admin.views.main import ChangeList
from AmadoFinance.models import RecedeImage
import jdatetime

class DetailInline(admin.TabularInline):
    model = SalaryDetail
    extra = 1
    exclude = ['add_user', 'confirm_user', 'add_date', 'confirm_date']

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
               return queryset.filter(Q(salary__month__gte=('%i%s01') % (this_year, month)) & Q(
                   salary__month__lte=('%i%s31') % (this_year, month)))
           except:
               try:
                   return queryset.filter(Q(salary__month__gte=('%i%s01') % (this_year, month)) & Q(
                       salary__month__lte=('%i%s30') % (this_year, month)))
               except:
                   return queryset.filter(Q(salary__month__gte=('%i%s01') % (this_year, month)) & Q(
                       salary__month__lte=('%i%s29') % (this_year, month)))
        else:
            r = queryset

        return queryset

    
    
class SalaryDFilter(admin.SimpleListFilter):
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
            ('registered', 'ثبت شده/در انتظار تایید'),
            ('confirmed', 'تایید شده/در انتظار امضای تسویه'),
            ('pending', 'در انتظار پرداخت'),
            ('paid', 'پرداخت شده'),
            ('error', 'نقص مدارک'),
        )

    def queryset(self, request, queryset):
        if self.value() == None:
            if request.user.has_perm('AmadoAccounting.can_pay_salary') and not request.user.is_superuser:
                r = queryset.filter(payment_status='pending')
            else:
                r = queryset.exclude(payment_status='paid')
        elif self.value() == 'registered':
            r = queryset.filter(payment_status='registered')
        elif self.value() == 'confirmed':
            r = queryset.filter(payment_status='confirmed')
        elif self.value() == 'pending':
            r = queryset.filter(payment_status='pending')
        elif self.value() == 'paid':
            r = queryset.filter(payment_status='paid')
        elif self.value() == 'error':
            r = queryset.filter(payment_status='error')
        else:
            r = queryset


        return r


class CurrencyFormCash(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CurrencyFormCash, self).__init__(*args, **kwargs)
        # self.fields['payment_due_date'].widget.attrs['readonly'] = True

    # extra_field = forms.CharField()

    def save(self, commit=True):
        extra_field = self.cleaned_data.get('extra_field', None)
        # ...do something with extra_field here...
        return super(CurrencyFormCash, self).save(commit=commit)

    class Meta:
        exclude = ()
        model = RecedeImage
        widgets = {
            'cost': forms.NumberInput(attrs={'step': 100000, 'min': 0, 'size': '100', 'localization': True}),
        }
class RecedeImageInline(admin.TabularInline):
    model = RecedeImage
    extra = 1
    form = CurrencyFormCash
    fields = ('image_title', 'cost','payment_due_date', 'image', 'factor_image')
    readonly_fields = ('factor_image',)

class SalaryDetailAdmin(admin.ModelAdmin):
    search_fields = ['person__name']
    
#    class Media:
#        js = (
#        'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
#        )
    
    list_display = ['id','get_branch', 'person', 'get_month', 'pardakhti','remainder', 'get_card','get_account','get_bank', 'payment_status']

    list_filter =[SalaryDFilter,MonthFilter,'salary__branch','account__bank','salary__month',]
    
    def remainder(self,obj):
        sum = RecedeImage.objects.filter(salary=obj).aggregate(sum=Sum('cost'))['sum']
        if sum:
            return obj.pardakhti-sum
        if obj.payment_status != 'paid':
            return obj.pardakhti
        return 0

    remainder.short_description = 'مانده قابل پرداخت(ریال)'
    
    inlines = [RecedeImageInline]
    
    autocomplete_fields = ['person','account']
    
    def get_card(self,obj):
        return obj.account.card
        
    get_card.short_description = 'کارت'
        
    def get_account(self,obj):
        return obj.account.account
    get_account.short_description = 'حساب'
        
    def get_bank(self,obj):
        if obj.account.bank:
            return obj.account.bank.bank_name
        else:
            return '-'
    get_bank.short_description = 'بانک'

    def get_branch(self, obj):
        if obj.salary.branch:
            return obj.salary.branch
        else:
            return 'قطع همکاری'

    get_branch.short_description = 'شعبه'
    
    get_branch.admin_order_field = 'salary__branch'

    def get_month(self,obj):
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

        return '%s %s'%(months[obj.salary.month.month-1],obj.salary.month.year)

    get_month.short_description = 'ماه'

    def wordifyfa(self,num, level):

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


    def print_tasvie(self,request,queryset):

        #TODO if not confirmed



        def my_int(num):
            if num :
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
        response['Content-Disposition'] = u'attachment; filename=tasvie.xls'
        wb = xlwt.Workbook(encoding='utf-8')

        today = jdatetime.datetime.today().strftime('%Y/%m/%d')


        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        #
        # alnum = Alignment()
        # alnum.horz = Alignment.HORZ_CENTER
        # alnum.vert = Alignment.VERT_CENTER

        al2 = Alignment()
        al2.horz = Alignment.HORZ_RIGHT
        al2.vert = Alignment.VERT_CENTER

        borders = xlwt.Borders()
        borders.left = 2
        borders.right = 2
        borders.top = 2
        borders.bottom = 2
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

        signature = xlwt.XFStyle()  # normal
        signature.alignment = al2
        signature.num_format_str = '#,##0'
        signature.font.height = 220
        signature.font.name = 'B Nazanin'

        header = xlwt.XFStyle()  # normal
        header.alignment = al
        header.font.bold = True
        header.num_format_str = '#,##0'
        header.font.height = 280
        header.borders = borders
        header.font.name = 'B Nazanin'


        for q in queryset:

            person = q.person
            agreement = BaseAgreement.objects.filter(person=person).order_by('date').last()
            branch = q.salary.branch
            
            if not branch:
                branch = WorkDetail.objects.filter(person=person).order_by('work__date').last().work.branch

            first_work = WorkDetail.objects.filter(person=person).order_by('-work__date').last().work.date
            last_work = WorkDetail.objects.filter(person=person).order_by('work__date').last().work.date

            from_date = q.salary.from_date
            to_date = q.salary.to_date

            if (first_work - from_date).days <= 0:  # first before from
                first_work = from_date
                if (last_work - to_date).days <= 0:
                    pass
                else:
                    last_work = to_date
            else:
                if (last_work - to_date).days <= 0:
                    pass
                else:
                    last_work = to_date
                    
            max_vac = (round((2.5 / 30) * (last_work - first_work).days * 2)) / 2

            gone_vac = max_vac - q.vacation_rem
                    
                    
            ws = wb.add_sheet(person.name)
            ws.cols_right_to_left = 1

            ws.col(0).width = int(55*42.3)
            ws.col(1).width = int(53*42.3)
            ws.col(2).width = int(101*42.3)
            ws.col(3).width = int(53*42.3)
            ws.col(4).width = int(63*42.3)
            ws.col(5).width = int(61*42.3)
            ws.col(6).width = int(53*42.3)
            ws.col(7).width = int(113*42.3)

            ws.row(0).height_mismatch = True
            ws.row(0).height = int(24*20)
            for i in range(1,25):
                ws.row(i).height_mismatch = True
                ws.row(i).height = int(17 * 20)
            ws.row(25).height_mismatch = True
            ws.row(25).height = int(15 * 20)
            for i in range(26,29):
                ws.row(i).height_mismatch = True
                ws.row(i).height = int(17 * 20)
            ws.row(30).height_mismatch = True
            ws.row(30).height = int(15 * 20)
            ws.row(31).height_mismatch = True
            ws.row(31).height = int(17 *20)
            
            month_days = 31
            try:
                jdatetime.datetime.strptime('%s31'%from_date.strftime('%Y-%m-'),'%Y-%m-%d')
            except:#not 31 days
                try:
                    jdatetime.datetime.strptime('%s30' % from_date.strftime('%Y-%m-'), '%Y-%m-%d')
                    month_days = 30
                except:
                    month_days = 29

            #1
            ws.write_merge(0,0,0,7,'برگه تسویه حساب قطعی رستوران آمادو شعبه %s'%(branch),header)

            #2
            ws.write(1,0,'محل خدمت',font_style)
            ws.write_merge(1, 1, 1, 2, 'رستوران آمادو شعبه %s' % (branch), font_style)

            ws.write_merge(1,1,3,4,'تاریخ تنظیم: %s'%today,font_style)#row1 row2 col1 col2

            ws.write(1, 5, 'شماره پرسنلی', font_style)
            ws.write_merge(1,1, 6,7, ' ', font_style)

            #3
            ws.write_merge(2,2,0,3,'اطلاعات فردی و پرسنلی',font_style)
            ws.write_merge(2,2,4,7,'اطلاعات حقوقی',font_style)

            #4
            font_style4gh = copy.deepcopy(font_style)
            font_style4gh.alignment.horz = Alignment.HORZ_CENTER
            ws.write(3,0,'نام',font_style)
            ws.write_merge(3,3,1,3,person.name.split(' ')[0],font_style)
            ws.write_merge(3,3,4,5,'دستمزد روزانه(ریال)',font_style)
            ws.write_merge(3,3,6,7,int(agreement.base/month_days),font_style4gh)

            #5
            ws.write(4, 0, 'نام خانوادگی', font_style)
            ws.write_merge(4, 4, 1, 3, person.name.split(' ')[1], font_style)
            ws.write(4, 4, 'شماره حساب', font_style)
            if q.account.account:
                ws.write_merge(4, 4, 5, 7, q.account.account, font_style4gh)
            else:
                ws.write_merge(4, 4, 5, 7, q.account.card, font_style4gh)

            #6
            ws.write(5, 0, 'کدملی', font_style)
            ws.write_merge(5, 5, 1, 3, person.nat_id, font_style4gh)
            ws.write_merge(5, 5,4,5, 'سایر مزایای روزانه', font_style)
            ws.write_merge(5, 5, 6, 7, ' ', font_style4gh)

            #7
            ws.write_merge(6, 6, 0, 1, 'تاریخ شروع به کار', font_style)
            ws.write_merge(6, 6, 2, 3, first_work.strftime('%Y/%m/%d'), font_style4gh)  # TODO
            ws.write_merge(6, 6, 4, 5, 'تاریخ خاتمه کار', font_style)
            ws.write_merge(6, 6, 6, 7, last_work.strftime('%Y/%m/%d'), font_style4gh)  # TODO

            #8
            font_style7c = copy.deepcopy(font_style)
            font_style7c.borders.left = 1
            ws.write_merge(7,7, 0,1, 'مدت زمان خدمت', font_style)
            ws.write(7,2, q.days, font_style4gh)
            ws.write(7, 3, 'روز', font_style7c)
            
            font_style4gh2 = copy.deepcopy(font_style4gh)
            font_style4gh2.num_format_str = '#,##0.0'
            
            ws.write_merge(7,7,4,5,'مرخصی قابل استفاده',font_style)
            ws.write(7, 6, max_vac, font_style4gh2)#TODO
            ws.write(7, 7, 'روز', font_style7c)

            #9
            ws.write_merge(8, 8, 0, 1, 'مرخصی استفاده شده', font_style)
            # ws.write(8, 2, gone_vac, font_style4gh2)#TODO
            ws.write(8, 2, '-', font_style4gh2)#TODO
            ws.write(8, 3, 'روز', font_style7c)
            ws.write_merge(8, 8, 4, 5, 'مرخصی قابل بازخرید', font_style)
            # ws.write(8, 6, Formula('G8-C9'), font_style4gh2)
            ws.write(8, 6, '-', font_style4gh2)#TODO
            # ws.write(8, 6, q.vacation_rem, font_style4gh2)
            ws.write(8, 7, 'روز', font_style7c)

            #10
            ws.write_merge(9, 9, 0, 3, ' ', font_style)
            ws.write_merge(9, 9, 4, 7, ' ', font_style)

            #11
            ws.write(10, 0, 'ردیف', font_style)
            ws.write_merge(10, 10, 1, 3, 'شرح', font_style)
            ws.write_merge(10, 10, 4, 6, 'محاسبه', font_style)
            ws.write(10, 7, 'مبلغ', font_style)
            row = 10

            # 12
            row += 1
            font_style12 = copy.deepcopy(font_style)
            font_style12.borders.bottom = 1
            font_style127 = copy.deepcopy(font_style12)
            font_style127.alignment.horz = Alignment.HORZ_CENTER
            ws.write(row, 0, row - 10, font_style127)
            ws.write_merge(row, row, 1, 3, 'حقوق و مزایا و سنوات %s' % months[q.salary.month.month - 1],
                           font_style12)  # TODO
            ws.write_merge(row, row, 4, 6, 'حقوق و مزایای %i روز کارکرد' % q.days, font_style12)
           

            # if q.vacation_rem > 0:  
            #     ws.write(row, 7, q.hoghoogh_mazaya_plus-q.eydi-q.vacation_rem_fee-q.negative_taraz-my_int(q.off_fee)-my_int(q.extra_shift_fee)-my_int(q.del_sal_fee)-my_iny(q.snapp)-my_int(q.reward), font_style127)
            # else:
            #      ws.write(row, 7, q.hoghoogh_mazaya_plus-q.eydi-q.negative_taraz-my_int(q.off_fee)-my_int(q.extra_shift_fee)-my_int(q.del_sal_fee)-my_iny(q.snapp)-my_int(q.reward), font_style127)

            ws.write(row, 7, q.hoghoogh_mazaya_plus - q.eydi - my_int(q.vacation_rem_fee) - q.negative_taraz - my_int(
                q.off_fee) - my_int(q.extra_shift_fee) - my_int(q.del_sal_fee) - my_int(q.snapp) - my_int(q.reward),
                     font_style127)

            font_style13 = copy.deepcopy(font_style)
            font_style13.borders.top = 1
            font_style137 = copy.deepcopy(font_style13)
            font_style137.alignment.horz = Alignment.HORZ_CENTER

            x = 0

            if q.vacation_rem > 0:

                x += 1

                row += 1

                ws.write(row, 0, row - 10, font_style137)
                ws.write_merge(row, row, 1, 3, ' ', font_style13)  # TODO
                ws.write_merge(row, row, 4, 6, 'بازخرید مرخصی', font_style13)  # TODO later morakhasi
                ws.write(row, 7, q.vacation_rem_fee, font_style137)
            
            if q.eydi > 0:

                x += 1

                row += 1

                ws.write(row, 0, row - 10, font_style137)
                ws.write_merge(row, row, 1, 3, ' ', font_style13)  # TODO
                ws.write_merge(row, row, 4, 6, 'عیدی', font_style13)  # TODO later morakhasi
                ws.write(row, 7, q.eydi, font_style137)
                
            if q.off > 0:

                x += 1

                row += 1

                ws.write(row, 0, row - 10, font_style137)
                ws.write_merge(row, row, 1, 3, ' ', font_style13)  # TODO
                ws.write_merge(row, row, 4, 6, 'حق %.1f روز آف'%q.off,font_style13)  # TODO later morakhasi
                ws.write(row, 7, q.off_fee, font_style137)
                
            

            if  my_int(q.del_sal) > 0:
                x += 1

                row += 1

                ws.write(row, 0, row - 10, font_style137)
                ws.write_merge(row, row, 1, 3, ' ', font_style13)  # TODO
                ws.write_merge(row, row, 4, 6, 'حق %i پیک/سالاد' % q.del_sal, font_style13)  # TODO later morakhasi
                ws.write(row, 7, q.del_sal_fee, font_style137)

            if my_int(q.extra_shift) > 0:
                x += 1

                row += 1

                ws.write(row, 0, row - 10, font_style137)
                ws.write_merge(row, row, 1, 3, ' ', font_style13)  # TODO
                ws.write_merge(row, row, 4, 6, 'حق %.1f شیفت اضافه' % q.extra_shift, font_style13)  # TODO later morakhasi
                ws.write(row, 7, q.extra_shift_fee, font_style137)

            if my_int(q.snapp) > 0:
                x += 1

                row += 1

                ws.write(row, 0, row - 10, font_style137)
                ws.write_merge(row, row, 1, 3, ' ', font_style13)  # TODO
                ws.write_merge(row, row, 4, 6, 'حق اسنپ', font_style13)  # TODO later morakhasi
                ws.write(row, 7, q.snapp, font_style137)

            if my_int(q.reward) > 0:
                x += 1

                row += 1

                ws.write(row, 0, row - 10, font_style137)
                ws.write_merge(row, row, 1, 3, ' ', font_style13)  # TODO
                ws.write_merge(row, row, 4, 6, 'پاداش', font_style13)  # TODO later morakhasi
                ws.write(row, 7, q.reward, font_style137)

            # 13 14 15 16
            for i in range(x, 4):
                row += 1
                ws.write(row, 0, row - 10, font_style137)
                ws.write_merge(row, row, 1, 3, ' ', font_style13)  # TODO
                ws.write_merge(row, row, 4, 6, ' ', font_style13)  # TODO later morakhasi
                ws.write(row, 7, ' ', font_style137)

            #17
            row += 1
            ws.write(row, 0, ' ', font_style)
            ws.write_merge(row, row, 1, 3, 'جمع کل', font_style)  # TODO
            ws.write_merge(row, row, 4, 6, ' ', font_style)  # TODO later morakhasi
            font_style177 = copy.deepcopy(font_style)
            font_style177.alignment.horz = Alignment.HORZ_CENTER
            ws.write(row, 7, Formula('SUM(H12:H16)'), font_style177)

            #18
            row += 1
            ws.write_merge(row,row, 0,7, 'کسورات', font_style)

            
            helps = EmployeePayment.objects.filter(
                Q(payment_person=q.person) & Q(payment_type='help') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))
            if helps:
                helps = helps.filter().values('payment_person').annotate(sum=Sum('payment_cost'))
                helps = helps[0]['sum']
            else:
                helps = None

            #19
            row += 1
            ws.write_merge(row, row, 0, 3, 'وام و مساعده تسویه نشده', font_style)  # TODO
            ws.write_merge(row, row, 4, 6, 'دریافتی', font_style)  # TODO
            ws.write(row, 7, helps, font_style177)  # TODO

            #20
            row += 1
            ws.write_merge(row, row, 0, 3, 'حق بیمه', font_style)  # TODO
            ws.write_merge(row, row, 4, 6, ' ', font_style12)  # TODO
            ws.write(row, 7, q.bime, font_style127)  # TODO

            #21
            # row += 1
            # ws.write_merge(row, row, 0, 3, 'کسورات', font_style)  # TODO
            # ws.write_merge(row, row, 4, 6, ' ', font_style13)  # TODO
            # s = my_int(q.other_deduction)+my_int(q.fine)+my_int(q.maliat)
            # if s != 0:
            #     ws.write(row, 7,s , font_style137)  # TODO
            # else:
            #     ws.write(row, 7, ' ', font_style137)  # TODO
        
            fines = EmployeePayment.objects.filter(
                Q(payment_person=q.person) & Q(payment_type='fine') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))

            other_ded = EmployeePayment.objects.filter(
                Q(payment_person=q.person) & Q(payment_type='other') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))


            x = 21
            for r in other_ded:
                x+=1
                row += 1

                ws.write_merge(row, row, 0, 3, 'کسورات', font_style)  # TODO
                ws.write_merge(row, row, 4, 6, r.payment_description, font_style13)  # TODO
                ws.write(row, 7, my_int(r.payment_cost), font_style137)  # TODO

            for r in fines:
                x += 1
                row += 1

                ws.write_merge(row, row, 0, 3, 'جریمه', font_style)  # TODO
                ws.write_merge(row, row, 4, 6, r.payment_description, font_style13)  # TODO
                ws.write(row, 7, my_int(r.payment_cost), font_style137)  # TODO



            if my_int(q.maliat)>0:
                x += 1
                row += 1

                ws.write_merge(row, row, 0, 3, 'مالیات', font_style)  # TODO
                ws.write_merge(row, row, 4, 6, ' ', font_style13)  # TODO
                ws.write(row, 7,my_int(q.maliat) , font_style137)  # TODO


            #22
            row += 1
            ws.write_merge(row, row, 0, 3, 'جمع کسورات', font_style)  # TODO
            ws.write_merge(row, row, 4, 6, ' ', font_style13)  # TODO
            ws.write(row, 7, Formula('SUM(H19:H%i)'%(x-1)), font_style137)  # TODO

            #23
            row += 1
            ws.write_merge(row, row, 0, 3, 'جمع قابل پرداخت', font_style)  # TODO
            ws.write_merge(row, row, 4, 6, ' ', font_style13)  # TODO
            ws.write(row, 7, Formula('H17-H%i'%x), font_style137)  # TODO

            #24
            row += 1

            #25
            row += 1
            ws.write_merge(row, row, 0, 2, 'تنظیم کننده: امور اداری و دستمزد', signature)  # TODO
            ws.write_merge(row, row, 4, 5, 'مدیر مالی و اداری:', signature)  # TODO
            ws.write(row, 7, 'مدیرعامل:', signature)  # TODO

            # 26
            row += 1

            #27
            row += 1

            r = RoleHistory.objects.filter(person=person).order_by('start_date').last().role
            if r.division.id == 8:
                del_sal = 'حق پیک، '
            elif r.division.id == 7:
                del_sal = 'حق سالاد، '
            else:
                del_sal = ''

            str = 'اینجانب %s با دریافت مبلغ %s ریال به حروف %s ریال کلیه مطالبات قانونی قرارداد شامل حقوق و مزایا، اضافه کاری، تعطیل کاری، حق سنوات %i، off کاری، شبکاری، %s حق مسکن، حق خواروبار و بیمه را از رستوران آمادو شعبه %s با رضایت کامل دریافت نموده و هیچگونه مطالبات دیگری ندارم و هرگونه ادعای بعدی از طرف اینجانب باطل و بی اساس خواهد بود' % (
            person.name, "{:,}".format(q.pardakhti), self.wordifyfa(q.pardakhti, 0), q.salary.month.year, del_sal,
            branch)
            
            sig = copy.deepcopy(signature)
            sig.alignment.wrap = 1
            sig.alignment.horz = Alignment.HORZ_JUSTIFIED

            ws.write_merge(row, row+4, 0, 7,str , sig)  # TODO

            row += 4


            # 28
            row += 1

            # 29
            row += 1
            ws.write_merge(row, row, 6, 7, 'امضا و اثرانگشت', signature)  # TODO




        wb.save(response)
        return response

    print_tasvie.short_description = 'خروجی فرم های تسویه'

    def confirm(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoAccounting.can_confirm_salary'):
            messages.error(request, "شما اجازه تایید ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status != 'registered':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'confirmed'
                q.confirm_user = request.user
                q.confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i حقوق تایید شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان تایید برخی یا همه حقوق ها وجود ندارد")

    confirm.short_description = 'تایید حقوق های انتخاب شده'


    def pend(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoAccounting.can_confirm_salary'):
            messages.error(request, "شما اجازه تایید ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status != 'confirmed':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'pending'
                q.confirm_user = request.user
                q.confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i حقوق در انتظار پرداخت است" % qs.count())
            return qs
        else:
            messages.error(request, "امکان انجام عملیات برای برخی یا همه حقوق ها وجود ندارد")

    pend.short_description = 'تبدیل وضعیت به در انتظار پرداخت'

    def pay(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoAccounting.can_pay_salary'):
            messages.error(request, "شما اجازه تایید ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status != 'pending':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'paid'
                q.confirm_user = request.user
                q.confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i حقوق پرداخت شد " % qs.count())
            return qs
        else:
            messages.error(request, "امکان پرداخت برخی یا همه حقوق ها وجود ندارد")

    pay.short_description = 'تبدیل وضعیت به پرداخت شده'

    def error(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoAccounting.can_pay_salary'):
            messages.error(request, "شما اجازه تایید ندارید")
            return
        flag = False
        for q in qs:
            if q.payment_status == 'paid':
                flag = True
        if not flag:
            for q in qs:
                q.payment_status = 'error'
                q.confirm_user = request.user
                q.confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i حقوق رد " % qs.count())
            return qs
        else:
            messages.error(request, "امکان رد برخی یا همه حقوق ها وجود ندارد")

    error.short_description = 'رد حقوق های انتخاب شده'
    
    def export_excel(self,request,queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=salaries.xls'
        wb = xlwt.Workbook(encoding='utf-8')

        today = jdatetime.datetime.today().strftime('%Y/%m/%d')

        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        #
        # alnum = Alignment()
        # alnum.horz = Alignment.HORZ_CENTER
        # alnum.vert = Alignment.VERT_CENTER

        al2 = Alignment()
        al2.horz = Alignment.HORZ_RIGHT
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

        font_style2 = xlwt.XFStyle()  # normal
        font_style2.alignment = al2
        font_style2.num_format_str = '#,##0.0'
        font_style2.font.height = 220
        font_style2.borders = borders
        font_style2.font.name = 'B Nazanin'

        signature = xlwt.XFStyle()  # normal
        signature.alignment = al2
        signature.num_format_str = '#,##0'
        signature.font.height = 220
        signature.font.name = 'B Nazanin'
        # b = xlwt.Borders()
        # b.left = 1
        # b.right = 1
        # b.top = 1
        # b.bottom = 1
        # b.left_colour = xlwt.Style.colour_map['white']
        # b.right_colour = xlwt.Style.colour_map['white']
        # b.top_colour = xlwt.Style.colour_map['white']
        # b.bottom_colour = xlwt.Style.colour_map['white']
        # signature.borders = b

        header = xlwt.XFStyle()  # normal
        header.alignment = al
        header.font.bold = True
        header.num_format_str = '#,##0'
        header.font.height = 280
        header.borders = borders
        header.font.name = 'B Nazanin'

        ws = wb.add_sheet('حقوق ها')
        ws.cols_right_to_left = 1

        ws.write(0, 0, 'نام و سمت',font_style)
        ws.write(0, 1, 'حقوق پرداختی',font_style)
        ws.write(0, 2, 'شماره کارت',font_style)
        ws.write(0, 3, 'شماره حساب',font_style)
        ws.write(0, 4, 'بانک',font_style)
        ws.write(0, 5, 'شعبه',font_style)
        ws.write(0, 6, 'وضعیت',font_style)

        row = 1

        ws.col(0).width = int(230 * 42.3)
        ws.col(1).width = int(111 * 42.3)
        ws.col(2).width = int(111 * 42.3)
        ws.col(3).width = int(111 * 42.3)
        ws.col(4).width = int(111 * 42.3)
        ws.col(5).width = int(111 * 42.3)
        ws.col(6).width = int(150 * 42.3)

        for q in queryset:

            ws.write(row,0,q.person.__str__(),font_style)
            ws.write(row,1,q.pardakhti,font_style)
            ws.write(row,2,q.account.card,font_style)
            ws.write(row,3,q.account.account,font_style)
            ws.write(row,4,q.account.bank.bank_name,font_style)
            ws.write(row,5,q.salary.branch.__str__(),font_style)


            if q.payment_status == 'registered':
                ws.write(row,6,'ثبت شده/در انتظار تایید',font_style)
            elif q.payment_status == 'confirmed':
                ws.write(row, 6, 'تایید شده/در انتظار امضای تسویه', font_style)
            elif q.payment_status == 'pending':
                ws.write(row, 6, 'در انتظار پرداخت', font_style)
            elif q.payment_status == 'paid':
                ws.write(row, 6, 'پرداخت شده', font_style)
            else:
                ws.write(row, 6, 'نقص مدارک', font_style)

            row += 1



        wb.save(response)
        return response

    export_excel.short_description = 'خروجی اکسل'

    actions = ['confirm', 'print_tasvie','pend','pay','error','export_excel']
    
    change_list_template = 'salary_det_change_list.html'

    def get_changelist(self, request):
        class MyChangeList(ChangeList):
            def remainder(self,obj):
                sum = RecedeImage.objects.filter(salary=obj).aggregate(sum=Sum('cost'))['sum']
                if sum:
                    return obj.pardakhti-sum
                if obj.payment_status != 'paid':
                    return obj.pardakhti
                return 0
            def get_results(self, *args, **kwargs):
                super(MyChangeList, self).get_results(*args, **kwargs)
                # rs = self.result_list.aggregate(tomato_sum=Sum('get_price'))
                sum = 0
                remsum = 0 
                for r in self.result_list:
                    sum += r.pardakhti
                    remsum += self.remainder(r)
                self.tomato_count = int(sum)
                self.tomato_count1 = int(remsum)

        return MyChangeList

class SalaryAdmin(admin.ModelAdmin):
    inlines = [DetailInline]

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/2.2.3/jquery.min.js',
            )

    # change_form_template = 'salary_change_form.html'

    change_list_template = 'salary_change_list.html'


class WorkDetailAdmin(admin.ModelAdmin):

    list_display = ['id','person','work','work_delivery_salad','work_status']
    
    list_filter = ['work__branch','work_status','person','work__date']
    
    search_fields = ['person__name']

    def get_queryset(self, request):
        qs = super(WorkDetailAdmin, self).get_queryset(request)
        role = request.user.groups.all()[0].name
        
        if role == 'assistant':
            return qs

        
        if role == 'manager':
            b = Branch.objects.get(branch_manager__manager_user=request.user)

            return qs.filter(work__branch=b)
        return qs

    def get_readonly_fields(self, request, obj=None):
        role = request.user.groups.all()[0].name

        if request.user.is_superuser or request.user.has_perm('AmadoAccounting.can_change_work'):
            return list([])

        if obj is None:
            if role == 'manager':
                return list([])
            return list([])

        if request.user.has_perm('AmadoFinance.can_see_work_detail'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        if obj.work.status == 'registered':
            if role == 'manager':
                return list([])
            return list([])

        else:
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result


class DetailWInline(admin.TabularInline):
    model = WorkDetail
    extra = 0
    
    # classes = ['collapse']

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/2.2.3/jquery.min.js',
            )

    def get_formset(self, request, obj=None, **kwargs):
        ## Put in your condition here and assign extra accordingly
        if obj is not None or request.user.is_superuser:
            return super(DetailWInline, self).get_formset(request, obj, **kwargs)

        b = Branch.objects.get(branch_manager__manager_user=request.user)

        if b.id == 4:
            persons = RoleHistory.objects.filter(
                (Q(role__branch__id=4)&(Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))|Q(finish_date=None)))|
                (Q(role__branch__id=8)&(Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))|Q(finish_date=None)))).values(
                'person__id')
        else:
            persons = RoleHistory.objects.filter(
                Q(role__branch=b) & (Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))|Q(finish_date=None))).values(
                'person__id')


        kwargs['extra'] = Person.objects.filter(id__in=[persons]).count()


        return super(DetailWInline, self).get_formset(request, obj, **kwargs)
    
    ordering = ['work__date']

    autocomplete_fields = ['person']

    def get_readonly_fields(self, request, obj=None):
        role = request.user.groups.all()[0].name

        if request.user.is_superuser or request.user.has_perm('AmadoAccounting.can_change_work'):
            return list([])

        if obj is None:
            if role == 'manager':
                return list([])
            return list([])

        if request.user.has_perm('AmadoFinance.can_see_work'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result
            
        try:
            if obj.status == 'registered':
                if role == 'manager':
                        return list([])
                else:
                    result = list(set(
                        [field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]
                    ))
                    result.remove('id')
                    return result
            else:
                result = list(set(
                    [field.name for field in self.opts.local_fields] +
                    [field.name for field in self.opts.local_many_to_many]
                ))
                result.remove('id')
                return result
        except:
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        
        # try:
        #     if obj.status == 'registered':
        #         if role == 'manager':
        #             return list([])
        #     return list([])
        # except:
        #     result = list(set(
        #         [field.name for field in self.opts.local_fields] +
        #         [field.name for field in self.opts.local_many_to_many]
        #     ))
        #     result.remove('id')
        #     return result
        

        # else:
        #     result = list(set(
        #         [field.name for field in self.opts.local_fields] +
        #         [field.name for field in self.opts.local_many_to_many]
        #     ))
        #     result.remove('id')
        #     return result
        
        
class DetailWInlineP(admin.TabularInline):
    model = WorkDetail
    extra = 0
    
    classes = ['collapse']
    
    autocomplete_fields = ['']

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/2.2.3/jquery.min.js',
            )

    def get_formset(self, request, obj=None, **kwargs):
        ## Put in your condition here and assign extra accordingly
        if obj is not None or request.user.is_superuser:
            return super(DetailWInlineP, self).get_formset(request, obj, **kwargs)

        b = Branch.objects.get(branch_manager__manager_user=request.user)

        persons = RoleHistory.objects.filter(
            Q(role__branch=b) & Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))).values(
            'person__id')


        kwargs['extra'] = Person.objects.filter(id__in=[persons]).count()


        return super(DetailWInlineP, self).get_formset(request, obj, **kwargs)
    
    ordering = ['work__date']

    autocomplete_fields = ['person']

    def get_readonly_fields(self, request, obj=None):
        role = request.user.groups.all()[0].name

        if request.user.is_superuser or request.user.has_perm('AmadoAccounting.can_change_work'):
            return list([])

        if obj is None:
            if role == 'manager':
                return list([])
            return list([])

        if request.user.has_perm('AmadoFinance.can_see_work'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result
            
        try:
            if obj.status == 'registered':
                if role == 'manager':
                        return list([])
                else:
                    result = list(set(
                        [field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]
                    ))
                    result.remove('id')
                    return result
            else:
                result = list(set(
                    [field.name for field in self.opts.local_fields] +
                    [field.name for field in self.opts.local_many_to_many]
                ))
                result.remove('id')
                return result
        except:
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

   
class WorkAdmin(admin.ModelAdmin):
    inlines = [DetailWInline]

    list_filter = ['branch']

    list_display = ['id','date','branch','status']

    ordering = ['-date']
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if not request.user.is_superuser:
            b = Branch.objects.get(branch_manager__manager_user=request.user)
            if b.id == 4:
                
                persons = RoleHistory.objects.filter(
                    (Q(role__branch__id=4)&(Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))|Q(finish_date=None)))|
                    (Q(role__branch__id=8)&(Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))|Q(finish_date=None)))).values(
                    'person__id')
                ps = Person.objects.filter(id__in=[persons])
                extra_context['persons'] = list(ps)
                extra_context['count'] = ps.count()
                return super(WorkAdmin, self).change_view(
                    request, None, form_url, extra_context=extra_context,
                )
            else:
                persons = RoleHistory.objects.filter(
                    Q(role__branch=b) & (Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))|Q(finish_date=None))).values(
                    'person__id')
    
                ps = Person.objects.filter(id__in=[persons])
                extra_context['persons'] = list(ps)
                extra_context['count'] = ps.count()
                return super(WorkAdmin, self).change_view(
                    request, None, form_url, extra_context=extra_context,
                )
        return super(WorkAdmin, self).change_view(
                    request, None, form_url, extra_context=extra_context,
                )

    change_form_template = 'work_change_form.html'

    def confirm(self, request, qs):
        role = request.user.groups.all()[0].name
        print(request.user.has_perm('AmadoAccounting.can_confirm_work'))
        if not request.user.has_perm('AmadoAccounting.can_confirm_work'):
            messages.error(request, "شما اجازه تایید ندارید")
            return

        for q in qs:
            q.status = 'confirmed'
            q.confirm_user = request.user
            q.confirm_date = jdatetime.datetime.now()
            q.save()
        self.message_user(request, "%i کارکرد تایید شد" % qs.count())
        return qs

    def open(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoAccounting.can_confirm_work'):
            messages.error(request, "شما اجازه باز کردن ندارید")
            return

        for q in qs:
            q.status = 'registered'
            q.save()
        self.message_user(request, "%i کارکرد باز شد" % qs.count())
        return qs

    confirm.short_description = 'تایید کارکرد های انتخاب شده'
    open.short_description = 'باز کردن کارکرد های انتخاب شده'

    actions = ['confirm','open']

    def save_model(self, request, instance, form, change):
        user = request.user
        role = request.user.groups.all()[0].name
        if not change:
            if not request.user.is_superuser:
                instance.add_user = request.user
                # instance.add_date = jdatetime.datetime.now()
                instance.branch = Branch.objects.get(branch_manager__manager_user=request.user)

        instance = form.save(commit=False)

        instance.save()
        form.save_m2m()
        return instance

    def get_readonly_fields(self, request, obj=None):
        role = request.user.groups.all()[0].name

        if request.user.is_superuser or request.user.has_perm('AmadoAccounting.can_change_work'):
            return list([])

        if obj is None:
            if role == 'manager' or role=='wh':
                return list(['status', 'add_user', 'add_date', 'confirm_user', 'confirm_date','branch'])
            return list(['status','add_user','add_date','confirm_user','confirm_date'])

        if request.user.has_perm('AmadoFinance.can_see_work'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        if obj.status == 'registered':
            if role == 'manager':
                return list(['status', 'add_user', 'add_date', 'confirm_user', 'confirm_date','branch'])
            return list(['status','add_user','add_date','confirm_user','confirm_date'])

        else:
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

    def get_queryset(self, request):
        qs = super(WorkAdmin, self).get_queryset(request)
        role = request.user.groups.all()[0].name
        
        if role == 'assistant':
            return qs
        

        
        if role == 'manager':
            b = Branch.objects.get(branch_manager__manager_user=request.user)

            return qs.filter(branch=b)
            
        if request.user.username == 'mms':
            b = Branch.objects.get(branch_manager__manager_user=request.user)

            return qs.filter(branch=b)
        return qs



class HistoryInline(admin.TabularInline):
    model = RoleHistory
    extra = 1

class BranchFilter(admin.SimpleListFilter):
    title = ('آخرین شعبه فرد')
    parameter_name = 'branch'

    def lookups(self, request, model_admin):

        return (
            (3, 'پونک'),
            (4, 'جنت آباد'),
            (5, 'سعادت آباد'),
            (6, 'گلستان'),
            (7, 'هایپراستار ارم'),
            (8, 'آماده سازی'),
            (9, 'دفتر مرکزی'),


        )

    def queryset(self, request, queryset):
        if self.value() == None:
            r = queryset.filter().order_by('check_due_date')
        else:
            today = jdatetime.datetime.today().date()
            req = queryset
            for p in queryset:
                rh = RoleHistory.objects.filter(Q(person=p)).order_by('start_date').last()
                # print(rh.finish_date != None and (today-rh.finish_date).days >=0 and rh.role.branch.last().id != int(self.value()))
                # if rh.finish_date != None and (today-rh.finish_date).days >=0 :#finished working
                #     req = req.exclude(id=p.id)
                # elif rh.role.branch.last().id != int(self.value()):#not this branch
                if rh.role.branch.last().id != int(self.value()):#not this branch
                    req = req.exclude(id=p.id)
                else:
                    pass

            return req


class PersonStatusFilter(admin.SimpleListFilter):
    title = ('وضعیت کاری فرد')
    parameter_name = 'pstatus'

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
            ('all','همه'),
            ('0', 'در حال کار'),
            ('1', 'استعفا داده/بدون امضای تسویه'),
            ('2', 'دارای امضای تسویه'),

        )

    def queryset(self, request, queryset):
        if self.value() == None:
            today = jdatetime.datetime.today()
            rh = RoleHistory.objects.filter((Q(finish_date__gte=today) | Q(finish_date__isnull=True))).values(
                'person__id')
            
            return queryset.filter(id__in=rh)
        elif self.value() == '1':
            today = jdatetime.date.today()
            retq = queryset
            for p in queryset:
                rh = RoleHistory.objects.filter(person=p).order_by('start_date').last()
                if rh.finish_date == None or rh.finish_date >= today:#kar mikonad
                    retq = retq.exclude(id=p.id)
                #kar nemikonad
                elif SalaryDetail.objects.filter(Q(person=p)&(Q(payment_status='pending')|Q(payment_status='paid'))).count()>0: #emza karde
                    retq = retq.exclude(id=p.id)
                else:
                    pass


            return retq

        elif self.value() == '2':
            today = jdatetime.date.today()
            retq = queryset
            for p in queryset:
                rh = RoleHistory.objects.filter(person=p).order_by('start_date').last()
                if rh.finish_date == None or rh.finish_date >= today:#kar mikonad
                    retq = retq.exclude(id=p.id)



                elif SalaryDetail.objects.filter(Q(person=p) & (
                    Q(payment_status='pending') | Q(payment_status='paid'))).count() == 0:  # emza karde
                    retq = retq.exclude(id=p.id)
                else:
                    pass


            return retq
        else:
#            today = jdatetime.datetime.today()
#            rh = RoleHistory.objects.filter((Q(finish_date__gte=today)|Q(finish_date__isnull=True))).values(
#                'person__id')
#            return queryset.filter(id__in=rh)
            return queryset


class AgreementInline(admin.TabularInline):
    model = BaseAgreement
    extra = 0

class AgreementFilter(admin.SimpleListFilter):
    title = ('توافق')
    parameter_name = 'agreement'

    def lookups(self, request, model_admin):

        return (
            ('has', 'دارد'),
            ('no', 'ندارد'),
        )

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset



        elif self.value() == 'has':
            r = queryset
            for q in queryset:
                ags = BaseAgreement.objects.filter(person=q)
                if ags.count() == 0:
                    r = r.exclude(id=q.id)
            return r
        else:
            r = queryset
            for q in queryset:
                ags = BaseAgreement.objects.filter(person=q)
                if ags.count() > 0:
                    r = r.exclude(id=q.id)

            return r


class PersonAdmin(admin.ModelAdmin):
    # inlines=[AgreementInline,HistoryInline,DetailWInlineP]
    inlines=[AgreementInline,HistoryInline]
    
    list_display = ['id','name','start_date','finish_date','role','vacs','rem_vacations']
    
    def vacs(self,obj=None):
        year = jdatetime.datetime.now().year
        return WorkDetail.objects.filter(Q(person=obj)&Q(work_status='V')&Q(work__date__gte=('%i-01-01'%year))).count()
        
    year = jdatetime.datetime.now().year    
    vacs.short_description = 'مرخصی های رفته از ابتدای سال %i'%year

    def start_date(self,obj=None):
        last_role = RoleHistory.objects.filter(Q(person=obj)).order_by('-start_date').last()

        return last_role.start_date

    start_date.short_description = 'تاریخ شروع کار '

    def finish_date(self, obj=None):
        last_role = RoleHistory.objects.filter(Q(person=obj)).order_by('start_date').last()

        return last_role.finish_date

    finish_date.short_description = 'تاریخ پایان کار'

    def role(self, obj=None):
        last_role = RoleHistory.objects.filter(Q(person=obj)).order_by('start_date').last()

        return last_role.role

    role.short_description = 'پست فعلی'

    search_fields = ['name']
    
    list_filter=[BranchFilter,PersonStatusFilter,AgreementFilter]
    
    change_list_template = 'person_change_list.html'
    
    filter_horizontal = ['banks']
    
    
    def changelist_view(self, request, extra_context=None):
        from_date = WorkDetail.objects.all().order_by('-work__date').last().work.date
        to_date = WorkDetail.objects.all().order_by('work__date').last().work.date

        my_context = {
            'from_date': from_date,
            'to_date': to_date,
        }
        return super(PersonAdmin, self).changelist_view(request,
                                                         extra_context=my_context)

    
    def action(self,request,queryset):

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=work_detail.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("کارکرد")

        row_num = 0

        from_date = jdatetime.datetime.strptime(request.POST.get('from_date'),'%Y-%m-%d')
        to_date = jdatetime.datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d')

        today = jdatetime.datetime.today()


        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300

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

        ws.write_merge(0, 0, 0, (to_date-from_date).days+1, 'کارکرد از تاریخ %s تا تاریخ %s' % (from_date.strftime('%Y/%m/%d'),to_date.strftime('%Y/%m/%d')), font_style)





        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 2
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al
        font_style.borders = borders
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        font_style.pattern = pattern

        counter_date = from_date

        columns = []
        row_num += 1

        ws.write(row_num, 0, 'نام فرد', font_style)
        ws.col(0).width = 6000
        ws.write(row_num, 1, 'سمت', font_style)
        ws.col(1).width = 6000


        for i in range(1,(to_date-from_date).days+2,1):
            columns.append(
                (counter_date.strftime("%m-%d"), 3500)
            )

            ws.write(row_num, i+1, counter_date.strftime("%m-%d"), font_style)
            counter_date += jdatetime.timedelta(days=1)



        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 2
        font_style.num_format_str = '#,##0'
        font_style.font.height = 300
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        font_style.alignment = al
        font_style.borders = borders

        for p in queryset:
            row_num += 1
            ws.write(row_num, 0, p.name, font_style)
            role = RoleHistory.objects.filter(person=p).order_by('start_date').last().role
            ws.write(row_num, 1, '%s %s'%(role.title,role.branch.last().branch_name), font_style)
            counter_date = from_date
            for i in range(1, (to_date - from_date).days + 2, 1):
                try:
                    status = WorkDetail.objects.get(Q(person=p)&Q(work__date=counter_date)).work_status
                except:
                    if today < counter_date:
                        status = ''
                    else:
                        status = '*'

                ws.write(row_num, i+1, status, font_style)

                counter_date += jdatetime.timedelta(days=1)

        wb.save(response)
        return response
    action.short_description = 'خروجی اکسل کارکرد پرسنل'
   
    def get_days(self, person, from_date, to_date, two_shift, extra_percentage,talab_morakhasi):

        details = WorkDetail.objects.filter(
            Q(person=person) & Q(work__date__gte=from_date) & Q(work__date__lte=to_date)).values(
            'work_status').annotate(count=Count('work_status'), dcount=Sum('work_delivery_salad'))

        prev_work = WorkDetail.objects.filter(Q(person=person) & Q(work__date__lt=from_date)).order_by('work__date')
        first_date = prev_work
        # if prev_work:
        #     last_date = prev_work.last().work.date
        #     first_date = first_date.last().work.date
        #     months = (last_date - first_date).months
        #     max_vac = months * 2.5
        #     talab_morakhasi = 0
        #     for tm in prev_work:
        #         if tm.work_status == 'V':
        #             talab_morakhasi += 1
        #
        #     talab_morakhasi = max_vac - talab_morakhasi
        #     if talab_morakhasi < 0:
        #         talab_morakhasi = 0
        # else:
        #     talab_morakhasi = 2.5



        first_work = WorkDetail.objects.filter(person=person).order_by('-work__date').last().work.date
        last_work = WorkDetail.objects.filter(person=person).order_by('work__date').last().work.date

        # if (first_work - from_date.date()).days <= 0:
        #     talab_morakhasi = 5  # TODO
        # else:
        #     talab_morakhasi = 0
        #
        # talab_morakhasi = 0
        # if talab_morakhasi != '':
        #     talab_morakhasi = int(talab_morakhasi)
        
        talab_morakhasi = person.rem_vacations

        if (first_work - from_date.date()).days <= 0:  # first before from
            first_work = from_date.date()
            if (last_work - to_date.date()).days <= 0:
                pass
            else:
                last_work = to_date.date()
        else:
            if (last_work - to_date.date()).days <= 0:
                pass
            else:
                last_work = to_date.date()

        max_vac = (round((2.5 / 30) * (last_work - first_work).days *2))/2

        max_off = round(((last_work - first_work).days + 1) / 7)


        if max_off < 0:
            max_off = 0

        if max_vac < 0:
            max_vac = 0

        days = 0
        off = 0
        vacations = 0
        absents = 0
        p = 0
        extra_shift = 0
        del_sal = 0
        for d in details:
            if d['dcount']:
                del_sal += d['dcount']

            if d['work_status'] == 'O':
                off += d['count']

            if two_shift and d['work_status'] == 'PP':
                days += d['count']
            elif two_shift and d['work_status'] == 'P':
                days += d['count'] / 2
                p += d['count'] / 2
            elif not two_shift and d['work_status'] == 'PP':
                days += d['count']
                extra_shift += d['count']
            elif not two_shift and d['work_status'] == 'P':
                days += d['count']

            if d['work_status'] == 'V':
                vacations += d['count']

            if d['work_status'] == 'A':
                absents += d['count']

            if d['work_status'] == 'T':
                days += d['count']

        if off > max_off:
            absents += (off - max_off)
            off = max_off

        gone_vac = vacations

        if vacations > max_vac + talab_morakhasi:
            absents += vacations - (max_vac + talab_morakhasi)
            vacations = max_vac + talab_morakhasi

        off += p

        off_rem = max_off - off
        if off_rem > absents:
            off_rem -= absents
            absents = 0
        elif off_rem < absents:
            absents -= off_rem
            off_rem = 0
        else:
            absents = 0
            off_rem = 0

        # return (days+off+vacations-extra_percentage*absents),off_rem,extra_shift,del_sal
        return (days + off + vacations), off_rem, extra_shift, del_sal,talab_morakhasi+max_vac-gone_vac
    
    def get_salary(self, request, queryset):




        last_constant = LawConstant.objects.all().order_by('date').last()

        response = HttpResponse(content_type='application/ms-excel')

        output = BytesIO()
        wb = xlsxwriter.Workbook(output)
        ws = wb.add_worksheet("حقوق")
        ws.right_to_left()
        ws.freeze_panes(0, 1)
        ws.freeze_panes(0, 2)
        ws.freeze_panes(0, 3)

        ws.set_zoom(50)





        from_date = jdatetime.datetime.strptime(request.POST.get('from_date'), '%Y-%m-%d')
        to_date = jdatetime.datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d')

        month_days = 31
        try:
            jdatetime.datetime.strptime('%s31'%from_date.strftime('%Y-%m-'),'%Y-%m-%d')
        except:#not 31 days
            try:
                jdatetime.datetime.strptime('%s30' % from_date.strftime('%Y-%m-'), '%Y-%m-%d')
                month_days = 30
            except:
                month_days = 29

        q = queryset[0]

        branch = RoleHistory.objects.filter(person=q).order_by('-start_date')[0].role.branch.last().branch_name

        month = from_date.month

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

        header = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size':30,
            'reading_order': 2})

        font_style = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 15,
            'num_format': '#,###',
            'reading_order': 2})


        radif = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color':'#c0c0c0',
            'font_size': 15,
            'num_format': '#,###',
            'reading_order': 2})

        before_mazaya = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': 'yellow',
            'font_size': 15,
            'num_format': '#,###',
            'reading_order': 2})

        mazaya = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#d6fdd1',
            'font_size': 15,
            'num_format': '#,###',
            'reading_order': 2})

        kosoorat = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#ef8783',
            'font_size': 15,
            'num_format': '#,###',
            'reading_order': 2})

        payable = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#d6feff',
            'font_size': 15,
            'num_format': '#,###',
            'reading_order': 2})

        cards = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#ffffa6',
            'font_size': 15,
            'num_format': '#,###',
            'reading_order': 2})

        sums = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#a3ca3f',
            'font_size': 15,
            'num_format': '#,###',
            'reading_order': 2})


        ws.merge_range('A1:AL1', 'حقوق ماه %s %s' % (months[month - 1], branch), header)

        alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                     'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']

        cols = [
            ('ردیف', radif),('نام', radif),('سمت', radif),
            ('روز های کارکرد', font_style),('حقوق ثابت', font_style),('حقوق پایه', before_mazaya),
            ('پایه حقوق توافقی', font_style),('حق مسکن', before_mazaya),('تعداد فرزند', font_style),
            ('حق اولاد', before_mazaya),('بن', before_mazaya),('سنوات', before_mazaya),('جمع حقوق وزارت کار', before_mazaya),

            ('تراز', mazaya),('مزایای شغلی', mazaya),('شیفت اضافه', font_style),('مزد شیفت اضافه', mazaya),
            ('پیک/سالاد', font_style),('حق پیک/سالاد', mazaya),('ایام تعطیل کاری', font_style),('مبلغ تعطیل کاری', mazaya),
            ('ساعت اضافه کاری', font_style),('مبلغ اضافه کاری', mazaya),

            ('عیدی', mazaya), ('تعداد مرخصی مانده', font_style), ('حق طلب مرخصی', mazaya),

            ('پاداش', mazaya),('حق اسنپ', mazaya),('جمع حقوق و مزایا', mazaya),

            ('مساعده', kosoorat),('تراز', kosoorat),('سایر کسورات', kosoorat),('جریمه', kosoorat),
            ('بیمه', kosoorat),('مالیات', kosoorat),('جمع کسورات', kosoorat),

            ('حقوق پرداختی', payable),('بیمه سهم کارفرما', font_style),

            ('شماره حساب', cards),('شماره کارت', cards),('بانک', cards)


        ]

        row_num = 2
        ws.set_row(1, 30)
        # ws.set_column('A:A', 10)
        ws.set_column('A:AL', 25)

        for i in range(0,cols.__len__()):
            ws.write('%s%i'%(alphabets[i],row_num),cols[i][0],cols[i][1])

        last_row = queryset.count() + 3

        i = 2
        for q in queryset:
            i+= 1

            calc_vacations = False
            vacation_left = None
            if request.POST.get('v%i'%q.id):
                calc_vacations = True

            vacation_left = request.POST.get('vnum%i'%q.id)

            if vacation_left == '' or vacation_left == None:
                vacation_left
                if from_date.year == 1397:
                    start = '1397-05-01'
                    talab = q.rem_vacations  # before mordad 1397
                    max_vac = 2.5 * (from_date - jdatetime.datetime.strptime(start,'%Y-%m-%d')).days / month_days#max morakhasi az mordad ta avvale dore hoghogh o dastmozd

                    gone_v_before = WorkDetail.objects.filter(
                        Q(person=q) & Q(work_status='V') & Q(work__date__lt=from_date)).count()#morakhasi haye rafte ta avvale dore hoghogh o dastmozd

                    vacation_left = max_vac - gone_v_before + talab
                else:
                    start = '%i-01-01'%(from_date.year)
                    max_vac = 2.5 * (from_date - jdatetime.datetime.strptime(start,'%Y-%m-%d')).days / month_days

                    gone_v_before = WorkDetail.objects.filter(
                        Q(person=q) & Q(work_status='V') & Q(work__date__lt=from_date)).count()

                    vacation_left = max_vac - gone_v_before
            else:
                vacation_left = float(vacation_left)




            calc_eydi = False
            eydi_formula = ''
            if request.POST.get('eydi%i' % q.id):
                calc_eydi = True
                days = int(request.POST.get('eydinum%i' % q.id))
                if q.insurance_start_date and not q.insurance_finish_date:
                    eydi_formula = '=2*(11112690/365)*%i' % days
                else:
                    eydi_formula = '=(11112690/365)*%i' % days
                    
                    
#                eydi_formula = '=IF(2*%s^>3*%s^,3*%s^*%i*%i/(365*%s^),2*%s^*%i*%i/(365*%s^))' % (
#                alphabets[cols.index(('پایه حقوق توافقی', font_style))],
#                alphabets[cols.index(('حقوق پایه', before_mazaya))],
#                alphabets[cols.index(('حقوق پایه', before_mazaya))],month_days, days,
#                alphabets[cols.index(('روز های کارکرد', font_style))],
#                alphabets[cols.index((
#                    'پایه حقوق توافقی',
#                    font_style))],month_days, days,
#                alphabets[cols.index((
#                    'روز های کارکرد',
#                    font_style))]
#                )

            aggreement = BaseAgreement.objects.filter(Q(person=q) & Q(date__lte=to_date)).order_by(
                'date').last()  # TODO ask
            role = RoleHistory.objects.filter(person=q).order_by('-start_date')[0].role

            bank_account = q.banks.last()

            if aggreement:
                days, off, extra_shift, del_sal,gone_vac = self.get_days(q, from_date, to_date, aggreement.two_shift,
                                                                last_constant.extra_percentage,vacation_left)
                snapp_fee = aggreement.snapp_fee
                aggreement = aggreement.base
                
            else:
                days, off, extra_shift, del_sal,gone_vac = self.get_days(q, from_date, to_date, True,
                                                                last_constant.extra_percentage,vacation_left)
                aggreement = 0
                snapp_fee = 0

            if not calc_vacations:
                gone_vac = 0


            rewards = EmployeePayment.objects.filter(
                Q(payment_person=q) & Q(payment_type='reward') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))

            rewards_str = '='
            for r in rewards:
                rewards_str = '%s+%i'%(rewards_str,r.payment_cost)
            # rewards_str = rewards_str[:-1]

            helps = EmployeePayment.objects.filter(
                Q(payment_person=q) & Q(payment_type='help') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))

            helps_str = '='
            for r in helps:
                helps_str = '%s+%i' % (helps_str,r.payment_cost)
            # helps_str = helps_str[:-1]

            fines = EmployeePayment.objects.filter(
                Q(payment_person=q) & Q(payment_type='fine') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))

            fines_str = '='
            for r in fines:
                fines_str = '%s+%i' % (fines_str, r.payment_cost)
            # fines_str = fines_str[:-1]


            other_ded = EmployeePayment.objects.filter(
                Q(payment_person=q) & Q(payment_type='other') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))

            other_ded_str = '='
            for r in other_ded:
                other_ded_str = '%s+%i' % (other_ded_str, r.payment_cost)
            # other_ded_str = other_ded_str[:-1]


            other_maz = EmployeePayment.objects.filter(
                Q(payment_person=q) & Q(payment_type='otherm') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))

            other_maz_str = '='
            for r in other_maz:
                other_maz_str = '%s+%i' % (other_maz_str, r.payment_cost)
            # other_maz_str = other_maz_str[:-1]


            snapp = EmployeePayment.objects.filter(
                Q(payment_person=q) & Q(payment_type='snapp') & Q(payment_do_date__gte=from_date) & Q(
                    payment_do_date__lte=to_date) & Q(payment_status='paid'))

            snapp_str = '='
            for r in snapp:
                snapp_str = '%s+%i' % (snapp_str, r.payment_cost)
            # snapp_str = snapp_str[:-1]

            rew_coms = ''
            for e in EmployeePayment.objects.filter(Q(payment_person=q) & Q(payment_type='reward') & Q(
                    payment_do_date__gte=from_date) & Q(payment_do_date__lte=to_date) & Q(payment_status='paid')):
                rew_coms = '%s\n%s' % (e.payment_description,rew_coms)
            helps_coms = ''
            for e in EmployeePayment.objects.filter(Q(payment_person=q) & Q(payment_type='help') & Q(
                    payment_do_date__gte=from_date) & Q(payment_do_date__lte=to_date) & Q(payment_status='paid')):
                helps_coms = '%s\n%s' % (e.payment_description,helps_coms)
            fine_coms = ''
            for e in EmployeePayment.objects.filter(Q(payment_person=q) & Q(payment_type='fine') & Q(
                    payment_do_date__gte=from_date) & Q(payment_do_date__lte=to_date) & Q(payment_status='paid')):
                fine_coms = '%s\n%s' % (e.payment_description,fine_coms)
            otherm_coms = ''
            for e in EmployeePayment.objects.filter(Q(payment_person=q) & Q(payment_type='other') & Q(
                    payment_do_date__gte=from_date) & Q(payment_do_date__lte=to_date) & Q(payment_status='paid')):
                otherm_coms = '%s\n%s' % (e.payment_description,otherm_coms)
            othermaz_coms = ''
            for e in EmployeePayment.objects.filter(Q(payment_person=q) & Q(payment_type='otherm') & Q(
                    payment_do_date__gte=from_date) & Q(payment_do_date__lte=to_date) & Q(payment_status='paid')):
                othermaz_coms = '%s\n%s' % (e.payment_description,othermaz_coms)
            snapp_coms = ''
            for e in EmployeePayment.objects.filter(Q(payment_person=q) & Q(payment_type='snapp') & Q(
                    payment_do_date__gte=from_date) & Q(payment_do_date__lte=to_date) & Q(payment_status='paid')):
                snapp_coms = '%s\n%s' % (e.payment_description,snapp_coms)


            ws.set_row(i, 30)

            childs = q.childs

            insurance = None
            # if q.insurance_start_date.strftime('%Y-%m-%d') <= from_date.strftime('%Y-%m-%d') and (not q.insurance_finish_date or(q.insurance_finish_date and q.insurance_finish_date.strftime('%Y-%m-%d') >= from_date.strftime('%Y-%m-%d'))):
            #         ws.write(i, 28, Formula('(Y%i-L%i-J%i)*%i%%' % (i + 1, i + 1,i+1,last_constant.bime_percentage)), font_style)  # TODO
            #     else:
            #         ws.write(i, 28,None,font_style)  # TODO
            if q.insurance_start_date and not q.insurance_finish_date:
#                insurance = 908818
#                insurance = 882888
#                insurance = '=(%s^-%s^-%s^)*7%%'%(alphabets[cols.index(('جمع حقوق وزارت کار', before_mazaya))],alphabets[cols.index(('سنوات', before_mazaya))],alphabets[cols.index(('حق مسکن', before_mazaya))])
#                insurance = 1049300
                insurance = 880818

            baccount = None
            bcard = None
            bname = None
            if bank_account:
                baccount =  bank_account.account
                bcard =  bank_account.card
                bname =  bank_account.bank.__str__()


            row_cols = [
                (i-2,radif),(q.name, radif),(role.title, radif),
                (days, font_style),(last_constant.vezarat_kar_base, font_style),
                ('=%s^/30*%s^'%(alphabets[cols.index(('حقوق ثابت',font_style))],alphabets[cols.index(('روز های کارکرد',font_style))]),font_style),
                ('=%i/%i*%s^'%(aggreement,month_days,alphabets[cols.index(('روز های کارکرد',font_style))]),font_style),
                ('=%i/%i*%s^'%(last_constant.maskan_base,month_days,alphabets[cols.index(('روز های کارکرد',font_style))]),font_style),
                (q.childs,font_style),
                ('=IF(%s^=0,0,IF(%s^=%i,B%i/30*3,B%i/30*6))' % (alphabets[cols.index(('تعداد فرزند', font_style))],alphabets[cols.index(('تعداد فرزند', font_style))],
                                                                last_constant.min_child,last_row + 2,last_row + 2 ),font_style),
                ( '=%i/%i*%s^'%(last_constant.bon_base,month_days,alphabets[cols.index(('روز های کارکرد',font_style))]) ,font_style),
                ('=%s^/365*%s^' % (alphabets[cols.index(('روز های کارکرد', font_style))],alphabets[cols.index(('حقوق ثابت', font_style))]),font_style),
                ('=%s^+%s^+%s^+%s^+%s^' % (alphabets[cols.index(('حقوق پایه', before_mazaya))],
                                           alphabets[cols.index(('حق مسکن', before_mazaya))],
                                           alphabets[cols.index(('حق اولاد', before_mazaya))],
                                           alphabets[cols.index(('بن', before_mazaya))],
                                           alphabets[cols.index(('سنوات', before_mazaya))])
                                   , font_style),

                ('=IF(%s^>%s^,%s^-%s^,0)'%(alphabets[cols.index(('پایه حقوق توافقی', font_style))],alphabets[cols.index(('جمع حقوق وزارت کار', before_mazaya))],
                                           alphabets[cols.index(('پایه حقوق توافقی', font_style))],
                                           alphabets[cols.index(('جمع حقوق وزارت کار', before_mazaya))]),font_style),
                (other_maz_str,font_style),
                (extra_shift,font_style),
                ('=%s^/30*%s^'%(alphabets[cols.index(('حقوق ثابت', font_style))],alphabets[cols.index(('شیفت اضافه', font_style))]),font_style),
                (del_sal, font_style),
                ('=%s^*%i'%(alphabets[cols.index(('پیک/سالاد', font_style))],last_constant.delivery_base), font_style),
                (off, font_style),
                ('=%s^/30*%s^' % (alphabets[cols.index(('حقوق ثابت', font_style))],
                                  alphabets[cols.index(('ایام تعطیل کاری', font_style))]), font_style),
                (None, font_style),
                ('=(%s^/%i*% 6.2f)*%s^'%(alphabets[cols.index(('حقوق پایه', before_mazaya))],last_constant.week_base, last_constant.extra_percentage,
                                         alphabets[cols.index(('ساعت اضافه کاری', font_style))]),font_style),
                (eydi_formula,font_style)
                ,(gone_vac,font_style),('=%s^/30*%s^'%(alphabets[cols.index(('حقوق ثابت',font_style))],alphabets[cols.index(('تعداد مرخصی مانده',font_style))]),font_style),
                (rewards_str, font_style),
                (snapp_str, font_style),
                # ('=%s^*%i'%(alphabets[cols.index(('روز های کارکرد', font_style))],snapp_fee), font_style),TODO
                ('=%s^+%s^+%s^+%s^+%s^+%s^+%s^+%s^+%s^+%s^+%s^' % (alphabets[cols.index(('جمع حقوق وزارت کار', before_mazaya))],
                                           alphabets[cols.index(('تراز', mazaya))],
                                           alphabets[cols.index(('مزایای شغلی', mazaya))],
                                           alphabets[cols.index(('مزد شیفت اضافه', mazaya))],
                                           alphabets[cols.index(('حق پیک/سالاد', mazaya))],
                                           alphabets[cols.index(('مبلغ تعطیل کاری', mazaya))],
                                           alphabets[cols.index(('مبلغ اضافه کاری', mazaya))],
                                           alphabets[cols.index(('عیدی', mazaya))],
                                           alphabets[cols.index(('حق طلب مرخصی', mazaya))],
                                           alphabets[cols.index(('پاداش', mazaya))],
                                           alphabets[cols.index(('حق اسنپ', mazaya))],
                                           )
                 , font_style),
                (helps_str, font_style),
                ('=IF(%s^<%s^,%s^-%s^,0)' % (alphabets[cols.index(('پایه حقوق توافقی', font_style))],
                                             alphabets[cols.index(('جمع حقوق وزارت کار', before_mazaya))],
                                             alphabets[cols.index(('جمع حقوق وزارت کار', before_mazaya))],
                                             alphabets[cols.index(('پایه حقوق توافقی', font_style))]), font_style),
                (other_ded_str, font_style),
                (fines_str, font_style),
                (insurance, font_style),
                (None,font_style),
                ('=SUM(%s^:%s^)'%(alphabets[cols.index(('مساعده', kosoorat))],alphabets[cols.index(('مالیات', kosoorat))]),font_style),
                ('=%s^-%s^'%(alphabets[cols.index(('جمع حقوق و مزایا', mazaya))],alphabets[cols.index(('جمع کسورات', kosoorat))]),font_style),
                ('=%s^/%i%%*%i%%'%(alphabets[cols.index(('بیمه', kosoorat))],last_constant.bime_percentage,last_constant.kargar_bime_ratio1),font_style),
                (baccount, cards),
                (bcard, cards),
                (bname, cards),

            ]

            for j in range(0, row_cols.__len__()):
                try:
                    first = row_cols[j][0].replace('^', '%i' % i)
                except:
                    first = row_cols[j][0]
                ws.set_row(i-1,30)
                ws.write('%s%i' % (alphabets[j], i), first, row_cols[j][1])

            if rew_coms != '':
                ws.write_comment('%s%i'%(alphabets[cols.index(('پاداش', mazaya))],i), rew_coms)
            if helps_coms != '':
                ws.write_comment('%s%i'%(alphabets[cols.index(('مساعده', kosoorat))],i), helps_coms)
            if fine_coms != '':
                ws.write_comment('%s%i'%(alphabets[cols.index(('جریمه', kosoorat))],i), fine_coms)
            if otherm_coms != '':
                ws.write_comment('%s%i'%(alphabets[cols.index(('سایر کسورات', kosoorat))],i), otherm_coms)
            if othermaz_coms != '':
                ws.write_comment('%s%i'%(alphabets[cols.index(('مزایای شغلی', mazaya))],i), othermaz_coms)
            if snapp_coms != '':
                ws.write_comment('%s%i'%(alphabets[cols.index(('حق اسنپ', mazaya))],i), snapp_coms)

        #     # ws.write(i, 29, Formula('IF(Y%i>=%i,(Y%i-%i-(AC%i*% 6.2f))*%i%%,0)' % (i + 1,last_constant.tax_min, i + 1,last_constant.tax_min,i+1,last_constant.tax_bime_ratio,last_constant.tax_percentage)),font_style)  # TODO


        i += 1
        #
        # ws.row(last_row).height_mismatch = True
        ws.set_row(last_row,30)
        ws.merge_range('A%i:C%i'%(last_row,last_row), 'جمع کل', sums)

        for i in range(3,cols.__len__()):
            col_alphabet = alphabets[i]
            ws.write('%s%i'%(col_alphabet,last_row),'=Sum(%s3:%s%i)'%(col_alphabet,col_alphabet,last_row-1),sums)

        ws.set_row(last_row, 30)
        ws.write(last_row, 0, 'حقوق پایه وزارت کار', sums)
        ws.write(last_row, 1, last_constant.vezarat_kar_base, sums)
        
        ws.write(last_row, 2, 'از تاریخ', sums)
        ws.write(last_row, 3, from_date.strftime('%Y/%m/%d'), sums)
        ws.write(last_row, 4, 'تا تاریخ', sums)
        ws.write(last_row, 5, to_date.strftime('%Y/%m/%d'), sums)

        wb.close()  # close book and save it in "output"
        output.seek(0)  # seek stream on begin to retrieve all data from it

        # send "output" object to stream with mimetype and filename
        response = StreamingHttpResponse(
            output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = u'attachment; filename=salary.xlsx'
        return response
    
    
    get_salary.short_description = 'محاسبه حقوق'

    actions = [action,get_salary]
    
    def get_model_perms(self, request):
        if request.user.is_superuser or not request.user.has_perm('AmadoAccounting.can_see_person') or request.user.username=='sadeghi':
            perms = admin.ModelAdmin.get_model_perms(self, request)
            return perms
        return {}

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return list([])

        if request.user.has_perm('AmadoAccounting.can_see_person'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result

        return list([])

    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        role = request.user.groups.all()[0].name

        
        if role == 'manager':
            b = Branch.objects.get(branch_manager__manager_user=request.user)

            # persons = RoleHistory.objects.filter(role__branch=b).values('person__id')
#            persons = RoleHistory.objects.filter(Q(role__branch=b)&Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))).values('person__id')
            persons = RoleHistory.objects.filter(Q(role__branch=b)&(Q(finish_date__gte=jdatetime.datetime.today().strftime('%Y-%m-%d'))|Q(finish_date=None))).values('person__id')
    
            

            return qs.filter(id__in=[persons])
        return qs

class RoleAdmin(admin.ModelAdmin):
    inlines=[HistoryInline]

class BranchFilterE(admin.SimpleListFilter):
    title = ('آخرین شعبه فرد')
    parameter_name = 'branch'

    def lookups(self, request, model_admin):

        return (
            (3, 'پونک'),
            (4, 'جنت آباد'),
            (5, 'سعادت آباد'),
            (6, 'گلستان'),
            (7, 'هایپراستار ارم'),
            (8, 'آماده سازی'),
            (9, 'افراد غیر فعال'),

        )

    def queryset(self, request, queryset):
        if self.value() == None:
            r = queryset.filter().order_by('check_due_date')
            
        elif self.value() == '9':
            today = jdatetime.date.today()
            retq = queryset
            for q in queryset:
                p = q.payment_person
                rh = RoleHistory.objects.filter(person=p).order_by('start_date').last()
                if rh.finish_date >= today or rh.finish_date == None:
                    retq = retq.exclude(id=q.id)
            # rh = RoleHistory.objects.filter(finish_date__lt=today).order_by().values('person__id')
                
            return retq
        else:
            today = jdatetime.datetime.today()
            rh = RoleHistory.objects.filter(Q(role__branch__id=self.value()) & (Q(finish_date__gte=today)|Q(finish_date=None))).values(
                'person__id')
            
            return queryset.filter(payment_person__id__in=rh)

class PaymentStatusFilter(admin.SimpleListFilter):
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
            r = queryset.exclude(payment_status='paid').order_by('payment_date')
        elif self.value() == 'notpaid':
            r = queryset.exclude(payment_status='paid').order_by('payment_date')
        elif self.value() == 'paid':
            r = queryset.filter(payment_status='paid').order_by('payment_date')
        elif self.value() == 'registered':
            r = queryset.filter(payment_status='registered').order_by('payment_date')
        elif self.value() == 'confirmed':
            r = queryset.filter(payment_status='confirmed').order_by('payment_date')
        elif self.value() == 'rejected':
            r = queryset.filter(payment_status='rejected').order_by('payment_date')
        elif self.value() == 'closed':
            r = queryset.filter(payment_status='closed').order_by('payment_date')
        else:
            r = queryset


        return r


class PaymentTypeFilter(admin.SimpleListFilter):
    title = ('نوع')
    parameter_name = 'type'

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
            ('help', 'مساعده'),
            ('reward', 'پاداش'),
            ('fine', 'جریمه'),
            ('other', 'سایر کسورات'),
            ('otherm', 'سایر مزایا'),
            ('snapp', 'حق اسنپ'),
        )

    def queryset(self, request, queryset):
        
        if self.value() == None:
            if request.user.has_perm('AmadoFinance.can_confirm_cash') and not request.user.is_superuser:
                r = queryset.filter(payment_type='help').order_by('payment_date')
            else:
                return queryset
        elif self.value() == 'help':
            r = queryset.filter(payment_type='help').order_by('payment_date')
        elif self.value() == 'reward':
            r = queryset.filter(payment_type='reward').order_by('payment_date')
        elif self.value() == 'fine':
            r = queryset.filter(payment_type='fine').order_by('payment_date')
        elif self.value() == 'other':
            r = queryset.filter(payment_type='other').order_by('payment_date')
        elif self.value() == 'otherm':
            r = queryset.filter(payment_type='otherm').order_by('payment_date')
        elif self.value() == 'snapp':
            r = queryset.filter(payment_type='snapp').order_by('payment_date')
        else:
            r = queryset

        return r
        
        
class AmountForm(forms.ModelForm):
    class Meta:
        model = EmployeePayment
        exclude = []
        widgets = {
            'payment_cost': forms.NumberInput(attrs={'size': 100,'min':0}),
        }

class EmployeePaymentAdmin(admin.ModelAdmin):
    form = AmountForm
    readonly_fields = ['payment_recede']
    
    change_form_template = 'epayment_change_form.html'

    ordering = ['payment_do_date']

    search_fields = ['payment_person__name']

    fields = ['payment_title', 'payment_type', 'payment_date', 'payment_do_date', 'payment_cost', 'payment_person','accounts',
              'payment_description', 'payment_status', 'payment_recede','get_image',
              'payment_add_user', 'payment_add_date', 'payment_confirm_user', 'payment_confirm_date',
              'payment_pay_user', 'payment_pay_date',
              'payment_change_user', 'payment_change_date','payment_account_bank']

    list_filter = [PaymentStatusFilter,PaymentTypeFilter,'payment_do_date',BranchFilterE]

    list_display = ['getid','payment_title','payment_description','get_date','payment_type','payment_cost','payment_person','getcard','status']

    autocomplete_fields = ['payment_person','payment_account_bank']
    
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
        else:
            # link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" >پرداخت شده</span>'
            link = '<span style="padding:5px;border-radius:5px;background: #dff0d8;" ><i class="fas fa-check-double"></i></span>'


        return mark_safe(link)

    status.short_description = "وضعیت"

    def getcard(self,obj):
        if obj.payment_account_bank:
            return obj.payment_account_bank.card
        elif obj.payment_person.banks.all().count()>0:
            return obj.payment_person.banks.all()[0].card
        else:
            return '-'

    getcard.short_description = 'شماره کارت'

    def get_date(self,obj):
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

        if obj.payment_type != 'help' :
            return '%s %s'%(months[obj.payment_do_date.month-1],obj.payment_do_date.year)
        else:
            days = (
                (0, 'شنبه'),
                (1, 'یکشنبه'),
                (2, 'دوشنبه'),
                (3, 'سه شنبه'),
                (4, 'چهارشنبه'),
                (5, 'پنجشنبه'),
                (6, 'جمعه'),
            )

            l = '%s - %s' % (obj.payment_date, days[obj.payment_date.weekday()][1])
            # l = '%s %s' % (obj.payment_due_date, days[obj.payment_due_date.weekday()][1])
            if obj.payment_status == 'paid' or obj.payment_status == 3:
                return l
            t = jdatetime.datetime.today().strftime('%Y-%m-%d')
            if obj.payment_date.strftime('%Y-%m-%d') < t:
                link = '<span style="padding:0 5px;border-radius:5px;background: #f25252;" >%s</span>' % l
            elif obj.payment_date.strftime('%Y-%m-%d') == t:
                link = '<span style="padding:0 5px;border-radius:5px;background: #f9e36b;" >%s</span>' % l
            else:
                link = '<span style="padding:0 5px;border-radius:5px;background: #98f970;" >%s</span>' % l

            return mark_safe(link)

    get_date.short_description = 'ماه حقوقی'
    get_date.admin_order_field = 'payment_do_date'


    # def get_readonly_fields(self, request, obj=None):

    #     if not request.user.is_superuser:
    #         if obj == None:
    #             return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
    #                     'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
    #                     'payment_change_date', ]

    #         elif obj.payment_status == 'confirmed' or obj.payment_status == 'paid':
    #             result = list(set(
    #                 [field.name for field in self.opts.local_fields] +
    #                 [field.name for field in self.opts.local_many_to_many]
    #             ))

    #             result.remove('id')
    #             return result
    #         else:
    #             if request.user.has_perm('AmadoFinance.can_see_fund'):
    #                 result = list(set(
    #                     [field.name for field in self.opts.local_fields] +
    #                     [field.name for field in self.opts.local_many_to_many]
    #                 ))
    #                 result.remove('id')
    #                 return result

    #             return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
    #                     'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
    #                     'payment_change_date']
    #     return list()
    def get_readonly_fields(self, request, obj=None):
        
        if not request.user.is_superuser:
            if obj == None:
                if request.user.has_perm('AmadoFinance.can_confirm_fund'):
                    return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date','accounts','get_image' ]
                return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date','accounts','get_image' ]
                
            elif obj.payment_status == 'confirmed':
                if request.user.has_perm('AmadoFinance.can_confirm_fund'):
                    return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date','accounts','get_image' ]
                result = list(set(
                    [field.name for field in self.opts.local_fields] +
                    [field.name for field in self.opts.local_many_to_many]+['accounts','get_image']
                ))

                result.remove('id')
                return result
            elif obj.payment_status == 'paid':
                result = list(set(
                    [field.name for field in self.opts.local_fields] +
                    [field.name for field in self.opts.local_many_to_many]+['accounts','get_image']
                ))

                result.remove('id')
                return result
            else:
                if request.user.has_perm('AmadoFinance.can_see_fund'):
                    result = list(set(
                        [field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]+['accounts','get_image']
                    ))
                    result.remove('id')
                    return result
                
                if request.user.has_perm('AmadoFinance.can_confirm_fund'):
                    return ['payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date','accounts','get_image']
                return ['payment_status', 'payment_add_user', 'payment_add_date', 'payment_confirm_user',
                        'payment_confirm_date', 'payment_pay_user', 'payment_pay_date', 'payment_change_user',
                        'payment_change_date','accounts','get_image']
        return list(['accounts','get_image'])


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


    def confirm(self, request, qs):
        role = request.user.groups.all()[0].name
        # if not request.user.has_perm('AmadoFinance.can_confirm_fund'):
        #     messages.error(request, "شما اجازه تایید ندارید")
        #     return
        flag = False
        for q in qs:
            if q.payment_status == 'paid':
                flag = True
        # if not flag:
        if True:#TODO
            for q in qs:
                q.payment_status = 'confirmed'
                q.payment_confirm_user = request.user
                q.payment_confirm_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i رکورد تایید شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان تایید برخی یا همه رکورد ها وجود ندارد")

    confirm.short_description = 'تایید رکورد های انتخاب شده'

    def decline(self, request, qs):
        role = request.user.groups.all()[0].name
        if not request.user.has_perm('AmadoFinance.can_decline_fund'):
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
            self.message_user(request, "%i رکورد رد شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان رد برخی یا همه رکورد ها وجود ندارد")

    decline.short_description = 'رد رکورد های انتخاب شده'

    def pay(self, request, qs):
        role = request.user.groups.all()[0].name
        # if not request.user.has_perm('AmadoFinance.can_pay_cash'):
        #     messages.error(request, "شما اجازه پرداخت رکورد را ندارید")
        #     return
        flag = False
        for q in qs:
            if q.payment_status != 'confirmed':
                flag = True
        # if not flag: #TODO
        if True:
            for q in qs:
                q.payment_status = 'paid'
                q.payment_pay_user = request.user
                q.payment_pay_date = jdatetime.datetime.now()
                q.save()
            self.message_user(request, "%i رکورد پرداخت شد" % qs.count())
            return qs
        else:
            messages.error(request, "امکان پرداخت برخی یا همه رکورد ها وجود ندارد")

    pay.short_description = 'اعمال / پرداخت رکورد های انتخاب شده'

    actions = [ confirm,pay,decline ]

    def getid(self, obj):
        return obj.pk

    getid.short_description = 'شناسه'
    getid.admin_order_field = 'id'

    
class BaseAgreementAdmin(admin.ModelAdmin):
    list_display = ['person','base','two_shift','date']
    autocomplete_fields = ['person']
    search_fields = ['person__name']

from AmadoWH.mysite import site

site.register(Person,PersonAdmin)
site.register(Division)
site.register(Role,RoleAdmin)
site.register(RoleHistory)
site.register(Salary,SalaryAdmin)
site.register(SalaryDetail,SalaryDetailAdmin)
site.register(Work,WorkAdmin)
site.register(WorkDetail,WorkDetailAdmin)
site.register(EmployeePayment,EmployeePaymentAdmin)
site.register(LawConstant)
site.register(BaseAgreement,BaseAgreementAdmin)