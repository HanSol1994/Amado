from django.db import models
from django.contrib.auth.models import User
import jdatetime
from django_jalali.db import models as jmodels

from django.utils.safestring import mark_safe

# Create your models here.
from AmadoWHApp.models import Branch, Supplier



class Pos(models.Model):
    pos_serial = models.CharField(max_length=128,verbose_name="سریال پوز",unique=True)
    pos_branch = models.ForeignKey(Branch,on_delete=models.CASCADE,verbose_name="شعبه مربوطه")
    
    pos_bank = models.ForeignKey('Bank',verbose_name='بانک پوز',on_delete=models.SET_NULL,null=True,blank=True)
    pos_is_mobil = models.BooleanField(default=False,verbose_name='پوز سیار است',)
    
    pos_is_active = models.BooleanField(default=True,verbose_name='پوز فعال است',)
    
    def __str__(self):
        if self.pos_is_mobil:
            return ('پوز سیار بانک %s به شماره %s شعبه %s') % (self.pos_bank, self.pos_serial, self.pos_branch)
        else:
            return ('پوز ثابت بانک %s به شماره %s شعبه %s') % (self.pos_bank, self.pos_serial,self.pos_branch)

    class Meta:
        verbose_name = "پوز"
        verbose_name_plural = "پوز ها"
        permissions = (
            ("can_see_pos", "می تواند مشاهده کند"),
        )

class PosSale(models.Model):
    pos = models.ForeignKey(Pos,verbose_name='پوز مربوطه',on_delete=models.CASCADE,related_name='serial')
    sale = models.ForeignKey('Sales',verbose_name='فروش مربوطه',on_delete=models.CASCADE,related_name='sale')
    cost = models.IntegerField(verbose_name="مبلغ(ریال)")

    def __str__(self):
        return self.pos.pos_serial

    class Meta:
        unique_together = ('pos', 'sale',)
        verbose_name = "فروش پوز"
        verbose_name_plural = "فروش های پوز ها"
        permissions = (
            ("can_see_pos_sale", "می تواند مشاهده کند"),
        )


class InternetSeller(models.Model):
    name = models.CharField(max_length=64,verbose_name="نام وبسایت")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "وبسایت فروش"
        verbose_name_plural = "وبسایت های فروش"
        permissions = (
            ("can_see_wesite", "می تواند مشاهده کند"),
        )


class InternetSale(models.Model):
    website = models.ForeignKey(InternetSeller,verbose_name='سایت',on_delete=models.CASCADE,related_name='website')
    sale = models.ForeignKey('Sales',verbose_name='فروش مربوطه',on_delete=models.CASCADE,related_name='wsale')
    cost = models.IntegerField(verbose_name="مبلغ(ریال)")

    def __str__(self):
        return self.website.name

    class Meta:
        unique_together = ('website', 'sale',)
        verbose_name = "فروش اینترنتی"
        verbose_name_plural = "فروش های اینترنتی"
        permissions = (
            ("can_see_website_sale", "می تواند مشاهده کند"),
        )


class Sales(models.Model):
    
    status = (
        ('registered','ثبت شده'),
        ('closed','بسته شده'),
        ('changed','تغییر کرده'),
        ('tryagain','نیاز به بررسی'),
    )
    
    sales_branch = models.ForeignKey(Branch, verbose_name="شعبه مربوطه", on_delete=models.CASCADE, null=True,blank=True)
    sales_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر ثبت کننده", null=True,blank=True)
    sales_add_date = jmodels.jDateField(verbose_name="تاریخ ثبت", default=jdatetime.datetime.today().strftime("%Y-%m-%d"))
    sales_date = jmodels.jDateField(verbose_name="تاریخ فروش", default=jdatetime.datetime.today().strftime("%Y-%m-%d"))

    sales_cash_cost = models.IntegerField(verbose_name="جمع نقدی(ریال)")

    sales_salon = models.IntegerField(verbose_name="تعداد فیش سالن")

    sales_delivery = models.IntegerField(verbose_name="تعداد فیش دلیوری")
    
    
    sales_salon_cancel = models.IntegerField(verbose_name="تعداد فیش  حذفی سالن")
    sales_salon_cancel_cost = models.IntegerField(verbose_name='جمع مبلغ حذفی سالن')

    sales_delivery_cancel = models.IntegerField(verbose_name="تعداد فیش حذفی دلیوری")
    sales_delivery_cancel_cost = models.IntegerField(verbose_name="جمع مبلغ فیش حذفی دلیوری")

    sales_tot_cash_cost = models.IntegerField(verbose_name="کل مبلغ فروش(ریال)")
    sales_delivery_cost = models.IntegerField(verbose_name="مبلغ دلیوری(ریال)")

    sales_status = models.CharField(max_length=16,choices=status,verbose_name='وضعیت',default='closed')


    sales_close_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",
                                             related_name="closes_user", null=True, blank=True)
    sales_close_date = jmodels.jDateTimeField(null=False, blank=False,
                                                  default=jdatetime.datetime.now,
#                                                   default="1397-06-31 00:09:00.000000",
                                                  verbose_name="تاریخ تایید")

    sales_try_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="رد کننده",
                                         related_name="try_user", null=True, blank=True)
    sales_try_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                               default="1397-06-31 00:09:00.000000",
                                              verbose_name="تاریخ رد")

    sales_change_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تغییر دهنده",
                                            related_name="changes_user", null=True, blank=True)
    sales_change_date = jmodels.jDateTimeField(null=False, blank=False,
                                                  default=jdatetime.datetime.now,
#                                                  default="1397-06-31 00:09:00.000000",
                                                 verbose_name="تاریخ تغییر")

    
    def totm(self):
        return mark_safe('<span id ="tot_fill"></span>')
    totm.short_description = 'جمع کل'

    def balancem(self):
        return mark_safe('<span id ="balance_fill"></span>')

    balancem.short_description = 'بالانس'


    def __str__(self):
        return "فروش شعبه %s در تاریخ %s"%(self.sales_branch,self.sales_date)

    class Meta:
        verbose_name = 'فروش'
        verbose_name_plural = "فروش ها"
        permissions = (
            ("can_see_sales", "می تواند مشاهده کند"),
            ("can_close_sales", "می تواند ببندد"),
            ("can_edit_sales", "می تواند ویرایش کند"),
        )


class RecipientCompany(models.Model):
    recipient_name = models.CharField(verbose_name="نام شرکت گیرنده",max_length=128)
    recipient_description = models.TextField(verbose_name="توضیحات شرکت",max_length=256,blank=True,null=True)

    def __str__(self):
        return "%s"%(self.recipient_name)

    class Meta:
        verbose_name = 'گیرنده'
        verbose_name_plural = "گیرندگان"
        permissions = (
            ("can_see_recipientcom", "می تواند مشاهده کند"),
        )


class Bank(models.Model):
    bank_name = models.CharField(verbose_name="نام بانک", max_length=128)
    bank_description = models.TextField(verbose_name="توضیحات بانک", max_length=256,blank=True,null=True)



    def __str__(self):
        return "%s" % (self.bank_name)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'بانک'
        verbose_name_plural = "بانک ها"
        permissions = (
            ("can_see_bank", "می تواند مشاهده کند"),
        )



class PaymentCategory(models.Model):
    cat_name = models.CharField(verbose_name="نام دسته", max_length=128)
    cat_description = models.TextField(verbose_name="توضیحات دسته", max_length=256,blank=True,null=True)

    def __str__(self):
        return "%s" % (self.cat_name)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'دسته پرداخت'
        verbose_name_plural = "دسته های پرداختی"
        permissions = (
            ("can_see_paycat", "می تواند مشاهده کند"),
        )


class FactorImage(models.Model):
    image_title = models.CharField(null=True,blank=True,verbose_name="عنوان",max_length=64)
    image = models.FileField(upload_to='AmadoWH/static/ChashFactors',null=True,blank=True,verbose_name="فایل تصویر")
    factor = models.ForeignKey('CashPayment',on_delete=models.CASCADE,verbose_name='پرداخت مربوطه',null=True,blank=True)
    fund = models.ForeignKey('FundPayment', on_delete=models.CASCADE, verbose_name='تنخواه مربوطه', null=True,
                             blank=True)
    checkp = models.ForeignKey('CheckPayment', on_delete=models.CASCADE, verbose_name='چک مربوطه', null=True,
                             blank=True)
    cost = models.IntegerField(verbose_name="مبلغ فاکتور(ریال)",null=True,blank=True)
    
    def factor_image(self):
        return mark_safe('<a target=_blank href="/%s" ><img src="/%s" style="height:50px;"/></a>' % (self.image.url,self.image.url))
        # <embed src="http://example.com/the.pdf" width="500" height="375" type='application/pdf'>


    factor_image.short_description = 'تصویر فاکتور'
    factor_image.allow_tags = True

    def __str__(self):
        return "%s" % (self.image_title)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'تصویر فاکتور'
        verbose_name_plural = "تصاویر فاکتور ها"
        permissions = (
            ("can_see_image", "می تواند مشاهده کند"),
        )


class RecedeImage(models.Model):
    payment_due_date = jmodels.jDateField(null=False,blank=False,verbose_name="تاریخ")
    image_title = models.CharField(null=True,blank=True,verbose_name="عنوان",max_length=64)
    image = models.FileField(upload_to='AmadoWH/static/ChashRecedes',null=True,blank=True,verbose_name="فایل تصویر")
    factor = models.ForeignKey('CashPayment',on_delete=models.CASCADE,verbose_name='پرداخت مربوطه',null=True,blank=True)
    fund = models.ForeignKey('FundPayment',on_delete=models.CASCADE,verbose_name='تنخواه مربوطه',null=True,blank=True)
    cost = models.IntegerField(verbose_name="مبلغ رسید(ریال)",null=False,blank=False)
    checkp = models.ForeignKey('CheckPayment', on_delete=models.CASCADE, verbose_name='چک مربوطه', null=True,
                             blank=True)
                             
    waste_sell = models.ForeignKey('ActualCost.WasteSale', on_delete=models.CASCADE, verbose_name='فروش ضایعات', null=True,
                             blank=True)                         
                             
    salary = models.ForeignKey('AmadoAccounting.SalaryDetail', on_delete=models.CASCADE, verbose_name='حقوق مربوطه',null=True,blank=True)                             
    
    def_account = models.ForeignKey('AmadoWHApp.Branch',related_name='defacheck', on_delete=models.SET_NULL,null=True,blank=True, verbose_name="حساب معین")

    
    def factor_image(self):
        return mark_safe('<a target=_blank href="/%s" ><img src="/%s" style="height:50px;"/></a>' % (self.image.url,self.image.url))
    
      
    
        # return mark_safe('<a target=_blank href="/%s" ><embed src="/%s" style="max-height:100px;max-width:50px;"/></a>' % (self.image.url,self.image.url))

    factor_image.short_description = 'تصویر رسید'
    factor_image.allow_tags = True

    def __str__(self):
        return "%s" % (self.image_title)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'تصویر رسید'
        verbose_name_plural = "تصاویر رسید ها"
        permissions = (
            ("can_see_image", "می تواند مشاهده کند"),
        )

def get_full_name(self):
    return self.get_full_name()

User.add_to_class("__str__", get_full_name)
class CashPayment(models.Model):

    status = (
        ('registered', 'ثبت شده/در انتظار تایید'),
        ('confirmed', 'تایید شده/در انتظار پرداخت'),
        ('rejected','رد شده'),
        ('paid','پرداخت شده'),
    )

    account_type=(
        ('card','کارت'),
        ('account','حساب'),
        ('shaba','شبا'),
        ('pos', 'پوز'),
    )

    payment_title = models.CharField(verbose_name="عنوان پرداخت", max_length=128,null=True,blank=True)
    payment_description = models.TextField(verbose_name="توضیحات پرداخت", max_length=256,null=True,blank=True)

    payment_due_date = jmodels.jDateField(null=False,blank=False,default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ پرداخت")
    payment_cost = models.IntegerField(verbose_name="مبلغ پرداختی(ریال)",)
    payment_cause = models.ForeignKey(PaymentCategory,verbose_name="بابت",on_delete=models.CASCADE)
    payment_recipient = models.ForeignKey(RecipientCompany,verbose_name="گیرنده",on_delete=models.CASCADE,null=False,blank=False)
    # payment_card = models.CharField(verbose_name="شماره کارت",max_length=19,null=True,blank=True)
    # payment_card_person = models.CharField(verbose_name="نام صاحب کارت",max_length=64,null=True,blank=True)
    # payment_card_bank = models.ForeignKey(Bank, verbose_name="بانک کارت", null=True, blank=True,on_delete=models.CASCADE,related_name="card_bank")
    payment_account = models.CharField(verbose_name="شماره",max_length=64)
    payment_account_type = models.CharField(choices=account_type,verbose_name="نوع شماره",max_length=64,default='card')
    payment_account_person = models.CharField(verbose_name="نام صاحب شماره",max_length=64,null=True,blank=True)
    payment_account_bank = models.ForeignKey(Bank,verbose_name="بانک",on_delete=models.CASCADE,related_name="account_bank",null=True,blank=True)
    # payment_SHABA = models.CharField(verbose_name="شماره شبا",max_length=64,null=True,blank=True,default='IR')
    # payment_SHABA_person = models.CharField(verbose_name="نام صاحب شبا",max_length=64,null=True,blank=True)
    # payment_SHABA_bank = models.ForeignKey(Bank, verbose_name="بانک شبا", null=True, blank=True,on_delete=models.CASCADE,related_name="shaba_bank")

    # payment_factor = models.ImageField(upload_to='AmadoWH/static/ChashFactors',null=True,blank=True,verbose_name="عکس فاکتور")
    # payment_factors = models.ManyToManyField(Image,null=True,blank=True,verbose_name="تصویر فاکتور",related_name="factors")

    payment_add_user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ثبت کننده",related_name="register_user",null=True,blank=True)
    payment_add_date = jmodels.jDateTimeField(null=False,blank=False,verbose_name="تاریخ ثبت",
                                              default=jdatetime.datetime.now)
#                                               default="1397-03-28 20:38:00")

    payment_confirm_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",related_name="confirm_user",null=True,blank=True)
    payment_confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                                  default=jdatetime.datetime.now,
#                                                   default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")

    payment_pay_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="پرداخت کننده",related_name="pay_user",null=True,blank=True)
    payment_pay_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                               default="1397-03-28 20:38:00",
                                                  verbose_name="تاریخ تایید")

    payment_change_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تغییر دهنده",
                                         related_name="change_user", null=True, blank=True)
    payment_change_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                               default="1397-03-28 20:38:00",
                                              verbose_name="تاریخ تغییر")

    # payment_recede = models.ImageField(upload_to='AmadoWH/static/ChashRecedes',null=True,blank=True,verbose_name="عکس رسید")
    # payment_recedes = models.ManyToManyField(Image, null=True, blank=True, verbose_name="تصویر رسید",related_name="recedes")

    payment_status = models.CharField(choices=status,max_length=16,verbose_name="وضعیت پرداخت",default='registered')
    
    supplier = models.ForeignKey(Supplier, verbose_name='تامین کننده', on_delete=models.CASCADE,null=True,blank=True)
    
    cost_center = models.ForeignKey('CostCenter',related_name='costccash', on_delete=models.CASCADE, verbose_name="مرکز هزینه")
    over_account = models.ForeignKey('ActualCost.OverAccount',related_name='overcash',on_delete=models.CASCADE,verbose_name="حساب کل")
    

    def __str__(self):
        return "%i: بابت %s تاریخ %s در وجه %s" % (self.pk, self.payment_cause, self.payment_due_date, self.payment_recipient,)
        
    def accounts(self):
        if not self.supplier:
            return '-'
        supplier = self.supplier
        accounts = supplier.supplier_account
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

        return mark_safe(str)

    accounts.short_description = 'حساب های تامین کننده'

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'پرداخت'
        # verbose_name_plural = "پرداخت ها"
        verbose_name_plural = 'پرداخت به تامین کنندگان'
        permissions = (
            ("can_see_cash", "می تواند مشاهده کند"),
            ("can_confirm_cash", "می تواند تایید کند"),
            ("can_decline_cash", "می تواند رد کند"),
            ("can_pay_cash", "می تواند پرداخت کند"),
            ("can_change_status_cash", "می تواند وضعیت را تغییر دهد"),
        )


    def factor_image(self):
        return mark_safe('<a target=_blank href="/%s" ><img src="/%s" style="width:100px;height:100px;"/></a>' % (self.payment_factor.url,self.payment_factor.url))

    factor_image.short_description = 'عکس فاکتور'
    factor_image.allow_tags = True


    def recede_image(self):
        return mark_safe('<a target=_blank href="/%s" ><img src="/%s" style="width:100px;height:100px;"/></a>' % (
        self.payment_recede.url, self.payment_recede.url))

    recede_image.short_description = 'عکس رسید'
    recede_image.allow_tags = True


class CheckCategory(models.Model):
    cat_name = models.CharField(verbose_name="نام نوع هزینه", max_length=128)
    cat_description = models.TextField(verbose_name="توضیحات نوع هزینه", max_length=256, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.cat_name)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'نوع هزینه'
        verbose_name_plural = "انواع هزینه"
        permissions = (
            ("can_see_checkcat", "می تواند مشاهده کند"),
        )


class CheckPayment(models.Model):

    status = (
        ('registered', 'ثبت شده/در انتظار تایید'),
        ('confirmed', 'تایید شده/در انتظار پرداخت'),
        ('rejected','رد شده'),
        ('paid','پرداخت شده'),
        ('back','برگشت خورده'),
    )

    check_title = models.CharField(verbose_name="عنوان چک", max_length=128,null=True,blank=True)
    check_description = models.TextField(verbose_name="توضیحات چک", max_length=256,null=True,blank=True)

    check_number = models.CharField(verbose_name="شماره چک", max_length=128,null=True,blank=True)

    check_date = jmodels.jDateField(null=False,blank=False,default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ صدور")
    check_due_date = jmodels.jDateField(null=False,blank=False,default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ چک")
    check_cause = models.ForeignKey(PaymentCategory, verbose_name="بابت", on_delete=models.CASCADE)

    check_payment_type = models.ForeignKey(CheckCategory, verbose_name="نوع هزینه", on_delete=models.CASCADE)

    payment_cost = models.IntegerField(verbose_name="مبلغ چک(ریال)",)
    check_bank = models.ForeignKey(Bank, verbose_name="بانک", on_delete=models.CASCADE,null=True,blank=True,
                                             related_name="caccount_bankc")

    check_recipient = models.ForeignKey(RecipientCompany,verbose_name="دریافت کننده",on_delete=models.CASCADE,null=False,blank=False)


    check_again_date = jmodels.jDateField(null=False, blank=False,
                                        default=jdatetime.datetime.today().strftime("%Y-%m-%d"),
                                        verbose_name="تاریخ مراجعه مجدد به بانک")


    payment_add_user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ثبت کننده",related_name="cregister_userc",null=True,blank=True)
    payment_add_date = jmodels.jDateTimeField(null=False,blank=False,verbose_name="تاریخ ثبت",
                                              default=jdatetime.datetime.now)
#                                               default="1397-03-28 20:38:00")

    payment_confirm_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",related_name="cconfirm_userc",null=True,blank=True)
    payment_confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                                  default=jdatetime.datetime.now,
#                                                   default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")

    payment_pay_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="پرداخت کننده",related_name="cpay_userc",null=True,blank=True)
    payment_pay_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                               default="1397-03-28 20:38:00",
                                                  verbose_name="تاریخ تایید")

    payment_change_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تغییر دهنده",
                                         related_name="cchange_userc", null=True, blank=True)
    payment_change_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                               default="1397-03-28 20:38:00",
                                              verbose_name="تاریخ تغییر")

    payment_status = models.CharField(choices=status,max_length=16,verbose_name="وضعیت چک",default='confirmed')
    
    
    supplier = models.ForeignKey(Supplier, verbose_name='تامین کننده', on_delete=models.CASCADE,null=True,blank=True)
    
    cost_center = models.ForeignKey('CostCenter', on_delete=models.CASCADE, verbose_name="مرکز هزینه")
    over_account = models.ForeignKey('ActualCost.OverAccount',related_name='overccheck',on_delete=models.CASCADE,verbose_name="حساب کل")
#    def_account = models.ForeignKey('AmadoWHApp.Branch',related_name='defacheck', on_delete=models.CASCADE, verbose_name="حساب معین")

    def __str__(self):
        return "%i: بابت %s تاریخ %s در وجه %s" % (self.pk,self.check_cause,self.check_due_date,self.check_recipient,)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'چک'
        verbose_name_plural = "چک ها"
        permissions = (
            ("can_see_check", "می تواند مشاهده کند"),
            ("can_confirm_check", "می تواند تایید کند"),
            ("can_decline_check", "می تواند رد کند"),
            ("can_pay_check", "می تواند پرداخت کند"),
            ("can_back_check", "می تواند برگشت بزند"),
            ("can_change_status_check", "می تواند وضعیت را تغییر دهد"),
        )


class FundPayment(models.Model):

    status = (
        ('registered','ثبت شده/در انتظار تایید'),
        ('confirmed','تایید شده/در انتظار پرداخت'),
        ('rejected','رد شده'),
        ('paid','پرداخت شده/در انتظار تسویه'),
        # ('closed','تسویه شد'),
    )

    account_type=(

        ('card','کارت'),
        ('account','حساب'),
        ('shaba','شبا'),
        ('pos','پوز'),
    )


    payment_title = models.CharField(verbose_name="عنوان تنخواه", max_length=128,null=True,blank=True)
    payment_description = models.TextField(verbose_name="توضیحات تنخواه", max_length=256,null=True,blank=True)

    payment_due_date = jmodels.jDateField(null=False,blank=False,default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ پرداخت")
    payment_cost = models.IntegerField(verbose_name="مبلغ پرداختی(ریال)",)
    payment_cause = models.ForeignKey(PaymentCategory,verbose_name="بابت",on_delete=models.CASCADE)
    payment_recipient = models.ForeignKey(RecipientCompany,verbose_name="گیرنده",on_delete=models.CASCADE,null=False,blank=False)
    # payment_card = models.CharField(verbose_name="شماره کارت",max_length=19,null=True,blank=True)
    # payment_card_person = models.CharField(verbose_name="نام صاحب کارت",max_length=64,null=True,blank=True)
    # payment_card_bank = models.ForeignKey(Bank, verbose_name="بانک کارت", null=True, blank=True,on_delete=models.CASCADE,related_name="card_bank")
    payment_account = models.CharField(verbose_name="شماره",max_length=64,default='6219861035801181')
    payment_account_type = models.CharField(choices=account_type,verbose_name="نوع شماره",max_length=64,default='card',null=True,blank=True)
    payment_account_person = models.CharField(verbose_name="نام صاحب شماره",max_length=64,null=True,blank=True,)
    payment_account_bank = models.ForeignKey(Bank,verbose_name="بانک",on_delete=models.CASCADE,related_name="fund_account_bank",null=True,blank=True)
    # payment_SHABA = models.CharField(verbose_name="شماره شبا",max_length=64,null=True,blank=True,default='IR')
    # payment_SHABA_person = models.CharField(verbose_name="نام صاحب شبا",max_length=64,null=True,blank=True)
    # payment_SHABA_bank = models.ForeignKey(Bank, verbose_name="بانک شبا", null=True, blank=True,on_delete=models.CASCADE,related_name="shaba_bank")

    # payment_factor = models.ImageField(upload_to='AmadoWH/static/ChashFactors',null=True,blank=True,verbose_name="عکس فاکتور")
    # payment_factors = models.ManyToManyField(Image,null=True,blank=True,verbose_name="تصویر فاکتور",related_name="factors")

    payment_add_user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ثبت کننده",related_name="fund_register_user",null=True,blank=True)
    payment_add_date = jmodels.jDateTimeField(null=False,blank=False,verbose_name="تاریخ ثبت",
                                              default=jdatetime.datetime.now)
#                                               default="1397-03-28 20:38:00")

    payment_confirm_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",related_name="fund_confirm_user",null=True,blank=True)
    payment_confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                                  default=jdatetime.datetime.now,
#                                                   default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")

    payment_pay_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="پرداخت کننده",related_name="fund_pay_user",null=True,blank=True)
    payment_pay_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                               default="1397-03-28 20:38:00",
                                                  verbose_name="تاریخ تایید")

    payment_change_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تغییر دهنده",
                                         related_name="fun_change_user", null=True, blank=True)
    payment_change_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                               default="1397-03-28 20:38:00",
                                              verbose_name="تاریخ تغییر")

    # payment_recede = models.ImageField(upload_to='AmadoWH/static/ChashRecedes',null=True,blank=True,verbose_name="عکس رسید")
    # payment_recedes = models.ManyToManyField(Image, null=True, blank=True, verbose_name="تصویر رسید",related_name="recedes")

    payment_status = models.CharField(choices=status,max_length=16,verbose_name="وضعیت پرداخت",default='registered')
    
    
    cost_center = models.ForeignKey('CostCenter', on_delete=models.CASCADE, verbose_name="مرکز هزینه")
    over_account = models.ForeignKey('ActualCost.OverAccount',related_name='overcfund',on_delete=models.CASCADE,verbose_name="حساب کل")
#    def_account = models.ForeignKey('AmadoWHApp.Branch',related_name='defafund', on_delete=models.CASCADE, verbose_name="حساب معین")


    def __str__(self):
        return "%i: بابت %s تاریخ %s در وجه %s" % (
        self.pk, self.payment_cause, self.payment_due_date, self.payment_recipient,)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'تنخواه / صبحانه'
        verbose_name_plural = 'تنخواه ها / صبحانه ها'
        permissions = (
            ("can_see_fund", "می تواند مشاهده کند"),
            ("can_confirm_fund", "می تواند تایید کند"),
            ("can_decline_fund", "می تواند رد کند"),
            ("can_pay_fund", "می تواند پرداخت کند"),
            ("can_close_fund", "می تواند تسویه کند"),
            ("can_change_status_fund", "می تواند وضعیت را تغییر دهد"),
        )


class RelationShip(models.Model):
    cash = models.ForeignKey(CashPayment,verbose_name='پرداخت نقدی',null=True,blank=True,on_delete=models.CASCADE)
    checkp = models.ForeignKey(CheckPayment,verbose_name='چک/نقد',null=True,blank=True,on_delete=models.CASCADE)
    fund = models.ForeignKey(FundPayment,verbose_name='تنخواه',null=True,blank=True,on_delete=models.CASCADE)
    purchase = models.ForeignKey('AmadoWHApp.ShopRequest',verbose_name='خرید',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return "ارجاع شماره %i" % (self.pk)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'ارجاع'
        verbose_name_plural = "ارجاعات"
        permissions = (
            ("can_see_relation", "می تواند مشاهده کند"),
        )


class BankAccount(models.Model):
    card = models.CharField(verbose_name="کارت", max_length=64)
    account = models.CharField(verbose_name="شماره حساب", max_length=64)
    shaba = models.CharField(verbose_name="شبا", max_length=64)
    person = models.CharField(verbose_name="نام صاحب حساب", max_length=64, null=True, blank=True)
    bank = models.ForeignKey(Bank, verbose_name="بانک", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        # return "%s شماره کارت %s شماره حساب %s شماره شبا %s بانک %s" % (self.person,self.card,self.account,self.shaba,self.bank)
        return "%s بانک %s" % (self.person,self.bank)

    class Meta:
        verbose_name = 'حساب بانکی'
        verbose_name_plural = "حساب های بانکی"
        permissions = (
            ("can_see_image", "می تواند مشاهده کند"),
        )
        
class CostCenter(models.Model):
    title = models.CharField(max_length=64,verbose_name='عنوان')
#    branch = models.ForeignKey('AmadoWHApp.Branch',null=True,blank=True,on_delete=models.SET_NULL,verbose_name='شعبه')

    def __str__(self):
        return "مرکز %s" % (self.title)

    class Meta:
        # app_label = 'پرداختی'
        verbose_name = 'مرکز هزینه'
        verbose_name_plural = "مراکز هزینه"