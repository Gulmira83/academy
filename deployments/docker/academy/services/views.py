from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserServiceForm, UserServiceFormDelete
from django.conf import settings
import logging
from .models import Pynote, UserService
from django.contrib.auth.models import User



@login_required
def services(request):
    environment = getattr(settings, 'ENVIRONMENT', None),
    pynote = Pynote()

    services = [
        pynote
        ]

    form = UserServiceForm()
    user = User.objects.get(id=request.user.id)
    form = UserServiceForm()
    if request.method == 'POST':
        form = UserServiceForm(request.POST)
        if form.is_valid():
            if not UserService.objects.filter(username=user.id).exists():
                user_service = form.save(commit=False)
                user_service.username = user
                user_service.service  = pynote.name
                user_service.path     = f"/services/user-services/{user.username}"

                pynote.create_service(
                    f"{user.username}", 
                    f"{user_service.password}", 
                    f"/services/user-services/{user.username}"
                    )

                user_service.save()
                return redirect(f'user-services')
            else:
                return redirect(f'user-services')
    return render(request, 'services.html', {"services" : services, 'form': form})

@login_required
def user_services(request, id=None):
    user = User.objects.get(id=request.user.id)
    services = UserService.objects.all()
    form = UserServiceForm()
    if request.method == 'DELETE':
        form = UserServiceForm(request.DELETE)
        if form.is_valid():
            user_service = form.delete()
            return redirect(f'user-services')
    return render(request, 'user-services.html', {"services": services})


@login_required
def user_service_delete(request, name=None):
    user     = User.objects.get(id=request.user.id)
    service = UserService.objects.filter(username=user).first()
    form = UserServiceFormDelete()
    if request.method == 'POST':
        form = UserServiceFormDelete(request.POST)
        if form.is_valid():
            form.delete()
    return render(request, 'user-service-delete.html', {"services": services, "form": form})