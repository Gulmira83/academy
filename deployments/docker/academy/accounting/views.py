from django.shortcuts import render
from .models import Plans

from main.models import Feature
from django.http import JsonResponse
import json


# Create your views here.

#we are passing the id of the plan with the url
def index(request, id):
    if Plans.objects.filter(id=id).exists():  
        plan = Plans.objects.filter(id=id)

    return render(request, 'paypal.html', {'plan':plan})



def paymentComplete(request):
    body = json.loads(request.body)
    plan = Plans.objects.get(id=body['productId'])

    feature = Feature.objects.filter(user=request.user).update(payment_confirmation='True',feature_type=str(plan))

    return JsonResponse('payment completed!', safe=False)
