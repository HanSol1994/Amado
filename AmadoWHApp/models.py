from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
import jdatetime
import time
from django.utils.safestring import mark_safe

from smart_selects.db_fields import ChainedForeignKey, \
    ChainedManyToManyField, GroupedForeignKey


#can see means can only see and not change, can see  bedoone change nadarim bekhatere link

class Manager(models.Model):
    manager_user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="کاربر")
    manager_name = models.CharField(max_length=128, verbose_name="نام مدیر")
    manager_tel = models.CharField(max_length=128, verbose_name="تلفن مدیر")
    manager_image = models.ImageField(verbose_name='عکس مدیر شعبه',null=True,blank=True)
    # manager_branch = models.ForeignKey(Branch,null=True,blank=True, on_delete=models.SET_NULL, verbose_name="شعبه مدیر")

    class Meta:
        verbose_name = "مدیر"
        verbose_name_plural = "مدیران"
        permissions = (
            ("can_see_manager", "می تواند مشاهده کند"),
        )

    def __str__(self):
        return '%s' % (self.manager_name)

class Branch(models.Model):
    branch_name = models.CharField(max_length=128, verbose_name="نام شعبه")
    branch_manager = models.ForeignKey(Manager,null=True,blank=True, on_delete=models.SET_NULL, verbose_name="مدیر شعبه")
    branch_phone = models.CharField(max_length=128, verbose_name="تلفن شعبه")

    def __str__(self):
        return '%s' % (self.branch_name)

    class Meta:
        verbose_name = "شعبه"
        verbose_name_plural = "شعبات"
        permissions = (
            ("can_see_branch", "می تواند مشاهده کند"),
        )


class Supplier (models.Model):
    supplier_company = models.CharField(max_length=128, blank= True, null= True, verbose_name="شرکت تامین کننده");
    supplier_name = models.CharField(max_length=128 , null=False,blank=False,default="", verbose_name="نام تامین کننده");
    supplier_phone = models.CharField(max_length=128 , null=True,blank=True,default="", verbose_name="تلفن تامین کننده");
    supplier_address = models.TextField(max_length=256,null=True,blank=True,default="", verbose_name="آدرس تامین کننده")
    
    supplier_account =  models.ManyToManyField('AmadoFinance.BankAccount',verbose_name='حساب بانکی تامین کننده',)

    def __str__(self):
        if self.supplier_company:
            return "%s از %s" % (self.supplier_name, self.supplier_company);
        else:
            return self.supplier_name

    class Meta:
        verbose_name = "تامین کننده"
        verbose_name_plural = "تامین کنندگان"
        permissions = (
            ("can_see_supplier", "می تواند مشاهده کند"),
        )

class ProductCategory (models.Model):
    product_category_name = models.CharField(max_length=128, verbose_name="نام دسته");

    def __str__(self):
        return "%s" % (self.product_category_name);

    class Meta:
        verbose_name = "دسته بندی محصول"
        verbose_name_plural = "دسته بندی های محصول"

        permissions = (
            ("can_see_pcat", "می تواند مشاهده کند"),
        )

class Unit(models.Model):
    unit_name = models.CharField(max_length=64,null=False,verbose_name="نام واحد",unique=True);
    unit_description = models.CharField(max_length=128,null=True,blank=True,verbose_name="توضیح واحد");

    def __unicode__(self):
        return self.unit_name

    def __str__(self):
        return '%s' % (self.unit_name)

    class Meta:
        verbose_name = "واحد"
        verbose_name_plural = "واحد ها"
        permissions = (
            ("can_see_unit", "می تواند مشاهده کند"),
        )

class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=64, null=False, verbose_name="نام انبار", unique=True);
    warehouse_description = models.CharField(max_length=128, null=True, blank=True, verbose_name="توضیح انبار");

    def __unicode__(self):
        return 'انبار %s'%self.warehouse_name

    def __str__(self):
        return '%s' % (self.warehouse_name)

    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبار ها"
        permissions = (
            ("can_see_wh", "می تواند مشاهده کند"),
        )

class UnitToUnit(models.Model):
    first_unit = models.ForeignKey(Unit,verbose_name='واحد بزرگتر',on_delete=models.CASCADE,related_name='funit')
    second_unit = models.ForeignKey(Unit,verbose_name='واحد کوچکتر',on_delete=models.CASCADE,related_name='sunit')
    ration = models.FloatField(default=1,verbose_name='تبدیل بزرگ به کوچک')
    product = models.ForeignKey('Product',verbose_name='محصول مربوطه',on_delete=models.CASCADE,null=True,blank=True)
    raw_product = models.ForeignKey('RawProduct',verbose_name='کالای خام مربوطه',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        # return '%s' % (self.product_name)
        return '%s به %s' % (self.first_unit, self.second_unit)

    class Meta:
        verbose_name = "تبدیل واحد"
        verbose_name_plural = "تبدیلات واحد ها"
        
        
class Product (models.Model):
    
    level = (
        ('lvl1','کالای خام'),
        ('lvl2','کالای آماده سازی'),
        ('lvl1-2','کالای خام آماده سازی'),
        ('lvl3','غذای آمادو'),
    )
    
    product_name = models.CharField(max_length=128, verbose_name="نام محصول");
    product_supplier = models.ManyToManyField(Supplier, null=True, blank=True,verbose_name="تامین کننده")
    product_category = models.ForeignKey(ProductCategory,default='1', on_delete=models.CASCADE, verbose_name="دسته محصول")
    product_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="واحد محصول")
    
    product_second_unit = models.ForeignKey(Unit,related_name='second', on_delete=models.CASCADE, verbose_name="واحد دوم محصول")
    product_unit_ratio = models.FloatField(default=1,verbose_name='تبدیل واحد')

    
    product_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="انبار محصول",default=1,null=True,blank=True)
    current_price = models.IntegerField(default=0,verbose_name="قیمت خرید فعلی");
    previous_price = models.IntegerField(default=0,verbose_name="قیمت خرید قبلی");
    price_change_date = jmodels.jDateField(null=False,blank=False,default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ تغییر قیمت")
    product_description = models.TextField(max_length=256,verbose_name="توضیحات محصول",null=True,blank=True)

    product_weekly_consumption = models.FloatField(default=0,verbose_name="مصرف هفتگی")

    product_is_active = models.BooleanField(verbose_name="کالا فعال می باشد",default=True)
    
    product_level = models.CharField(choices=level,max_length=32,verbose_name="سطح",default='lvl2')
    product_payment_is_check = models.BooleanField(verbose_name='تسویه به صورت چک می باشد',default=False)
    product_payment_check_days = models.IntegerField(verbose_name='روزهای چک',default=0)
    
    
    report_index = models.IntegerField(default=-1,verbose_name='ردیف در گزارش')

    product_actual_price_1 = models.IntegerField(verbose_name='قیمت تمام شده نوع ۱(ریال)',null=True,blank=True )
    product_actual_price_2 = models.IntegerField(verbose_name='قیمت تمام شده نوع ۲(ریال)',null=True,blank=True )
    
    product_branch_warehouse = models.BooleanField(default=False,verbose_name='در موجودی انبار شعب باید وارد شود')
    # product_second_unit = models.ForeignKey(Unit,related_name='sec_unit', on_delete=models.CASCADE, verbose_name="واحد محصول")
    # unit_ratio = models.FloatField(default=1,verbose_name="واحد ۱ دارای این مقدار از واحد ۲ است")
    
    sale_percentage = models.FloatField(verbose_name='درصد برای قیمت فروش',default=15)

    
    
    def full_name(self):
        return '%s (%s)'%(self.product_name,self.product_unit)

    # def __unicode__(self):
    #     return self.product_name
    
    def func(self):
        last_price = Price.objects.filter(product=self).order_by('date')
        if last_price:
            last_price = last_price.last().cost
            return '%s ریال' % "{:,}".format(last_price)
        else:
            return ''


    def __str__(self):
        # return '%s' % (self.product_name)
        return '%s (%s)' % (self.product_name, self.product_unit)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

        permissions = (
            ("can_see_product", "می تواند مشاهده کند"),
        )

class Warehouse_Product (models.Model):
    warehouse_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    warehouse_handling_date = jmodels.jDateField(null=False, blank=False, default="1396-01-01",verbose_name="تاریخ گرفتن موجودی")
    # warehouse_product_finish_date = jmodels.jDateField(null=False,blank=False,default="1396-01-01",verbose_name="پیشبینی اتمام")
    warehouse_product_stock = models.FloatField(default=0, verbose_name="میزان موجودی در انبار")

    def __str__(self):
        return '%s' % (self.warehouse_product)

    class Meta:
        verbose_name = "محصول در انبار"
        verbose_name_plural = "محصولات در انبار"

        permissions = (
            ("can_see_whproduct", "می تواند مشاهده کند"),
        )


class RequestProduct(models.Model):
    request_product = models.ForeignKey(Product,null=False,blank=False, on_delete=models.CASCADE, verbose_name="محصول درخواستی")
    # request_warehouse = models.ForeignKey(Warehouse,null=True,blank=True, on_delete=models.CASCADE, verbose_name="انبار محصول درخواستی")
    # request_product = GroupedForeignKey(
    #     Product,
    #     group_field="product_warehouse",
    #     # chained_model_field="product_warehouse",
    #     # show_all=False,
    #     # auto_choose=True,
    #     # sort=True,
    #     verbose_name="محصول درخواستی")
    request_request = models.ForeignKey('Request', on_delete=models.CASCADE, verbose_name="درخواست")
    request_amount = models.FloatField(null=False,blank=False,default = 0, verbose_name="میزان درخواستی")
    request_unit = models.ForeignKey(Unit,verbose_name='واحد',null=True,blank=True,on_delete=models.SET_NULL)
    request_description = models.CharField(max_length=128,null=True, blank=True, verbose_name="توضیحات محصول")
    request_variance = models.ManyToManyField('RequestProductVariance',null=False,blank=False,verbose_name='مغایرت')
    request_time = models.TimeField(null=True, blank=True, default=jdatetime.datetime.now().strftime("%H:%M:%S"),
                                      verbose_name="ساعت ثبت")
    request_date = jmodels.jDateField(null=True, blank=True, default=jdatetime.datetime.now().strftime("%Y-%m-%d"),
                                      verbose_name="تاریخ ثبت")
    request_operator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name="کاربر ثبت کننده")
                                         
    request_amount_sent = models.FloatField(null=True, blank=True, verbose_name="میزان دریافتی از انبار")
    request_unit_sent = models.ForeignKey(Unit,verbose_name='واحد ارسال',null=True,blank=True,on_delete=models.SET_NULL,related_name='sent_unit')
    
    def mfield_1(self):
        if self.request_product.product_unit != self.request_product.product_second_unit:
            return mark_safe('<span>%s %i %sی</span>'%(self.request_product.product_unit,self.request_product.product_unit_ratio,self.request_product.product_second_unit))
        else:
            return mark_safe('<span>%s</span>'%(self.request_product.product_unit))
    mfield_1.short_description = 'واحد ۱ به ۲'

    # request_amount_received = models.FloatField(null=False,blank=False, verbose_name="میزان دریافتی")
    # request_variance = models.BooleanField(verbose_name="مغایرت دارد",default=False)#TODO

    # def __unicode__(self):
    #     return self.product_amount

    def __str__(self):
        return 'درخواست %s' % (self.request_product)

    class Meta:
        verbose_name = "محصول درخواستی"
        verbose_name_plural = "محصول های درخواستی"

        permissions = (
            ("can_see_requestp", "می تواند مشاهده کند"),
        )

class RequestProductVariance(models.Model):
    choices = (
        ('waiting', 'مغایرت در انتظار تایید'),
        ('confirmed', 'مغایرت تایید شده'),
        ('rejected', 'مغایرت رد شده'),
    )
    
    types = (
        ('less', 'مغایرت در ارسال'),
        ('waste', 'ضایعات از انبار'),
        ('fromother', 'دریافت از شعبه دیگر'),
        ('toother', 'ارسال به شعبه دیگر'),
    )

    request_product = models.ForeignKey(RequestProduct, on_delete=models.CASCADE, verbose_name="محصول دارای مغایرت",default=1)
    # request = models.ForeignKey('Request', default='1',on_delete=models.CASCADE, verbose_name="درخواست")
    request_amount_received = models.FloatField(null=False,blank=False, verbose_name="میزان دریافتی")
    request_unit = models.ForeignKey(Unit,verbose_name='واحد',null=True,blank=True,on_delete=models.SET_NULL)
    request_type = models.CharField(choices =types,max_length=16,verbose_name='مورد',default='less')
    
    request_time = models.TimeField(null=True, blank=True, default=jdatetime.datetime.now().strftime("%H:%M:%S"),
                                      verbose_name="ساعت ثبت مغایرت")
    request_date = jmodels.jDateField(null=True, blank=True, default=jdatetime.datetime.today().strftime("%Y-%m-%d"),
                                      verbose_name="تاریخ ثبت مغایرت")
    request_operator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name="کاربر ثبت کننده")
    request_variance_confirm = models.CharField(verbose_name="وضعیت مغایرت",choices=choices,default="0",max_length=16)

    request_description = models.CharField(max_length=256,null=True,blank=True,verbose_name="در صورتی که بجای این محصول،‌محصول دیگری دریافت کردید نام و مقدار آن را بنویسید")

    def __str__(self):
        return 'درخواست %s' % (self.request_product)

    class Meta:
        verbose_name = "مغایرت محصول درخواستی"
        verbose_name_plural = "مغایرت محصول های درخواستی"
        permissions = (
            ("can_see_requestpvar", "می تواند مشاهده کند"),
        )

class Request(models.Model):

    choices = (
        ('waiting','در انتظار تایید'),
        ('confirmed','تایید شده'),
        ('rejected','رد شده'),
        ('variated','مغایرت دارد'),
        ('closed','بسته شده است'),

    )

    # branch 00
    # date 970212
    # number 0

    request_code = models.CharField(max_length=13,default='-' , verbose_name="کد درخواست")
    request_branch = models.ForeignKey(Branch, on_delete=models.CASCADE,null=True,blank=True, verbose_name="شعبه درخواست دهنده")
    request_product = models.ManyToManyField(Product, through='RequestProduct', null=False, blank=False, verbose_name="محصول درخواستی")
    request_date = jmodels.jDateField(null=True, blank=True, default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ درخواست")

    request_time = models.TimeField(null=True, blank=True, default=jdatetime.datetime.now().strftime("%H:%M:%S"),
                                      verbose_name="ساعت درخواست")
    request_operator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name="کاربر ثبت کننده")


    request_received = models.CharField(verbose_name="وضعیت",choices=choices,default="waiting",max_length=16)
    # variance = models.ManyToManyField(RequestProduct, through='RequestProductVariance', null=False, blank=False,
    #                                          verbose_name="محصول دارای مغایرت")

    # def get_brief(self):
    #     try:
    #         ps = RequestProduct.objects.filter(request=self.id).values('request_amount','request_product__product_name')[5];
    #
    #         str = '<ul>';
    #         for p in ps:
    #             str += '<li>%i %s</li>' % (p.request_amount, prequest_product__product_name)
    #         if len(ps) > 5:
    #             str += '<li>...</li></ul>'
    #         else:
    #             str += '</ul>'
    #
    #         return str
    #     except:
    #         ps = RequestProduct.objects.filter(request=self.id).values('request_amount', 'request_product__product_name');
    #
    #
    #
    #         str = '<ul>';
    #         for p in ps:
    #             print(p.request_amount)
    #             str += '<li>%i %s</li>' % (p.request_amount, p.request_product__product_name)
    #         str += '</ul>'
    #
    #         return str
    #
    # get_brief.short_description='خلاصه سفارش'
    # get_brief.allow_tags = True

    # def get_link(self):
    #     return '<a href="../../../request/%i/change">مشاهده درخواست</a>'%self.id
    #
    # get_link.short_description = 'درخواست'
    # get_link.allow_tags = True


    def __str__(self):
        return '%s - %s' % (self.request_branch,self.request_date)

    class Meta:
        verbose_name = "درخواست"
        verbose_name_plural = "درخواست ها"

        permissions = (
            ("can_see_request", "می تواند مشاهده کند"),
            ("can_confirm_request", "می تواند تایید کند"),
            ("can_decline_request", "می تواند رد کند"),
        )

class Message(models.Model):
    choices = (
        ('warehouse', 'انبار/حسابداری'),
        ('management', 'مدیریت'),
    )

    # exclude()

    message_user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="کاربر")
    message_subject = models.CharField(max_length=256,default="", verbose_name='عنوان پیام', null=False, blank=False, )
    message_text = models.TextField(max_length=1024,verbose_name='متن پیام',null=False,blank=False,)
    message_date = models.CharField(max_length=32,null=True, blank=True, default=jdatetime.datetime.today().strftime("%Y-%m-%d ساعت %H:%M"),verbose_name="تاریخ ارسال پیام")
    message_answered = models.BooleanField(default=False,verbose_name='پاسخ داده شده')
    message_group = models.CharField(choices=choices,max_length=32,verbose_name='ارسال پیام برای')
    message_reply = models.TextField(max_length=1024,verbose_name='متن پاسخ',null=True,blank=True,)
    # message_replies = models.ManyToManyField('self', through='MessageRelationship',
    #                                        symmetrical=False,
    #                                        verbose_name='پاسخ ها')


    def __str__(self):
        return '%s (%s) : %s' % (self.message_user,self.message_date,self.message_subject)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

        permissions = (
            ("can_see_messaeg", "می تواند مشاهده کند"),
            ("can_reply_message", "می تواند پیام دهد"),
        )


class MessageRelationship(models.Model):
    from_relation = models.ForeignKey(Message, verbose_name='پیام اولیه',on_delete=models.CASCADE,related_name='from_message')
    to_relation = models.ForeignKey(Message, verbose_name='پیام پاسخ',on_delete=models.CASCADE,related_name='to_message')

    def __str__(self):
        return 'پاسخ پیام %s: %s' % (self.message_relation_from,self.message_relation_to)

    class Meta:
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ ها"

        permissions = (
            ("can_see_reply", "می تواند مشاهده کند"),
            ("can_reply_reply", "می تواند پاسخ دهد"),

        )

class ShopRequest(models.Model):

    s = (
        ('submitted','ثبت شده / در انتظار تایید'),
        ('confirmed','تایید شده'),
        ('done','خرید شده'),
        ('declined','رد شده'),
        ('received','دریافت شده'),
    )
    
    branch = models.ForeignKey(Branch,verbose_name='شعبه دریافت کننده',on_delete=models.CASCADE,default=8)

    from_date = jmodels.jDateField(default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ خرید")
    # delivery_date = jmodels.jDateField(default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ ارسال")
    description = models.TextField(max_length=512,verbose_name="توضیحات",null=True,blank=True)



    supplier = models.ForeignKey(Supplier, verbose_name='تامین کننده', on_delete=models.CASCADE)


    status = models.CharField(choices=s,verbose_name="وضعیت",max_length=32,default='submitted')

    submit_user = models.ForeignKey(User,verbose_name="کاربر ثبت کننده",on_delete=models.SET_NULL,null=True,blank=True,related_name="submitu")
    submit_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                              default="1397-03-28 20:38:00",
                                              verbose_name="تاریخ ثبت")

    confirm_user = models.ForeignKey(User,verbose_name="کاربر تایید کننده",on_delete=models.SET_NULL,null=True,blank=True,related_name="confirmu")
    confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                              default=jdatetime.datetime.now,
#                                               default="1397-03-28 20:38:00",
                                              verbose_name="تاریخ تایید")



    def __str__(self):
       
        return 'خرید تاریخ %s از %s' % (self.from_date,self.supplier)

    class Meta:
        verbose_name = "خرید و ورود به انبار"
        verbose_name_plural = "خرید ها و ورود به انبار"

        permissions = (
            ("can_see_shopreq", "می تواند مشاهده کند"),
            ("can_confirm_shopreq", "می تواند تایید کند"),

        )

class ShopDetail(models.Model):
    shop = models.ForeignKey(ShopRequest,verbose_name='خرید مربوطه',on_delete=models.CASCADE,default=1)
    # product = models.ForeignKey(Product,null=False,blank=False, on_delete=models.CASCADE, verbose_name="محصول")
    product = models.ForeignKey('RawProduct',null=True,blank=True, on_delete=models.CASCADE, verbose_name="محصول")
    
    definitive_product = models.ForeignKey('DefinitiveProduct',null=True,blank=True, on_delete=models.CASCADE, verbose_name="کالای خاص")
    
    unit = models.ForeignKey(Unit,verbose_name="واحد",on_delete=models.SET_NULL,null=True,blank=True)

    amount = models.FloatField(verbose_name='میزان خرید',default=0)

    last_price = models.IntegerField(verbose_name='فی(ریال)')
    last_price_date = jmodels.jDateField(verbose_name='تاریخ آخرین قیمت',default=jdatetime.datetime.today().strftime("%Y-%m-%d"),null=True,blank=True)

    purchase_durability = models.IntegerField(verbose_name='ماندگاری خرید(روز)',default=0)


    wh_amount = models.FloatField(verbose_name='میزان موجودی',default=0,null=True,blank=True)

    rc_amount = models.FloatField(verbose_name='میزان دریافتی',default=0,null=True,blank=True)

    rc_date = jmodels.jDateField(default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ دریافت")

    # description = models.CharField(max_length=128,verbose_name='توضیحات',null=True,blank=True)




    def __str__(self):
        return '%s' % (self.product)

    class Meta:
        verbose_name = "محصول خرید"
        verbose_name_plural = "محصول های خرید"

        permissions = (
            ("can_see_shopdet", "می تواند مشاهده کند"),
        )


class FoodSale(models.Model):

    date = jmodels.jDateField(default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ فروش")

    branch = models.ForeignKey(Branch, verbose_name="شعبه", on_delete=models.CASCADE, null=True,
                                     blank=True)

    is_closed = models.BooleanField(default=False,verbose_name='گزارش بسته شده است')

    submit_user = models.ForeignKey(User, verbose_name="کاربر ثبت کننده", on_delete=models.SET_NULL, null=True,
                                     blank=True, related_name="submituf")
    submit_date = jmodels.jDateTimeField(null=False, blank=False,
                                          default=jdatetime.datetime.now,
#                                           default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ ثبت")

    confirm_user = models.ForeignKey(User, verbose_name="کاربر تایید کننده", on_delete=models.SET_NULL, null=True,
                                     blank=True, related_name="confirmuf")
    confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                          default=jdatetime.datetime.now,
#                                           default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")



    def __str__(self):
        return "فروش غذای شعبه %s در تاریخ %s"%(self.branch,self.date)

    class Meta:
        verbose_name = 'فروش غذایی'
        verbose_name_plural = "فروش های غذایی"
        permissions = (
            ("can_see_foodsales", "می تواند مشاهده کند"),
            ("can_close_foodsales", "می تواند ببندد"),
        )


class FoodSaleProduct(models.Model):
    # product = models.ForeignKey('AmadoFood',on_delete=models.CASCADE,verbose_name='غذا')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='غذا')



    sale = models.ForeignKey(FoodSale,on_delete=models.CASCADE,verbose_name='فروش')

    amount = models.IntegerField(verbose_name='تعداد فروش',default=0)

    def __str__(self):
        return "غذای %s %s"%(self.product,self.sale)

    class Meta:
        verbose_name = 'غذای فروش'
        verbose_name_plural = "غذا های فروش"
        permissions = (
            ("can_see_productfoodsales", "می تواند مشاهده کند"),
        )

class BranchWarehouse(models.Model):

    date = jmodels.jDateField(default=jdatetime.datetime.today().strftime("%Y-%m-%d"), verbose_name="تاریخ موجودی")
    description = models.TextField(max_length=512, verbose_name="توضیحات", null=True, blank=True)

    branch = models.ForeignKey(Branch, verbose_name='شعبه', on_delete=models.CASCADE)

    submit_user = models.ForeignKey(User, verbose_name="کاربر ثبت کننده", on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name="submitubw")
    submit_date = jmodels.jDateTimeField(null=False, blank=False,
                                         default=jdatetime.datetime.now,
#                                           default="1397-03-28 20:38:00",
                                         verbose_name="تاریخ ثبت")
                                         
    status = (
        ('registered', 'ثبت شده/در انتظار تایید'),
        ('confirmed', 'تایید شده'),
        ('byadmin', 'موجودی توسط مدیریت گرفته شده'),
    )

    status = models.CharField(choices=status, max_length=16, verbose_name="وضعیت", default='registered')

    confirm_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تایید کننده",
                                     related_name="confirmbw", null=True, blank=True)
    confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                          default=jdatetime.datetime.now,
#                                           default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")

    def __str__(self):
        return '%s %s' % (self.date,self.branch)

    class Meta:
        verbose_name = 'موجودی انبار شعبه'
        verbose_name_plural = 'موجودی انبار شعب'

        permissions = (
            ("can_see_brawar", "می تواند مشاهده کند"),
        )


class BranchWarehouseProduct(models.Model):
    branch_warehouse = models.ForeignKey(BranchWarehouse,on_delete=models.CASCADE,verbose_name='رابطه موجودی')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE,verbose_name='واحد',null=True,blank=True)
    amount = models.FloatField(verbose_name='مقدار موجودی')
    description = models.CharField(max_length=128,verbose_name='توضیحات',null=True,blank=True)

    
    def getunit(self):
        return self.product.product_second_unit.unit_name
    
    getunit.short_description = 'واحد محاسبه'

    def __str__(self):
        return '%s' % (self.product)

    class Meta:
        verbose_name = "محصول موجود"
        verbose_name_plural = "محصولات موجود"

        permissions = (
            ("can_see_brawarpro", "می تواند مشاهده کند"),
        )
        
        
class FoodSale(models.Model):

    date = jmodels.jDateField(default=jdatetime.datetime.today().strftime("%Y-%m-%d"),verbose_name="تاریخ فروش")

    branch = models.ForeignKey(Branch, verbose_name="شعبه", on_delete=models.CASCADE, null=True,
                                     blank=True)

    is_closed = models.BooleanField(default=False,verbose_name='گزارش بسته شده است')

    submit_user = models.ForeignKey(User, verbose_name="کاربر ثبت کننده", on_delete=models.SET_NULL, null=True,
                                     blank=True, related_name="submituf")
    submit_date = jmodels.jDateTimeField(null=False, blank=False,
                                          default=jdatetime.datetime.now,
#                                           default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ ثبت")

    confirm_user = models.ForeignKey(User, verbose_name="کاربر تایید کننده", on_delete=models.SET_NULL, null=True,
                                     blank=True, related_name="confirmuf")
    confirm_date = jmodels.jDateTimeField(null=False, blank=False,
                                          default=jdatetime.datetime.now,
#                                           default="1397-03-28 20:38:00",
                                          verbose_name="تاریخ تایید")



    def __str__(self):
        return "فروش غذای شعبه %s در تاریخ %s"%(self.branch,self.date)

    class Meta:
        verbose_name = 'فروش غذایی'
        verbose_name_plural = "فروش های غذایی"
        permissions = (
            ("can_see_foodsales", "می تواند مشاهده کند"),
            ("can_close_foodsales", "می تواند ببندد"),
        )


class FoodSaleProduct(models.Model):
    product = models.ForeignKey('AmadoFood',on_delete=models.CASCADE,verbose_name='غذا')

    sale = models.ForeignKey(FoodSale,on_delete=models.CASCADE,verbose_name='فروش')

    amount = models.IntegerField(verbose_name='تعداد فروش')

    def __str__(self):
        return "غذای %s %s"%(self.product,self.sale)

    class Meta:
        verbose_name = 'غذای فروش'
        verbose_name_plural = "غذا های فروش"
        permissions = (
            ("can_see_productfoodsales", "می تواند مشاهده کند"),
        )


class AmadoFood(models.Model):
    name = models.CharField(max_length=128, verbose_name="نام محصول");
    current_price = models.IntegerField(default=0, verbose_name="قیمت فعلی(تومان)");
    previous_price = models.IntegerField(default=0, verbose_name="قیمت قبلی(تومان)");
    price_change_date = jmodels.jDateField(null=False, blank=False,
                                           default=jdatetime.datetime.today().strftime("%Y-%m-%d"),
                                           verbose_name="تاریخ تغییر قیمت")
    product_description = models.TextField(max_length=256, verbose_name="توضیحات محصول", null=True, blank=True)

    product_is_active = models.BooleanField(verbose_name="غذا در منو موجود می باشد", default=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "غذا"
        verbose_name_plural = "غذا ها"

        permissions = (
            ("can_see_food", "می تواند مشاهده کند"),
        )
        
        
class Price(models.Model):
    cost = models.IntegerField(verbose_name='قیمت(ریال)',)
    date = jmodels.jDateField(verbose_name='تاریخ قیمت',default=jdatetime.datetime.today().strftime('%Y-%m-%d'))

    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول مربوطه')

    def __str__(self):
        return '%s %s'%(self.product,self.date)

    class Meta:
        verbose_name = "قیمت"
        verbose_name_plural = "قیمت ها"


############################################################################################################

class RawProduct (models.Model):

    cats = (
        ('dried','خشک'),
        ('wet_p','تر فرآوری شده'),
        ('wet_np','تر فرآوری نشده'),
    )

    product_name = models.CharField(max_length=128, verbose_name="نام محصول");
    product_process = models.CharField(max_length=16,choices=cats, verbose_name="فرآوری محصول",default='dried');
    product_sale_prices = models.ManyToManyField('ActualCost.Cost', verbose_name="قیمت فروش", null=True, blank=True,related_name='sale_price')
    prodcut_divisions = models.ManyToManyField('AmadoAccounting.Division',verbose_name="بخش های مربوطه",null=True,blank=True)
    product_price_parameter = models.IntegerField(default=1,verbose_name="چندمین بزرگترین قیمت")

    product_actual_cost = models.ManyToManyField('ActualCost.Cost',verbose_name="قیمت تمام شده ها",related_name="actual_cost",null=True,blank=True)

    product_description = models.TextField(max_length=256,verbose_name="توضیحات محصول",null=True,blank=True)

    product_weekly_consumption = models.FloatField(default=0,verbose_name="مصرف هفتگی")

    product_is_active = models.BooleanField(verbose_name="کالا فعال می باشد",default=True)

    product_monthly_storage = models.FloatField(verbose_name="ماندگاری محصول(بر اساس ماه)",default=0)

    parameters = models.ManyToManyField('ActualCost.Parameter',verbose_name='پارامتر های قیمت تمام شده',null=True,blank=True)
    
    report_index = models.IntegerField(default=-1,verbose_name='ردیف در گزارش')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "کالای قابل خرید"
        verbose_name_plural = "کالاهای قابل خرید"

class DefinitiveProduct(models.Model):
    raw_product = models.ForeignKey(RawProduct,on_delete=models.CASCADE,verbose_name='کالای خام')
    name = models.CharField(max_length=64,verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "کالای معین"
        verbose_name_plural = "کالاهای معین"
        
        
class Recipe12(models.Model):
    recipe_child_product = models.ForeignKey(Product,verbose_name="محصول نهایی",related_name="child",on_delete=models.CASCADE)
    recipe_parent_product = models.ForeignKey(RawProduct,verbose_name="ماده تشکیل دهنده",related_name="parent",on_delete=models.CASCADE)
    recipe_amount = models.FloatField(verbose_name="میزان ماده تشکیل دهنده در ۱ واحد از محصول",null=False,blank=False)
    recipe_unit = models.ForeignKey(Unit,default=1,null=False,blank=False, on_delete=models.CASCADE, verbose_name="واحد مقدار")

    def __unicode__(self):
        return self.recipe_child_product

    class Meta:
        verbose_name = "دستور تهیه آماده سازی"
        verbose_name_plural = "دستور های تهیه آماده سازی"
        
class Recipe23(models.Model):
    recipe_child_product = models.ForeignKey(AmadoFood,verbose_name="غذا",related_name="child",on_delete=models.CASCADE)
    recipe_parent_product = models.ForeignKey(Product,verbose_name="ماده تشکیل دهنده",related_name="parent",on_delete=models.CASCADE)
    recipe_amount = models.FloatField(verbose_name="میزان ماده تشکیل دهنده در ۱ واحد از محصول",null=False,blank=False)
    recipe_unit = models.ForeignKey(Unit,default=1,null=False,blank=False, on_delete=models.CASCADE, verbose_name="واحد مقدار")

#    def __unicode__(self):
#        return self.recipe_child_product

    class Meta:
        verbose_name = "دستور تهیه غذا"
        verbose_name_plural = "دستور های تهیه غذا"