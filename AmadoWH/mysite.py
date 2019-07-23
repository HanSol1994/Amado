# from weakref import WeakSet
# from django.contrib.admin import AdminSite
# from django.contrib.admin import ModelAdmin, actions
# from django.template.response import TemplateResponse


# from AmadoWHApp.models import *

# all_sites = WeakSet()
# class MyAdminSite(AdminSite):
#     def __init__(self, name='admin'):
#         self._registry = {}  # model_class class -> admin_class instance
#         self.name = name
#         self._actions = {'delete_selected': actions.delete_selected}
#         self._global_actions = self._actions.copy()
#         all_sites.add(self)

#     def index(self, request, extra_context=None):

#         products = Product.objects.filter(report_index__gt=-1).order_by('report_index')
#         json = []

#         for p in products:
#             sd = ShopDetail.objects.filter(product=p).order_by('shop__from_date')

#             try:
#                 lastshop = sd.last().last_price
#                 lastshopdate = sd.last().shop.from_date.strftime("%Y/%m/%d")
#             except:
#                 lastshop = '-'
#                 lastshopdate = '-'


#             try:
#                 secondlastshop = sd[sd.count() - 2].last_price
#                 secondlastshopdate = sd[sd.count()-2].shop.from_date.strftime("%Y/%m/%d")
#             except:
#                 secondlastshop = '-'
#                 secondlastshopdate = '-'



#             sale_prices = Price.objects.filter(product=p).order_by('date')
#             try:
#                 lastprice = sale_prices.last().cost
#             except:
#                 lastprice = '-'

#             try:
#                 secondlastprice = sale_prices[sale_prices.count() - 2].cost
#             except:
#                 secondlastprice = '-'



#             data = {'product': p.product_name,'last':{'price':lastshop,'date':lastshopdate,'sale':lastprice},
#                     'secondlast':{'price': secondlastshop, 'date':secondlastshopdate , 'sale': secondlastprice}}

#             json.append(data)



#         app_list = self.get_app_list(request)

#         context = dict(
#             self.each_context(request),
#             title=self.index_title,
#             app_list=app_list,
#             shops= json,
#             report_auth=request.user.has_perm('auth.can_see_report')
#         )

#         # print(json)
#         context.update(extra_context or {})

#         request.current_app = self.name

#         return TemplateResponse(request, self.index_template or 'admin/myindex.html', context)



# site = MyAdminSite(name='myadmin')



from django.contrib.admin import AdminSite

from functools import update_wrapper
from weakref import WeakSet

from django.apps import apps
from django.contrib.admin import ModelAdmin, actions
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, reverse
from django.utils.text import capfirst
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.i18n import JavaScriptCatalog

from AmadoWHApp.models import *
from AmadoFinance.models import *
from AmadoAccounting.models import *

from django.db.models import Q, Sum, Count

all_sites = WeakSet()
class MyAdminSite(AdminSite):
    """
        An AdminSite object encapsulates an instance of the Django admin application, ready
        to be hooked in to your URLconf. Models are registered with the AdminSite using the
        register() method, and the get_urls() method can then be used to access Django view
        functions that present a full admin interface for the collection of registered
        models.
        """

    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy('Django site admin')

    # Text to put in each page's <h1>.
    site_header = gettext_lazy('Django administration')

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('Site administration')

    # URL for the "View site" link at the top of each admin page.
    site_url = '/'

    _empty_value_display = '-'

    login_form = None
    index_template = None
    app_index_template = None
    login_template = None
    logout_template = None
    password_change_template = None
    password_change_done_template = None

    def __init__(self, name='admin'):
        self._registry = {}  # model_class class -> admin_class instance
        self.name = name
        self._actions = {'delete_selected': actions.delete_selected}
        self._global_actions = self._actions.copy()
        all_sites.add(self)

    def check(self, app_configs):
        """
        Run the system checks on all ModelAdmins, except if they aren't
        customized at all.
        """
        if app_configs is None:
            app_configs = apps.get_app_configs()
        app_configs = set(app_configs)  # Speed up lookups below

        errors = []
        modeladmins = (o for o in self._registry.values() if o.__class__ is not ModelAdmin)
        for modeladmin in modeladmins:
            if modeladmin.model._meta.app_config in app_configs:
                errors.extend(modeladmin.check())
        return errors

    def register(self, model_or_iterable, admin_class=None, **options):
        """
        Register the given model(s) with the given admin class.

        The model(s) should be Model classes, not instances.

        If an admin class isn't given, use ModelAdmin (the default admin
        options). If keyword arguments are given -- e.g., list_display --
        apply them as options to the admin class.

        If a model is already registered, raise AlreadyRegistered.

        If a model is abstract, raise ImproperlyConfigured.
        """
        if not admin_class:
            admin_class = ModelAdmin

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    'The model %s is abstract, so it cannot be registered with admin.' % model.__name__
                )

            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)

            # Ignore the registration if the model has been
            # swapped out.
            if not model._meta.swapped:
                # If we got **options then dynamically construct a subclass of
                # admin_class with those **options.
                if options:
                    # For reasons I don't quite understand, without a __module__
                    # the created class appears to "live" in the wrong place,
                    # which causes issues later on.
                    options['__module__'] = __name__
                    admin_class = type("%sAdmin" % model.__name__, (admin_class,), options)

                # Instantiate the admin class to save in the registry
                self._registry[model] = admin_class(model, self)

    def unregister(self, model_or_iterable):
        """
        Unregister the given model(s).

        If a model isn't already registered, raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model]

    def is_registered(self, model):
        """
        Check if a model class is registered with this `AdminSite`.
        """
        return model in self._registry

    def add_action(self, action, name=None):
        """
        Register an action to be available globally.
        """
        name = name or action.__name__
        self._actions[name] = action
        self._global_actions[name] = action

    def disable_action(self, name):
        """
        Disable a globally-registered action. Raise KeyError for invalid names.
        """
        del self._actions[name]

    def get_action(self, name):
        """
        Explicitly get a registered global action whether it's enabled or
        not. Raise KeyError for invalid names.
        """
        return self._global_actions[name]

    @property
    def actions(self):
        """
        Get all the enabled actions as an iterable of (name, func).
        """
        return self._actions.items()

    @property
    def empty_value_display(self):
        return self._empty_value_display

    @empty_value_display.setter
    def empty_value_display(self, empty_value_display):
        self._empty_value_display = empty_value_display

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

    def admin_view(self, view, cacheable=False):
        """
        Decorator to create an admin view attached to this ``AdminSite``. This
        wraps the view and provides permission checking by calling
        ``self.has_permission``.

        You'll want to use this from within ``AdminSite.get_urls()``:

            class MyAdminSite(AdminSite):

                def get_urls(self):
                    from django.urls import path

                    urls = super().get_urls()
                    urls += [
                        path('my_view/', self.admin_view(some_view))
                    ]
                    return urls

        By default, admin_views are marked non-cacheable using the
        ``never_cache`` decorator. If the view can be safely cached, set
        cacheable=True.
        """

        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                if request.path == reverse('admin:logout', current_app=self.name):
                    index_path = reverse('admin:index', current_app=self.name)
                    return HttpResponseRedirect(index_path)
                # Inner import to prevent django.contrib.admin (app) from
                # importing django.contrib.auth.models.User (unrelated model).
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(
                    request.get_full_path(),
                    reverse('admin:login', current_app=self.name)
                )
            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    def get_urls(self):
        from django.urls import include, path, re_path
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        from django.contrib.contenttypes import views as contenttype_views

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = [
            path('', wrap(self.index), name='index'),
            path('login/', self.login, name='login'),
            path('logout/', wrap(self.logout), name='logout'),
            path('password_change/', wrap(self.password_change, cacheable=True), name='password_change'),
            path(
                'password_change/done/',
                wrap(self.password_change_done, cacheable=True),
                name='password_change_done',
            ),
            path('jsi18n/', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
            path(
                'r/<int:content_type_id>/<path:object_id>/',
                wrap(contenttype_views.shortcut),
                name='view_on_site',
            ),
        ]

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []
        for model, model_admin in self._registry.items():
            urlpatterns += [
                path('%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
            urlpatterns += [
                re_path(regex, wrap(self.app_index), name='app_list'),
            ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'admin', self.name

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        return {
            'site_title': self.site_title,
            'site_header': self.site_header,
            'site_url': site_url,
            'has_permission': self.has_permission(request),
            'available_apps': self.get_app_list(request),
        }

    def password_change(self, request, extra_context=None):
        """
        Handle the "change password" task -- both form display and validation.
        """
        from django.contrib.admin.forms import AdminPasswordChangeForm
        from django.contrib.auth.views import PasswordChangeView
        url = reverse('admin:password_change_done', current_app=self.name)
        defaults = {
            'form_class': AdminPasswordChangeForm,
            'success_url': url,
            'extra_context': dict(self.each_context(request), **(extra_context or {})),
        }
        if self.password_change_template is not None:
            defaults['template_name'] = self.password_change_template
        request.current_app = self.name
        return PasswordChangeView.as_view(**defaults)(request)

    def password_change_done(self, request, extra_context=None):
        """
        Display the "success" page after a password change.
        """
        from django.contrib.auth.views import PasswordChangeDoneView
        defaults = {
            'extra_context': dict(self.each_context(request), **(extra_context or {})),
        }
        if self.password_change_done_template is not None:
            defaults['template_name'] = self.password_change_done_template
        request.current_app = self.name
        return PasswordChangeDoneView.as_view(**defaults)(request)

    def i18n_javascript(self, request, extra_context=None):
        """
        Display the i18n JavaScript that the Django admin requires.

        `extra_context` is unused but present for consistency with the other
        admin views.
        """
        return JavaScriptCatalog.as_view(packages=['django.contrib.admin'])(request)

    @never_cache
    def logout(self, request, extra_context=None):
        """
        Log out the user for the given HttpRequest.

        This should *not* assume the user is already logged in.
        """
        from django.contrib.auth.views import LogoutView
        defaults = {
            'extra_context': dict(
                self.each_context(request),
                # Since the user isn't logged out at this point, the value of
                # has_permission must be overridden.
                has_permission=False,
                **(extra_context or {})
            ),
        }
        if self.logout_template is not None:
            defaults['template_name'] = self.logout_template
        request.current_app = self.name
        return LogoutView.as_view(**defaults)(request)

    @never_cache
    def login(self, request, extra_context=None):
        """
        Display the login form for the given HttpRequest.
        """
        if request.method == 'GET' and self.has_permission(request):
            # Already logged-in, redirect to admin index
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)

        from django.contrib.auth.views import LoginView
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.admin.forms eventually imports User.
        from django.contrib.admin.forms import AdminAuthenticationForm
        context = dict(
            self.each_context(request),
            title=_('Log in'),
            app_path=request.get_full_path(),
            username=request.user.get_username(),
        )
        if (REDIRECT_FIELD_NAME not in request.GET and
                    REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse('admin:index', current_app=self.name)
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        request.current_app = self.name
        return LoginView.as_view(**defaults)(request)

    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': perms,
            }
            if perms.get('change'):
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                }

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            for m in app['models']:
                on = m['object_name']
                count = ''
                import AmadoFinance
                user = request.user
                # if not request.user.is_superuser:
                if on == 'CashPayment':
                    if user.has_perm('auth.can_see_pay_count') or user.is_superuser:
                        count = '(%i در انتظار پرداخت)'%AmadoFinance.models.CashPayment.objects.filter(payment_status='confirmed').count()
                    elif user.has_perm('auth.can_see_confirm_count'):
                        count = '(%i در انتظار تایید)' % AmadoFinance.models.CashPayment.objects.filter(payment_status='registered').count()
                elif on == 'CheckPayment':
                    if user.has_perm('auth.can_see_pay_count') or user.is_superuser:
                        count = '(%i در انتظار پرداخت)'%AmadoFinance.models.CheckPayment.objects.filter(payment_status='confirmed').count()
                    elif user.has_perm('auth.can_see_confirm_count'):
                        count = '(%i در انتظار تایید)' % AmadoFinance.models.CheckPayment.objects.filter(payment_status='registered').count()
                elif on == 'FundPayment':
                    if user.has_perm('auth.can_see_pay_count') or user.is_superuser:
                        count = '(%i در انتظار پرداخت)'%AmadoFinance.models.FundPayment.objects.filter(payment_status='confirmed').count()
                    elif user.has_perm('auth.can_see_confirm_count'):
                        count = '(%i در انتظار تایید)' % AmadoFinance.models.FundPayment.objects.filter(payment_status='registered').count()


                m['name'] = m['name']+' '+count
            app['models'].sort(key=lambda x: x['name'])

        return app_list

    @never_cache
    def index(self, request, extra_context=None):

        # products = RawProduct.objects.filter(report_index__gt=-1).order_by('report_index')
        products = RawProduct.objects.filter(Q(report_index__gt=-1)&Q(product_is_active=True)).order_by('report_index')
        json = []

        for p in products:
            sd = ShopDetail.objects.filter(product=p).order_by('-shop__from_date','-last_price')

            try:
                sd0 = sd[0]
                lastshop = sd[0].last_price
                lastshopdate = sd[0].shop.from_date.strftime("%Y/%m/%d")
            except:
                sd0 = None
                lastshop = '-'
                lastshopdate = '-'

            try:
                sd1 = sd[1]
                secondlastshop = sd[1].last_price
                secondlastshopdate = sd[1].shop.from_date.strftime("%Y/%m/%d")
            except:
                sd1 = None
                secondlastshop = '-'
                secondlastshopdate = '-'

            # sale_prices = Price.objects.filter(product=p).order_by('-date')
            
            sale_prices = p.product_sale_prices.all()
            try:
                lastprice = sale_prices[0].cost_amount
            except:
                lastprice = '-'

            try:
                secondlastprice = sale_prices[1].cost_amount
            except:
                secondlastprice = '-'
                
            date0 = lastshopdate
            if sd0 and sd0.definitive_product:
                date0 = '%s ( %s )'%(lastshopdate,sd0.definitive_product.name)
                
            date1 = secondlastshopdate
            if sd1 and sd1.definitive_product:
                date1 = '%s ( %s )'%(secondlastshopdate,sd1.definitive_product.name)

            data = {'product': p.product_name, 'last': {'price': lastshop, 'date': date0, 'sale': lastprice},
                    'secondlast': {'price': secondlastshop, 'date': date1, 'sale': secondlastprice}}

            json.append(data)

        app_list = self.get_app_list(request)
        
        ##################Monitoring
        start_date = jdatetime.datetime.strptime('1398-03-23','%Y-%m-%d')
        today = jdatetime.datetime.today()+jdatetime.timedelta(days=-1)
        monitoring_json = []


#        branch_ids = [4,5,7]
        branch_ids = [4]

        max_count = 0
        counter = 0
        
        branches = Branch.objects.filter(id__in=branch_ids)
        bname= ''
        
        self_report_auth=False
        if request.user.has_perm('auth.can_see_self_report') and not request.user.is_superuser:
            try:
                bname = Branch.objects.get(~Q(id=3)&Q(branch_manager__manager_user=request.user)).branch_name
                
                branches = [Branch.objects.get(~Q(id=3)&Q(branch_manager__manager_user=request.user))]
                self_report_auth=True
            except:
                pass
            

        for b in branches:
            counter_date = today

            
            counter = 0
            for i in range(0,(today-start_date).days):
                
                if b.id == 7 and (counter_date.strftime('%Y-%m-%d') == '1397-06-28' or counter_date.strftime('%Y-%m-%d') == '1397-06-29' or counter_date.strftime('%Y-%m-%d') == '1397-06-27'):
                    counter_date = counter_date+jdatetime.timedelta(days=-1)
                else:
                
                    # request
                    if Request.objects.filter(Q(request_branch=b)&Q(request_date=counter_date)).count() == 0:
                    # if Request.objects.filter(Q(request_branch=b) & ((Q(request_date=counter_date)&Q(request_time__lt='01:00:00'))|(Q(request_date=counter_date+jdatetime.timedelta(days=-1))&Q(request_time__gt='19:00:00')))).count() == 0:
                        monitoring_json.append({'branch_id': b.id, 'text': 'درخواست %s' % counter_date.strftime('%Y/%m/%d')})
                        counter += 1
                    # work
                    if Work.objects.filter(Q(branch=b)&Q(date=counter_date)).count() == 0:
                        monitoring_json.append({'branch_id': b.id, 'text': 'کارکرد %s' % counter_date.strftime('%Y/%m/%d')})
                        counter += 1
    
                    if BranchWarehouse.objects.filter(Q(branch=b)&Q(date=counter_date)).count() == 0 and (today-counter_date).days<7:
                        monitoring_json.append({'branch_id': b.id, 'text': 'موجودی انبار %s' % counter_date.strftime('%Y/%m/%d')})
                        counter += 1
    
                    if Sales.objects.filter(Q(sales_branch=b)&Q(sales_date=counter_date)).count() == 0:
                        monitoring_json.append({'branch_id': b.id, 'text': 'فروش مبلغی %s' % counter_date.strftime('%Y/%m/%d')})
                        counter += 1
    
                    if FoodSale.objects.filter(Q(branch=b)&Q(date=counter_date)).count() == 0:
                        monitoring_json.append({'branch_id': b.id, 'text': 'فروش مقداری %s' % counter_date.strftime('%Y/%m/%d')})
                        counter += 1
    
                    counter_date = counter_date+jdatetime.timedelta(days=-1)
                
            if max_count < counter:
                max_count = counter
                
        v1 = []
        v2 = []
        v3 = []
        
        today = jdatetime.datetime.today()+jdatetime.timedelta(days=-1)
        
        branch_ids = [3,4,5,7]
        branches = Branch.objects.filter(id__in=branch_ids)
        
        if request.user.has_perm('auth.can_see_self_report') and not request.user.is_superuser:
            try:
                bname = Branch.objects.get(Q(branch_manager__manager_user=request.user)).branch_name
                
                branches = [Branch.objects.get(Q(branch_manager__manager_user=request.user))]
                self_report_auth=True
            except:
                pass
        
        for rv in RequestProductVariance.objects.filter(Q(request_product__request_request__request_date=today)&Q(request_product__request_request__request_branch__in=branches)).order_by('request_product__request_product'):
            
             if rv.request_product.request_unit:
                wunit = rv.request_product.request_unit
             else:
                wunit = rv.request_product.request_product.product_unit

             if rv.request_unit:
                    recunit = rv.request_unit
             elif rv.request_product.request_unit:
                    recunit = rv.request_product.request_unit
             else:
                    recunit = rv.request_product.request_product.product_unit
             v1.append({'product':rv.request_product.request_product.product_name,'unit':wunit.unit_name,'recunit':recunit.unit_name,'want':rv.request_product.request_amount,'get':rv.request_amount_received,'branch':rv.request_product.request_request.request_branch.id})

        for rv in RequestProductVariance.objects.filter(Q(request_product__request_request__request_date=today+jdatetime.timedelta(days=-1))&Q(request_product__request_request__request_branch__in=branches)).order_by('request_product__request_product'):
             if rv.request_product.request_unit:
                wunit = rv.request_product.request_unit
             else:
                wunit = rv.request_product.request_product.product_unit

             if rv.request_unit:
                    recunit = rv.request_unit
             elif rv.request_product.request_unit:
                    recunit = rv.request_product.request_unit
             else:
                    recunit = rv.request_product.request_product.product_unit
                
             v2.append({'product':rv.request_product.request_product.product_name,'unit':wunit.unit_name,'recunit':recunit.unit_name,'want':rv.request_product.request_amount,'get':rv.request_amount_received,'branch':rv.request_product.request_request.request_branch.id})

        for rv in RequestProductVariance.objects.filter(Q(request_product__request_request__request_date=today+jdatetime.timedelta(days=-2))&Q(request_product__request_request__request_branch__in=branches)).order_by('request_product__request_product'):
            
             if rv.request_product.request_unit:
                wunit = rv.request_product.request_unit
             else:
                wunit = rv.request_product.request_product.product_unit

             if rv.request_unit:
                    recunit = rv.request_unit
             elif rv.request_product.request_unit:
                    recunit = rv.request_product.request_unit
             else:
                    recunit = rv.request_product.request_product.product_unit
             v3.append({'product':rv.request_product.request_product.product_name,'unit':wunit.unit_name,'recunit':recunit.unit_name,'want':rv.request_product.request_amount,'get':rv.request_amount_received,'branch':rv.request_product.request_request.request_branch.id})

        variances={'today':v1,'todayd':(today+jdatetime.timedelta(days=1)).strftime('%Y/%m/%d'),'yesterday':v2,'yesterdayd':today.strftime('%Y/%m/%d'),'3day':v3,'3dayd':(today+jdatetime.timedelta(days=-1)).strftime('%Y/%m/%d')}

        context = dict(
            self.each_context(request),
            title=self.index_title,
            app_list=app_list,
            shops=json,
            report_auth=request.user.has_perm('auth.can_see_report'),
            self_report_auth=self_report_auth,
            bname = bname,
            monitoring=monitoring_json,
            max_count = max_count,
            variances = variances

        )

        # print(json)
        context.update(extra_context or {})

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or 'admin/myindex.html', context)




site = MyAdminSite(name='myadmin')



