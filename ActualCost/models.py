from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
import jdatetime
import time
#
#
from AmadoWHApp.models import *
from AmadoFinance.models import *
from AmadoAccounting.models import *

class WasteProduct(models.Model):
    name = models.CharField(verbose_name='نام',max_length=64)

    def __str__(self):
        return 'ضایعات %s'%self.name

    class Meta:
        verbose_name = "کالای ضایعات"
        verbose_name_plural = "کالاهای ضایعات"

class WasteSale(models.Model):

    status_char = (
        ('registered','ثبت شده'),
        ('confirmed','تایید شده'),
        ('rejected','رد شده'),
        ('paid','پرداخت شده'),
    )

    sale_date = jmodels.jDateField(verbose_name='تاریخ فروش',default=jdatetime.date.today().strftime('%Y-%m-%d'))
    buyer = models.ForeignKey('AmadoWHApp.Supplier',on_delete=models.CASCADE,verbose_name='خریدار')

    payment_date = jmodels.jDateField(verbose_name='تاریخ واریز',default=jdatetime.date.today().strftime('%Y-%m-%d'))
    account = models.ForeignKey('AmadoFinance.BankAccount',on_delete=models.CASCADE,verbose_name='حساب واریزی')

    status = models.CharField(choices=status_char,verbose_name='وضعیت',max_length=16,default='registered')

    submit_user = models.ForeignKey(User, verbose_name="کاربر ثبت کننده", on_delete=models.SET_NULL, null=True,
                                    blank=True,related_name='wau' )

    submit_date = jmodels.jDateTimeField(null=False, blank=False,
#                                          default=jdatetime.datetime.now(),
                                          default="1397-03-28 20:38:00",
                                         verbose_name="تاریخ ثبت")

    confirm_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",
                                     null=True, blank=True,related_name='wcu')
    confirm_date = jmodels.jDateTimeField(null=False, blank=False,
#                                          default=jdatetime.datetime.now(),
                                           default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")

    def __str__(self):
        return 'فروش ضایعات %s'%self.sale_date.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = "فروش ضایعات"
        verbose_name_plural = "فروش های ضایعات"

class WasteSaleProduct(models.Model):
    product = models.ForeignKey(WasteProduct,on_delete=models.CASCADE,verbose_name='کالا')
    amount = models.FloatField(verbose_name='مقدار')
    unit = models.ForeignKey('AmadoWHApp.Unit',on_delete=models.CASCADE,verbose_name='واحد')
    center = models.ForeignKey('AmadoFinance.CostCenter',on_delete=models.CASCADE,verbose_name='مبدا')
    sale = models.ForeignKey(WasteSale,on_delete=models.CASCADE,verbose_name='فروش')
    fee = models.FloatField(verbose_name='فی(ریال)')
    
    # def __str__(self):
    #     return self.product.__str__()

    class Meta:
        verbose_name = "جزئیات ضایعات"
        verbose_name_plural = "جزئیات ضایعات ها"

class Cost(models.Model):
    cost_amount = models.IntegerField(verbose_name="مبلغ", );
    cost_date = jmodels.jDateField(null=False, blank=False, default=jdatetime.datetime.today().strftime("%Y-%m-%d"),
                                   verbose_name="تاریخ ثبت قیمت")
    cost_description = models.CharField(max_length=128, null=True, blank=True, verbose_name="توضیح قیمت");

    def __unicode__(self):
        return self.cost_description

    def __str__(self):
        try:
            return '%s %i تومان' % (self.cost_description, int(self.cost_amount))
        except:
            return self.cost_amount

    class Meta:
        verbose_name = "قیمت"
        verbose_name_plural = "قیمت ها"

class Parameter(models.Model):
    parameter_name = models.CharField(max_length=64, null=False, verbose_name="نام پارامتر", unique=True);
    parameter_description = models.CharField(max_length=128, null=True, blank=True, verbose_name="توضیح پارامتر");
    parameter_is_active = models.BooleanField(verbose_name="پارامتر فعال است", default=True)

    # parameter_category = models.ForeignKey(ParameterCategory,null=False,blank=False,verbose_name='دسته پارامتر',on_delete=models.CASCADE)

    def __unicode__(self):
        return self.parameter_name

    def __str__(self):
        return '%s' % (self.parameter_name)
        #

    class Meta:
        verbose_name = "پارامتر"
        verbose_name_plural = "پارامتر ها"
        
        
class Property(models.Model):
    name = models.CharField(verbose_name='نام',max_length=64)
    branch = models.ForeignKey('AmadoWHApp.Branch',on_delete=models.SET_NULL,null=True,blank=True,verbose_name='شعبه مربوطه')
    rent = models.ManyToManyField(Cost, verbose_name="اجاره بها ماهانه")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ملک"
        verbose_name_plural = "املاک"   
        
class OverAccount(models.Model):
    name = models.CharField(verbose_name='نام', max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "حساب کل"
        verbose_name_plural = "حساب های کل"
#
class DefinitiveAccount(models.Model):
    name = models.CharField(verbose_name='نام', max_length=64)
#    parent = models.ForeignKey(OverAccount,verbose_name='حساب کل',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "حساب معین"
        verbose_name_plural = "حساب های معین"
        verbose_name_plural = "حساب های معین"
        
class ActualCost(models.Model):
    product = models.ForeignKey(Product,verbose_name='کالا',null=True,blank=True,on_delete=models.CASCADE)
    food = models.ForeignKey(AmadoFood,verbose_name='غذا',null=True,blank=True,on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,verbose_name='واحد فی',on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='فی(ریال)',default=0)
    date = jmodels.jDateField(verbose_name='تاریخ ثبت قیمت',default=jdatetime.datetime.now().strftime('%Y-%m-%d'))
    from_date = jmodels.jDateField(verbose_name='محاسبه از تاریخ',default=jdatetime.datetime.now().strftime('%Y-%m-%d'))
    to_date = jmodels.jDateField(verbose_name='محاسبه تا تاریخ',default=jdatetime.datetime.now().strftime('%Y-%m-%d'))


    def __str__(self):
        if self.product:
            return self.product.product_name
        elif self.food:
            return self.food.name
        else:
            return ''


    class Meta:
        verbose_name = "قیمت تمام شده"
        verbose_name_plural = "قیمت تمام شده ها"       
        
class DetailActualCost(models.Model):
    actual_cost = models.ForeignKey(ActualCost,verbose_name='قیمت تمام شده',null=True,blank=True,on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter,verbose_name='قیمت تمام شده',null=True,blank=True,on_delete=models.CASCADE)
    effect = models.IntegerField(verbose_name='فی(ریال)',default=0)
    title = models.CharField(verbose_name='عنوان',max_length=32,default='',blank=True,null=True)
    is_active = models.BooleanField(verbose_name='فعال است',default = True)
    
    def __str__(self):
        return 'اثر %s روی %s'%(self.parameter.parameter_name,self.actual_cost.__str__())


    class Meta:
        verbose_name = "جزئیات قیمت تمام شده"
        verbose_name_plural = "جزئیات قیمت تمام شده ها"