from AmadoAccounting.models import *
from django.db.models import IntegerField
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum,Q,Count,F
from django.template import loader
import jdatetime
import requests
from django.shortcuts import redirect
import random
import string
from django.views.decorators.csrf import csrf_exempt
import xlrd

from AmadoFinance.models import Bank
from AmadoWHApp.models import Branch


@csrf_exempt
def upload_salary(request):

    def my_int(num):
        if num != '':
            return int(num)
        else:
            return None

    if not request.user.is_authenticated:
        return JsonResponse({'res':'no'})

    if request.method == 'POST' and request.FILES['salary']:

        date = jdatetime.datetime.strptime(request.POST['date'],'%Y-%m-%d')
        branch = int(request.POST['branch'])

        if branch != 11:
            salary, exists = Salary.objects.get_or_create(month=date, branch=Branch.objects.get(id=branch))
        else:
            salary, exists = Salary.objects.get_or_create(month=date, branch=None)

        input_excel = request.FILES['salary']
        book = xlrd.open_workbook(file_contents=input_excel.read())

        salary_sheet = book.sheet_by_index(0)




        for row_idx in range(2, salary_sheet.nrows-2):

            name = salary_sheet.cell_value(row_idx, 1)
            person = Person.objects.get(name=name)

            try:
                detail, dexists = SalaryDetail.objects.get_or_create(salary=salary,person=person)
            except:
                detail = SalaryDetail(salary=salary,person=person)

            detail.add_date=jdatetime.datetime.now()
            detail.payment_status='registered'
            detail.add_user=request.user

            desc = ''
            notes = salary_sheet.cell_note_map
            for key in notes.keys():
                if key[0] == row_idx:
                    desc = '%s \n %s'%(desc,notes[key].text)

            cols = ['radif','name','title', 'days', 'fix', 'base', 'agreement', 'maskan', 'childs', 'childs_money', 'bon', 'sanavat',
                    'hoghoogh_vezarat_kar_tot', 'positive_taraz', 'mazaya', 'extra_shift', 'extra_shift_fee',
                    'del_sal', 'del_sal_fee', 'off', 'off_fee', 'extra_hours', 'extra_hours_fee',
                    'eydi', 'vacation_rem', 'vacation_rem_fee',
                    'reward', 'snapp', 'hoghoogh_mazaya_plus', 'help', 'negative_taraz', 'other_deduction', 'fine', 'bime',
                    'maliat', 'kosoorat_sum', 'pardakhti', 'karfarma_bime', 'account', 'card', 'bank', ]




            title = salary_sheet.cell_value(row_idx, cols.index('title'))
            days = salary_sheet.cell_value(row_idx, cols.index('days'))
            detail.days = my_int(days)
            fix = salary_sheet.cell_value(row_idx, cols.index('fix'))
            detail.fix = my_int(fix)
            base = salary_sheet.cell_value(row_idx, cols.index('base'))
            detail.base = my_int(base)
            agreement = salary_sheet.cell_value(row_idx,  cols.index('agreement'))
            detail.agreement = my_int(agreement)
            maskan = salary_sheet.cell_value(row_idx, cols.index('maskan'))
            detail.maskan = my_int(maskan)
            childs = salary_sheet.cell_value(row_idx, cols.index('childs'))
            detail.childs = my_int(childs)
            childs_money = salary_sheet.cell_value(row_idx, cols.index('childs_money'))
            detail.childs_money = my_int(childs_money)
            bon = salary_sheet.cell_value(row_idx, cols.index('bon'))
            detail.bon = my_int(bon)
            sanavat = salary_sheet.cell_value(row_idx, cols.index('sanavat'))
            detail.sanavat = my_int(sanavat)
            hoghoogh_vezarat_kar_tot = salary_sheet.cell_value(row_idx, cols.index('hoghoogh_vezarat_kar_tot'))
            detail.hoghoogh_vezarat_kar_tot = my_int(hoghoogh_vezarat_kar_tot)
            positive_taraz = salary_sheet.cell_value(row_idx, cols.index('positive_taraz'))
            detail.positive_taraz = my_int(positive_taraz)
            mazaya = salary_sheet.cell_value(row_idx, cols.index('mazaya'))
            detail.mazaya = my_int(mazaya)
            extra_shift = salary_sheet.cell_value(row_idx, cols.index('extra_shift'))
            detail.extra_shift = my_int(extra_shift)
            extra_shift_fee = salary_sheet.cell_value(row_idx, cols.index('extra_shift_fee'))
            detail.extra_shift_fee = my_int(extra_shift_fee)
            del_sal = salary_sheet.cell_value(row_idx, cols.index('del_sal'))
            detail.del_sal = my_int(del_sal)
            del_sal_fee = salary_sheet.cell_value(row_idx, cols.index('del_sal_fee'))
            detail.del_sal_fee = my_int(del_sal_fee)
            off = salary_sheet.cell_value(row_idx, cols.index('off'))
            detail.off = my_int(off)
            off_fee = salary_sheet.cell_value(row_idx, cols.index('off_fee'))
            detail.off_fee = my_int(off_fee)
            extra_hours = salary_sheet.cell_value(row_idx, cols.index('extra_hours'))
            detail.extra_hours = my_int(extra_hours)
            extra_hours_fee = salary_sheet.cell_value(row_idx, cols.index('extra_hours_fee'))
            detail.extra_hours_fee = my_int(extra_hours_fee)

            eydi = salary_sheet.cell_value(row_idx,cols.index('eydi'))
            if my_int(eydi) == None:
                detail.eydi = 0
            else:
                detail.eydi = my_int(eydi)

            vacation_rem = salary_sheet.cell_value(row_idx, cols.index('vacation_rem'))

            if my_int(vacation_rem) == None:
                detail.vacation_rem = 0
            else:
                detail.vacation_rem = my_int(vacation_rem)

            vacation_rem_fee = salary_sheet.cell_value(row_idx, cols.index('vacation_rem_fee'))
            if my_int(vacation_rem_fee) == None:
                detail.vacation_rem_fee = 0
            else:
                detail.vacation_rem_fee = my_int(vacation_rem_fee)

            reward = salary_sheet.cell_value(row_idx, cols.index('reward'))
            detail.reward = my_int(reward)
            snapp = salary_sheet.cell_value(row_idx, cols.index('snapp'))
            detail.snapp = my_int(snapp)
            hoghoogh_mazaya_plus = salary_sheet.cell_value(row_idx, cols.index('hoghoogh_mazaya_plus'))
            detail.hoghoogh_mazaya_plus = my_int(hoghoogh_mazaya_plus)
            help = salary_sheet.cell_value(row_idx, cols.index('help'))
            detail.help = my_int(help)
            negative_taraz = salary_sheet.cell_value(row_idx, cols.index('negative_taraz'))
            detail.negative_taraz = my_int(negative_taraz)
            other_deduction = salary_sheet.cell_value(row_idx, cols.index('other_deduction'))
            detail.other_deduction = my_int(other_deduction)
            fine = salary_sheet.cell_value(row_idx, cols.index('fine'))
            detail.fine = my_int(fine)
            bime = salary_sheet.cell_value(row_idx, cols.index('bime'))
            detail.bime = my_int(bime)
            maliat = salary_sheet.cell_value(row_idx, cols.index('maliat'))
            detail.maliat = my_int(maliat)
            kosoorat_sum = salary_sheet.cell_value(row_idx, cols.index('kosoorat_sum'))
            detail.kosoorat_sum = my_int(kosoorat_sum)
            pardakhti = salary_sheet.cell_value(row_idx, cols.index('pardakhti'))
            detail.pardakhti = my_int(pardakhti)
            karfarma_bime = salary_sheet.cell_value(row_idx, cols.index('karfarma_bime'))
            detail.karfarma_bime = my_int(karfarma_bime)
            account = salary_sheet.cell_value(row_idx, cols.index('account'))
            card = salary_sheet.cell_value(row_idx, cols.index('card'))
            bank = salary_sheet.cell_value(row_idx, cols.index('bank'))
            bank,bankexists = Bank.objects.get_or_create(bank_name=bank)
            bank_account = BankAccount.objects.get(id = 94)
            if account != '' and card != '':
                bank_account,bexists = BankAccount.objects.get_or_create(account=account, card=card, shaba='-', bank=bank)
            if bank_account.id == 94:
                bank_account = person.banks.all().last()

            detail.account = bank_account
            detail.description = desc

            detail.save()
            
        from_date = jdatetime.datetime.strptime(salary_sheet.cell_value(salary_sheet.nrows-1, 3),'%Y/%m/%d')
        to_date = jdatetime.datetime.strptime(salary_sheet.cell_value(salary_sheet.nrows-1, 5),'%Y/%m/%d')

        salary.from_date = from_date
        salary.to_date = to_date
        salary.save()


    else:
        return JsonResponse({'res': 'err'})

    return redirect(request.META['HTTP_REFERER'])
# def upload_salary(request):

#     def my_int(num):
#         if num != '':
#             return int(num)
#         else:
#             return None

#     if not request.user.is_authenticated:
#         return JsonResponse({'res':'no'})

#     if request.method == 'POST' and request.FILES['salary']:

#         date = jdatetime.datetime.strptime(request.POST['date'],'%Y-%m-%d')
#         branch = int(request.POST['branch'])
        
        
#         if branch != 9:
#             salary,exists = Salary.objects.get_or_create(month=date,branch=Branch.objects.get(id=branch))
#         else:
#             salary,exists = Salary.objects.get_or_create(month=date,branch=None)


#         input_excel = request.FILES['salary']
#         book = xlrd.open_workbook(file_contents=input_excel.read())

#         salary_sheet = book.sheet_by_index(0)
        
#         notes = salary_sheet.cell_note_map

#         for row_idx in range(2, salary_sheet.nrows-2):

#             name = salary_sheet.cell_value(row_idx, 1)
#             person = Person.objects.get(name=name)

#             try:
#                 detail, dexists = SalaryDetail.objects.get_or_create(salary=salary,person=person)
#             except:
#                 detail = SalaryDetail(salary=salary,person=person)

#             detail.add_date=jdatetime.datetime.now()
#             detail.payment_status='registered'
#             detail.add_user=request.user

        

#             desc = ''
#             for key in notes.keys():
#                 if key[0] == row_idx:
#                     desc = '%s \n %s'%(desc,notes[key].text)

#             title = salary_sheet.cell_value(row_idx, 2)
#             days = salary_sheet.cell_value(row_idx, 3)
#             detail.days = my_int(days)
#             fix = salary_sheet.cell_value(row_idx, 4)
#             detail.fix = my_int(fix)
#             base = salary_sheet.cell_value(row_idx, 5)
#             detail.base = my_int(base)
#             agreement = salary_sheet.cell_value(row_idx, 6)
#             detail.agreement = my_int(agreement)
#             maskan = salary_sheet.cell_value(row_idx, 7)
#             detail.maskan = my_int(maskan)
#             childs = salary_sheet.cell_value(row_idx, 8)
#             detail.childs = my_int(childs)
#             childs_money = salary_sheet.cell_value(row_idx, 9)
#             detail.childs_money = my_int(childs_money)
#             bon = salary_sheet.cell_value(row_idx, 10)
#             detail.bon = my_int(bon)
            
#             hoghoogh_vezarat_kar_tot = salary_sheet.cell_value(row_idx, 11)
#             detail.hoghoogh_vezarat_kar_tot = my_int(hoghoogh_vezarat_kar_tot)
#             positive_taraz = salary_sheet.cell_value(row_idx, 12)
#             detail.positive_taraz = my_int(positive_taraz)
#             sanavat = salary_sheet.cell_value(row_idx, 13)
#             detail.sanavat = my_int(sanavat)
#             mazaya = salary_sheet.cell_value(row_idx, 14)
#             detail.mazaya = my_int(mazaya)
#             extra_shift = salary_sheet.cell_value(row_idx, 15)
#             detail.extra_shift = my_int(extra_shift)
#             extra_shift_fee = salary_sheet.cell_value(row_idx, 16)
#             detail.extra_shift_fee = my_int(extra_shift_fee)
#             del_sal = salary_sheet.cell_value(row_idx, 17)
#             detail.del_sal = my_int(del_sal)
#             del_sal_fee = salary_sheet.cell_value(row_idx, 18)
#             detail.del_sal_fee = my_int(del_sal_fee)
#             off = salary_sheet.cell_value(row_idx, 19)
#             detail.off = my_int(off)
#             off_fee = salary_sheet.cell_value(row_idx, 20)
#             detail.off_fee = my_int(off_fee)
#             extra_hours = salary_sheet.cell_value(row_idx, 21)
#             detail.extra_hours = my_int(extra_hours)
#             extra_hours_fee = salary_sheet.cell_value(row_idx, 22)
#             detail.extra_hours_fee = my_int(extra_hours_fee)
#             reward = salary_sheet.cell_value(row_idx, 23)
#             detail.reward = my_int(reward)
#             snapp = salary_sheet.cell_value(row_idx, 24)
#             detail.snapp = my_int(snapp)
#             hoghoogh_mazaya_plus = salary_sheet.cell_value(row_idx, 25)
#             detail.hoghoogh_mazaya_plus = my_int(hoghoogh_mazaya_plus)
#             help = salary_sheet.cell_value(row_idx, 26)
#             detail.help = my_int(help)
#             negative_taraz = salary_sheet.cell_value(row_idx, 27)
#             detail.negative_taraz = my_int(negative_taraz)
#             other_deduction = salary_sheet.cell_value(row_idx, 28)
#             detail.other_deduction = my_int(other_deduction)
#             fine = salary_sheet.cell_value(row_idx, 29)
#             detail.fine = my_int(fine)
#             bime = salary_sheet.cell_value(row_idx, 30)
#             detail.bime = my_int(bime)
#             maliat = salary_sheet.cell_value(row_idx, 31)
#             detail.maliat = my_int(maliat)
#             kosoorat_sum = salary_sheet.cell_value(row_idx, 32)
#             detail.kosoorat_sum = my_int(kosoorat_sum)
#             pardakhti = salary_sheet.cell_value(row_idx, 33)
#             detail.pardakhti = my_int(pardakhti)
#             karfarma_bime = salary_sheet.cell_value(row_idx, 34)
#             detail.karfarma_bime = my_int(karfarma_bime)
#             account = salary_sheet.cell_value(row_idx, 35)
#             card = salary_sheet.cell_value(row_idx, 36)
#             bank = salary_sheet.cell_value(row_idx, 37)
#             bank,bankexists = Bank.objects.get_or_create(bank_name=bank)
#             bank_account,bexists = BankAccount.objects.get_or_create(account=account, card=card, shaba='-', bank=bank)
#             detail.account = bank_account
#             detail.description = desc

#             detail.save()


#     else:
#         return JsonResponse({'res': 'err'})

#     return redirect(request.META['HTTP_REFERER'])
