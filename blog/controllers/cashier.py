from blog.models import CashierHistory


def contain_offer(request):
    try:
        s = request.POST.get('offer')
        if s is None:
            return False
        else:
            return True
    except:
        return False

def cashier_history_create(request):
