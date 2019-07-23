from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from AmadoFinance.models import BankAccount
from django.utils.safestring import mark_safe
import jdatetime
class Division(models.Model):
    title = models.CharField(max_length=128,verbose_name='عنوان')
    is_for_factory = models.BooleanField(verbose_name='بخش آماده سازی می باشد',default=False)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بخش'
        verbose_name_plural = "بخش ها"
        permissions = (
            ("can_see_division", "می تواند مشاهده کند"),
        )


class Role(models.Model):
    title = models.CharField(max_length=128, verbose_name='عنوان')
    division = models.ForeignKey(Division,verbose_name='بخش مربوطه',on_delete=models.CASCADE)
    branch = models.ManyToManyField('AmadoWHApp.Branch',verbose_name='شعبه مربوطه')

    def __str__(self):
        return '%s شعبه %s'%(self.title,self.branch.last())

    class Meta:
        verbose_name = 'نقش'
        verbose_name_plural = "نقش ها"
        permissions = (
            ("can_see_role", "می تواند مشاهده کند"),
        )

class Person(models.Model):
    name = models.CharField(max_length=128,verbose_name='نام')
    nat_id = models.CharField(max_length=10,verbose_name='شماره ملی',null=True,blank=True)
    birth_day = jmodels.jDateField(verbose_name='تاریخ تولد',null=True,blank=True)
    image = models.FileField(upload_to='AmadoWH/static/Staff/Picture', null=True, blank=True, verbose_name="عکس پرسنلی")
    kart_melli = models.FileField(upload_to='AmadoWH/static/Staff/ID', null=True, blank=True, verbose_name="کارت ملی و شناسنامه")
    behdasht = models.FileField(upload_to='AmadoWH/static/Staff/Health', null=True, blank=True, verbose_name="کارت بهداشت")
    sooepishine = models.FileField(upload_to='AmadoWH/static/Staff/Sooepishine', null=True, blank=True, verbose_name="گواهی عدم سوء پیشینه")
    banks = models.ManyToManyField('AmadoFinance.BankAccount',verbose_name='حساب های فرد',related_name='pbankp',null=True,blank=True)
    
    # two_shift = models.BooleanField('حضور دو شیفت',default=True)
    childs = models.IntegerField(verbose_name='تعداد فرزندان',default=0)
    
    rem_vacations = models.FloatField(verbose_name='مرخصی مانده از سال %i'%(jdatetime.datetime.now().year-1),default=0)

    insurance_start_date = jmodels.jDateField(verbose_name='تاریخ شروع بیمه',null=True,blank=True)
    insurance_finish_date = jmodels.jDateField(verbose_name='تاریخ پایان بیمه',null=True,blank=True)

    def __str__(self):
        r = RoleHistory.objects.filter(person__id=self.id).order_by('start_date').last().role
        role = Role.objects.get(id=r.id)
        return '%s %s'%(self.name,r)

    class Meta:
        verbose_name = 'فرد'
        verbose_name_plural = "افراد"
        permissions = (
            ("can_see_person", "می تواند مشاهده کند"),
        )


class LawConstant(models.Model):
    date = jmodels.jDateField(verbose_name='تاریخ قانون', default=jdatetime.datetime.today().strftime('%Y-%m-%d'),unique=True)

    vezarat_kar_base = models.IntegerField(verbose_name='حقوق پایه وزارت کار', default=11112690)
    maskan_base = models.IntegerField(verbose_name='پایه حق مسکن', default=400000)  # 400000/31 * hoghoogh
    min_child = models.IntegerField(verbose_name='حداقل تعداد فرزند', default=1)  #0=0,1 = *3,>1 = *6
    bon_base = models.IntegerField(verbose_name='پایه حق بن', default=1100000)
    year_days = models.IntegerField(verbose_name='تعداد روزهای سال', default=365)
    week_base = models.IntegerField(verbose_name='حداقل ساعات کار ماهانه', default=220)  # 220
    extra_percentage = models.FloatField(verbose_name='درصد اضافه کاری', default=1.4)  # 1.4
    bime_percentage = models.FloatField(verbose_name='درصد بیمه', default=7)  # 7
    tax_bime_ratio = models.FloatField(verbose_name='کسر بیمه مالیات', default=0.28571429)  # 2/7
    tax_percentage = models.IntegerField(verbose_name='درصد مالیات', default=10)  # 10%
    kargar_bime_ratio1 = models.FloatField(verbose_name='درصد حق کارگر در بیمه', default=23)
    tax_min = models.IntegerField(verbose_name='حداقل پایه حقوق برای محاسبه مالیات',default=23000000)

    delivery_base = models.IntegerField(verbose_name='پایه حق پیک',default=10000)
    salad_base = models.IntegerField(verbose_name='پایه حق سالاد',default=10000)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = 'ثابت حقوقی'
        verbose_name_plural = "ثابت های حقوقی"
        permissions = (
            ("can_see_lawconstant", "می تواند مشاهده کند"),
        )


class BaseAgreement(models.Model):
    # date = jmodels.jDateField(verbose_name='تاریخ توافق',default=jdatetime.datetime.today().strftime('%Y-%m-%d'))
    date = jmodels.jDateField(verbose_name='تاریخ توافق',default='1397-05-01')
    person = models.ForeignKey(Person,verbose_name='فرد',on_delete=models.CASCADE)

    base = models.IntegerField(verbose_name='مبلغ توافقی')
    two_shift = models.BooleanField('حضور دو شیفت', default=True)
    
    snapp_fee = models.IntegerField(verbose_name='حق اسنپ',default=0)


    def __str__(self):
        return '%s %s' % (self.person, self.date)

    class Meta:
        verbose_name = 'توافق حقوقی'
        verbose_name_plural = "توافقات حقوقی"
        permissions = (
            ("can_see_agreement", "می تواند مشاهده کند"),
        )

class RoleHistory(models.Model):
    start_date = jmodels.jDateField(verbose_name='تاریخ شروع')
    finish_date = jmodels.jDateField(verbose_name='تاریخ پایان',null=True,blank=True)

    person = models.ForeignKey(Person,verbose_name='فرد',on_delete=models.CASCADE)
    role = models.ForeignKey(Role,verbose_name='نقش',on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.title

    class Meta:
        verbose_name = 'تاریخچه نقش'
        verbose_name_plural = "تاریخچه ها"
        permissions = (
            ("can_see_rolehistory", "می تواند مشاهده کند"),
        )


class SalaryDetail(models.Model):  # all rial
    person = models.ForeignKey(Person, verbose_name='فرد', on_delete=models.CASCADE)

    salary = models.ForeignKey('Salary', verbose_name='پرونده حقوق مربوطه', on_delete=models.CASCADE)

    days = models.IntegerField(verbose_name='تعداد روزهای کارکرد')
    fix = models.IntegerField(verbose_name='حقوق ثابت')
    base = models.IntegerField(verbose_name='حقوق پایه دوره')
    agreement = models.IntegerField(verbose_name='حقوق توافقی دوره')
    maskan = models.IntegerField(verbose_name='حق مسکن')
    childs = models.IntegerField(verbose_name='تعداد فرزند')  # if childs > 3 or ...
    childs_money = models.IntegerField(verbose_name='حق اولاد')
    bon = models.IntegerField(verbose_name='بن')
    sanavat = models.IntegerField(verbose_name='سنوات')
    hoghoogh_vezarat_kar_tot = models.IntegerField(verbose_name='جمع حقوق وزارت کار')
    positive_taraz = models.IntegerField(verbose_name='تراز مثبت')
    mazaya = models.IntegerField(verbose_name='مزایای شغلی',null=True,blank=True)
    extra_shift = models.FloatField(verbose_name='شیفت اضافه')
    extra_shift_fee = models.IntegerField(verbose_name='مزد شیفت اضافه')
    del_sal = models.IntegerField(verbose_name='پیک/سالاد')
    del_sal_fee = models.IntegerField(verbose_name='حق پیک/سالاد')
    
    vacation_rem = models.FloatField(verbose_name='مرخصی نرفته')
    vacation_rem_fee = models.IntegerField(verbose_name='حق طلب مرخصی')
    eydi = models.IntegerField(verbose_name='عیدی')
    
    off = models.FloatField(verbose_name='ایام تعطیل کاری')
    off_fee = models.IntegerField(verbose_name='مبلغ تعطیل کاری')
    extra_hours = models.IntegerField(verbose_name='ساعت اضافه کاری',null=True,blank=True)
    extra_hours_fee = models.IntegerField(verbose_name='مبلغ اضافه کاری')
    reward = models.IntegerField(verbose_name='پاداش',null=True,blank=True)
    snapp = models.IntegerField(verbose_name='حق اسنپ',null=True,blank=True)
    hoghoogh_mazaya_plus = models.IntegerField(verbose_name='جمع حقوق و مزایا')
    help = models.IntegerField(verbose_name='مساعده',null=True,blank=True)
    negative_taraz = models.IntegerField(verbose_name='تراز منفی')
    other_deduction = models.IntegerField(verbose_name='سایر کسورات',null=True,blank=True)
    fine = models.IntegerField(verbose_name='جریمه',null=True,blank=True)
    bime = models.IntegerField(verbose_name='بیمه',null=True,blank=True)
    maliat = models.IntegerField(verbose_name='مالیات',null=True,blank=True)
    kosoorat_sum = models.IntegerField(verbose_name='جمع کسورات')
    pardakhti = models.IntegerField(verbose_name='حقوق پرداختی')
    karfarma_bime = models.IntegerField(verbose_name='بیمه سهم کارفرما')

    account = models.ForeignKey('AmadoFinance.BankAccount',on_delete=models.CASCADE,verbose_name='حساب بانکی')

    description = models.TextField(max_length=512,verbose_name='توضیحات',null=True,blank=True)



    status = (
        ('registered', 'ثبت شده/در انتظار تایید'),
        ('confirmed', 'تایید شده/در انتظار امضای تسویه'),
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('error', 'نقص مدارک'),
    )

    payment_status = models.CharField(choices=status, max_length=16, verbose_name='وضعیت حقوقی',
                                      default='registered')

    add_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ثبت کننده",
                                 related_name="salary_register_user", null=True, blank=True)
    add_date = jmodels.jDateTimeField(null=False, blank=False, verbose_name="تاریخ ثبت",
                                       default=jdatetime.datetime.now)
                                    #   default="1397-03-28 20:38:00")

    confirm_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",
                                     related_name="salary_confirm_user", null=True, blank=True)
    confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                           default=jdatetime.datetime.now,
                                        #   default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")

    # عیدی پارامتر های تسویه حساب
    # تسویه حساب هست یا نه


    def __str__(self):
         return '%s %s'%(self.person.name,self.salary.month)

    class Meta:
        unique_together = ('person', 'salary',)
        verbose_name = 'جزئیات حقوق'
        verbose_name_plural = "جزئیات حقوق ها"
        permissions = (
            ("can_see_salary_det", "می تواند مشاهده کند"),
        )

class Salary(models.Model):
    month = jmodels.jDateField(verbose_name='ماه')
    branch = models.ForeignKey('AmadoWHApp.Branch', on_delete=models.CASCADE, verbose_name="شعبه",null=True,blank=True)
    
    from_date = jmodels.jDateField(verbose_name='از تاریخ',null=True,blank=True)
    to_date = jmodels.jDateField(verbose_name='تا تاریخ',null=True,blank=True)

    def __str__(self):
        return 'حقوق ماه %s شعبه %s' % (self.month, self.branch)

    class Meta:
        verbose_name = 'حقوق'
        verbose_name_plural = "حقوق ها"
        permissions = (
            ("can_see_salary", "می تواند مشاهده کند"),
        )



class Work(models.Model):
    date = jmodels.jDateField(verbose_name="تاریخ", default=jdatetime.datetime.today().strftime("%Y-%m-%d"))
    branch = models.ForeignKey('AmadoWHApp.Branch', on_delete=models.CASCADE, verbose_name="شعبه")

    status = (
        ('registered', 'ثبت شده/در انتظار تایید'),
        ('confirmed', 'تایید شده'),
    )

    status = models.CharField(choices=status, max_length=16, verbose_name="وضعیت", default='confirmed')

    add_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ثبت کننده",
                                 related_name="work_register_user", null=True, blank=True)
    add_date = jmodels.jDateTimeField(null=False, blank=False, verbose_name="تاریخ ثبت",
                                      default=jdatetime.datetime.now)
                                      # default="1397-03-28 20:38:00")

    confirm_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",
                                     related_name="work_confirm_user", null=True, blank=True)
    confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                          default=jdatetime.datetime.now,
                                          # default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")

    def __str__(self):
        return 'کارکرد روز %s شعبه %s' % (self.date, self.branch)

    class Meta:
        verbose_name = 'کارکرد'
        verbose_name_plural = "کارکرد ها"
        permissions = (
            ("can_see_work", "می تواند مشاهده کند"),
        )

class WorkDetail(models.Model):#all rial
    person = models.ForeignKey(Person,verbose_name='فرد',on_delete=models.CASCADE)

    work = models.ForeignKey(Work,verbose_name='پرونده کارکرد مربوطه',on_delete=models.CASCADE)
    work_delivery_salad = models.IntegerField(verbose_name='تعداد پیک/سالاد',null=True,blank=True)

    status = (
        ('P','حضور یک شیفت'),
        ('PP','حضور دو شیفت'),
        ('V','مرخصی'),
        ('T','ترانسفر'),
        ('O','آف'),
        ('A','غیبت'),
        ('Q','استعفا'),
    )

    work_status = models.CharField(choices=status,max_length=16,verbose_name='وضعیت حضور',default='P')


    class Meta:
        unique_together = ('person', 'work',)
        verbose_name = 'جزئیات کارکرد'
        verbose_name_plural = "جزئیات کارکرد ها"
        permissions = (
            ("can_see_work_det", "می تواند مشاهده کند"),
        )
        
class EmployeePayment(models.Model):
    status = (
        ('registered', 'ثبت شده/در انتظار تایید'),
        ('confirmed', 'تایید شده/در انتظار پرداخت'),
        ('rejected', 'رد شده'),
        ('paid', 'پرداخت شده'),
    )

    type = (

        ('help', 'مساعده'),
        ('reward', 'پاداش'),
        ('fine', 'جریمه'),
        ('other', 'سایر کسورات'),
        ('otherm', 'سایر مزایا'),
        ('snapp', 'حق اسنپ'),
    )

    payment_title = models.CharField(verbose_name="عنوان", max_length=128, null=True, blank=True)
    payment_description = models.TextField(verbose_name="توضیحات", max_length=256, null=True, blank=True)

    payment_date = jmodels.jDateField(null=False, blank=False,
                                          default=jdatetime.datetime.today().strftime("%Y-%m-%d"),
                                          verbose_name="تاریخ پرداخت")
    payment_do_date = jmodels.jDateField(null=False, blank=False,
                                      default=jdatetime.datetime.today().strftime("%Y-%m-%d"),
                                      verbose_name="تاریخ اعمال")
    payment_type = models.CharField(choices=type,verbose_name='نوع',default='help',max_length=16)
    payment_cost = models.IntegerField(verbose_name="مبلغ پرداختی(ریال)", )
    payment_person = models.ForeignKey(Person, verbose_name="فرد", on_delete=models.CASCADE, null=False,blank=False)

    payment_account_bank = models.ForeignKey(BankAccount, verbose_name="حساب بانکی", on_delete=models.CASCADE,null=True, blank=True)

    payment_add_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ثبت کننده",
                                         related_name="hrf_register_user", null=True, blank=True)
    payment_add_date = jmodels.jDateTimeField(null=False, blank=False, verbose_name="تاریخ ثبت",
                                              default=jdatetime.datetime.now)
                                            #   default="1397-03-28 20:38:00")

    payment_confirm_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",
                                             related_name="hrf_confirm_user", null=True, blank=True)
    payment_confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                                  default=jdatetime.datetime.now,
                                                #   default="1397-03-28 20:38:00",
                                                  verbose_name="تاریخ تایید")

    payment_pay_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="پرداخت کننده",
                                         related_name="hrf_pay_user", null=True, blank=True)
    payment_pay_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
                                            #   default="1397-03-28 20:38:00",
                                              verbose_name="تاریخ تایید")

    payment_change_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تغییر دهنده",
                                            related_name="hrf_change_user", null=True, blank=True)
    payment_change_date = jmodels.jDateTimeField(null=False, blank=False,
                                                  default=jdatetime.datetime.now,
                                                #  default="1397-03-28 20:38:00",
                                                 verbose_name="تاریخ تغییر")

    payment_recede = models.ImageField(upload_to='AmadoWH/static/HRFRecede',null=True,blank=True,verbose_name="فایل رسید")


    payment_status = models.CharField(choices=status, max_length=16, verbose_name="وضعیت پرداخت", default='registered')

    def accounts(self):

        if not self.payment_person:
            return '-'
        supplier = self.payment_person
        accounts = supplier.banks
        if accounts.count() == 0:
            return '-'
        accounts = accounts.all()

        str = '<table style="text-align:center">'
        str += '<tr>'
        str += '<th>بانک</th>'
        str += '<th>نام دارنده حساب</th>'
        str += '<th>کارت</th>'
        str += '<th>حساب</th>'
        str += '<th>شبا</th>'
        str += '</tr>'


        for a in accounts:
            str += '<tr>'
            str += '<td>%s</td>'%a.bank
            str += '<td>%s</td>'%a.person
            str += '<td>%s</td>'%a.card
            str += '<td>%s</td>'%a.account
            str += '<td>%s</td>'%a.shaba
            str += '</tr>'
        str += '</table>'

        print('hi')

        return mark_safe(str)

    accounts.short_description = 'حساب های فرد'

    def get_image(self):
        return mark_safe('<a target=_blank href="/%s" ><img src="/%s" style="width:100px;height:100px;"/></a>' % (
        self.payment_recede.url, self.payment_recede.url))
    get_image.short_description = 'رسید'

    def __str__(self):
        return "%i: بابت %s تاریخ %s در وجه %s" % (
            self.pk, self.payment_type, self.payment_date, self.payment_person,)

    class Meta:
        verbose_name = 'مساعده/جریمه/پاداش'
        verbose_name_plural = "مساعده ها / جریمه ها / پاداش ها ..."
        permissions = (
            ("can_see_hrf", "می تواند مشاهده کند"),
            ("can_confirm_hrf", "می تواند تایید کند"),
            ("can_pay_hrf", "می تواند پرداخت کند"),
            ("can_change_status_hrf", "می تواند وضعیت را تغییر دهد"),
        )