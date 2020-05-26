from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import  AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UpdateInfo,RegistrationForm
from accounting.models import Plans
from .models import Emailer, Feature


def index(request):
    login_form = AuthenticationForm()
    plans = Plans.objects.all()

    return render(request, 'main.html', {'login_form': login_form, 'plans':plans})

@login_required
def home(request):

    login_form = AuthenticationForm()

    user = User.objects.get(username=request.user.username)
    feature = Feature.objects.get(user=request.user.id)

    if not feature.id:
        feature = Feature.objects.create(feature_type= "Basic", user=user)

    if not user.first_name or not user.last_name:
        return redirect('update_info')
    users = User.objects.all()
    return render(request, 'home.html', {'login_form': login_form, 'users': users})

@login_required
def update_info(request):
    login_form = AuthenticationForm()
    user = User.objects.get(username=request.user.username)
    
    if request.method == 'POST':
        form = UpdateInfo(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
    
    form = UpdateInfo()
    if user.first_name or user.last_name:
        return redirect('home')

    return render(request, 'update_info.html', {'form': form, 'login_form': login_form})


@login_required
def profile(request):
    login_form = AuthenticationForm()
    user = User.objects.get(username=request.user.username)
    return render(request, 'profile.html', {'login_form': login_form})


def commin_soon(request):
    return render(request, 'commin-soon.html', {})


def debug(request):
    login_form = AuthenticationForm()
    return render(request, 'debug.html', {'login_form': login_form})

@login_required
def settings(request):
    login_form = AuthenticationForm()
    user = User.objects.get(username=request.user.username)
    return render(request, 'settings.html', {'login_form': login_form})

def disabled(request):
    return render(request, 'disabled.html', {})


#signtup page tacking id of the selected item as an argument
def signup(request, id):
    if Plans.objects.filter(id=id).exists():  
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()

                user = authenticate(username=request.POST['username'], password=request.POST['password1'])
                login(request, user)

                plan = Plans.objects.filter(id=id).first()
                related_user = User.objects.get(username=request.user.username)
        
                feature = Feature.objects.create(feature_type= "Basic", user=related_user)

                if plan.price == 'Free':
                    return redirect('/profile')

                return redirect(f'/accounting/paypal/{id}')

        else:
            form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})


#subscription to the newsletter using the emailer model
def newsletter(request):
    if request.method == 'POST':
        email = request.POST['email']
        emailer = Emailer()
        emailer.send_email(email)
        welcome = "Welcome to our newsletter"
        return render(request, 'newsletter/newsletter.html',{'welcome':welcome})
             
    return render(request,'newsletter/newsletter.html')






