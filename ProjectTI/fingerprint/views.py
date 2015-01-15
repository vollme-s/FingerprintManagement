from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from fingerprint.models import Fingerprint
from fingerprint.models import Door
from fingerprint.models import Log
from sensor.HardwareMain import enrollment

# Create your views here.

@login_required(login_url='/fingerprint/accounts/login/')
def home_user(request):
    return render_to_response('fingerprint/home_user.html')


@login_required(login_url='/fingerprint/accounts/login/')
def doors_user(request):
    door_log_dict = {}
    user = request.user
    myDoor_list = Door.objects.filter(allowed_users=user)
    for door in myDoor_list:
        log_list = Log.objects.filter(user=user,door=door)
        dict_temp = {log_list:door}
        door_log_dict.update(dict_temp)

    context = {'user': user,
               'door_log_dict': door_log_dict}
    return render_to_response("fingerprint/doors_user.html", context)


@login_required(login_url='/fingerprint/accounts/login/')
def profile_user(request):
    user = request.user
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    context = {'username': username,
               'first_name': first_name,
               'last_name': last_name,
               'email': email}
    context.update(csrf(request))
    return render_to_response("fingerprint/profile_user.html", context)


@login_required(login_url='/fingerprint/accounts/login/')
def save_profile_changes(request):
    user = request.user
    username = request.POST.get('username', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    oldpass = request.POST.get('old_password','')
    newpass = request.POST.get('new_password','')

    if username and email:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if (oldpass and newpass):
            if (user.check_password(oldpass)):
                user.set_password(newpass)            
        user.save()
    return redirect("/fingerprint/profile_user/")


@login_required(login_url='/fingerprint/accounts/login/')
def fingerprint_user(request):
    user = request.user
    username = user.username
    fingerprint = Fingerprint.objects.filter(user=user).first()
    context = {'username': username,
               'fingerprint': fingerprint}
    return render_to_response("fingerprint/fingerprint_user.html", context)

@login_required(login_url='/fingerprint/accounts/login/')
def start_enrollment(request):
    user = request.user
    username = user.username
    fingerprint = Fingerprint.objects.filter(user=user)
    if(fingerprint):
        fingerprint[0].delete()
    retVal = enrollment()
    print(retVal)
    if(retVal != False):
        print("true")
        Fingerprint.objects.create(user=user, template=retVal)
    else:
        print("false")
        
    return redirect("/fingerprint/fingerprint_user/")
        


