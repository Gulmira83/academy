from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import (UpdateInfo,
                    RegistrationForm,
                    UpdateSettingsForm,
                    faqForm,
                    )
from accounting.models import Plans
from .models import (NewsletterEmailer,
                     AdminEmailer,
                     FAQEmailer,
                     Feature,
                     Questions,
                     Notification)
from django.contrib.auth import update_session_auth_hash
import urllib
import json
from django.conf import  settings



def index(request):
    login_form = AuthenticationForm()
    plans = Plans.objects.all()

    return render(request, 'main.html', {'login_form': login_form, 'plans':plans})

@login_required
def home(request):

    login_form = AuthenticationForm()

    user = User.objects.get(username=request.user.username)

    feature = Feature.objects.filter(user=request.user)

    if not feature.exists():
        feature = Feature.objects.create(feature_type= "Basic", user=user)

    
    confirmation = Feature.objects.get(user=request.user)
    need_payment = False

    if confirmation.payment_confirmation == False:
        need_payment = True


    if not user.first_name or not user.last_name:
        return redirect('update_info')
    users = User.objects.all()
    return render(request, 'home.html', {'login_form': login_form, 'users': users, 'need_payment':need_payment})


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
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UpdateSettingsForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = UpdateSettingsForm(instance=request.user)
        args = {'form':form}
    
    return render(request, 'settings.html', args)

@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            alert = True
            return render(request, 'change_password.html', {'alert':alert})

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
    
        return render(request, 'change_password.html', args)



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
        emailer = NewsletterEmailer()
        emailer.send_email(email)
        welcome = "Welcome to our newsletter"
        return render(request, 'newsletter/newsletter.html',{'welcome':welcome})
             
    return render(request,'newsletter/newsletter.html')


def faq(request):
    from django.conf import  settings

    form = faqForm(request.POST)
    recaptcha = True
    secret = getattr(settings, 'GOOGLE_RECAPTCHA_SECRET_KEY', None)
    admin_email = getattr(settings, 'EMAIL_HOST_USER', None)
    public_key = getattr(settings, 'GOOGLE_RECAPTCHA_PUBLIC_KEY', None)

    if request.method == 'POST': 
        if form.is_valid():
            
            #recaptcha verification
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': secret,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
 
            if result['success']:

                #sending an email to the user 
                email = form.cleaned_data['email']     
                emailer = FAQEmailer()
                emailer.send_email(email)

                #sending an email to the admin 
                mailer = AdminEmailer()
                mailer.send_email(admin_email)


                form.save()
                message = True
                form = faqForm(request.POST)

                return redirect('/faq-success')
            
            else:
                form = faqForm(request.POST)
                failed_recaptcha = True
                recaptcha = True

                args = {'form':form, 'failed_recaptcha':failed_recaptcha, 'recaptcha':recaptcha,'public_key':public_key}
                return render(request, 'faq.html', args)
  
    
    args = {'form':form, 'recaptcha':recaptcha,'public_key':public_key}

    return render(request, 'faq.html',args)


@login_required
def faq_success(request):
    return render(request,'faq_success_msg.html')


def faq_review(request):
    questions = Questions.objects.all().order_by('-subject')

    args = {'questions':questions}
    return render(request,'faq_reviews.html',args)
