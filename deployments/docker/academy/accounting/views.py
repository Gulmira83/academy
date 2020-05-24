from django.shortcuts import render
from .models import Plans

# Create your views here.

#we are passing the id of the plan with the url
def index(request, id):
    if Plans.objects.filter(id=id).exists():  
        plan = Plans.objects.filter(id=id)

    return render(request, 'paypal.html', {'plan':plan})
