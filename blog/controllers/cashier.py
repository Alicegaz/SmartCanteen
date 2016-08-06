from blog.models import CashierHist, Offers
from common.permission import have_permission
from django.utils import timezone
from datetime import date


def contain_begin(request):
    try:
        s = request.POST.get('begin')
        if s is None:
            return False
        else:
            return s
    except:
        return False


def contain_end(request):
    try:
        s = request.POST.get('end')
        if s is None:
            return False
        else:
            return s
    except:
        return False


def contain_jackpot(request):
    try:
        s = request.POST.get('jackpot')
        if s is None:
            return False
        else:
            return s
    except:
        return False


def cashier_history_create(request):
    begin = contain_begin(request)
    end = contain_end(request)
    user = have_permission(request, ['blog.can_edit_schedule'])
    if user:
        if bool(begin) != bool(end):
            if begin:
                hist = CashierHist.objects.filter(date=timezone.now(), end_time=None)
                if not hist.__len__():
                    cash_hist = CashierHist()
                    cash_hist.cashier = user
                    cash_hist.save()
                    return True
                else:
                    return False
            elif end:
                cash_hist = CashierHist.objects.get(date=timezone.now(), end_time=None)
                cash_hist.end_time = timezone.now()
                summ = 0
                cuant = 0
                for offer in Offers.objects.all():
                    if cash_hist.begin_time.date()<=offer.date.date()<= date.today():
                        summ += offer.offer_price()
                        cuant +=1
                cash_hist.jackpot = summ
                # TODO присваивать cash_hist.jackpot значение суммы всех заказов за период с begin time по настоящее время
                cash_hist.save()
                return True
    return False
