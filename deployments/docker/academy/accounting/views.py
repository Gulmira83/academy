from django.shortcuts import render
from .models import Plans
from django.contrib.auth.decorators import login_required
from main.models import Feature
from django.http import JsonResponse
import json


# Create your views here.

#we are passing the id of the plan with the url
@login_required
def index(request, id):
    if Plans.objects.filter(id=id).exists():  
        plan = Plans.objects.filter(id=id)

    return render(request, 'paypal.html', {'plan':plan})


@login_required
def paymentComplete(request):
    body = json.loads(request.body)
    plan = Plans.objects.get(id=body['productId'])

    # request_price = body['total']
    feature = Feature.objects.filter(user=request.user).update(payment_confirmation='True',feature_type=str(plan))
    
    return JsonResponse('payment completed!', safe=False)


@login_required
def declinedPayment(request):
    return render(request, 'declined-payment.html')

@login_required
def successPayment(request):
    return render(request, 'success-payment.html')