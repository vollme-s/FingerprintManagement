from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.context_processors import csrf

from fingerprint.models import Door
from fingerprint.models import Fingerprint
from sensor.HardwareMain import setTemplate, deleteTemplate


@user_passes_test(lambda u: u.is_staff, login_url='/fingerprint/accounts/login/?priv=Admin')
def home_admin(request):
    return render_to_response("fingerprint/admin/home_admin.html")


@user_passes_test(lambda u: u.is_staff, login_url='/fingerprint/accounts/login/?priv=Admin')
def users_admin(request):
    user_list = User.objects.all().order_by('username')
    context = {'user_list': user_list,
               }
    return render_to_response("fingerprint/admin/users_admin.html", context)


@user_passes_test(lambda u: u.is_staff, login_url='/fingerprint/accounts/login/?priv=Admin')
def edit_user_admin(request, user_id):
    user = User.objects.filter(id=user_id).first()
    door_list = Door.objects.all().order_by('name')
    user_door_list = Door.objects.filter(allowed_users=user).order_by('name')
    is_staff = user.is_staff
    if is_staff:
        option = 'checked'
    else:
        option = ''
    context = {'user': user,
               'door_list': door_list,
               'user_door_list': user_door_list,
               'is_staff': is_staff,
               'option': option, }
    context.update(csrf(request))
    return render_to_response("fingerprint/admin/edit_user_admin.html", context)


@user_passes_test(lambda u: u.is_staff, login_url='/fingerprint/accounts/login/?priv=Admin')
def save_admin_user_changes(request, user_id):
    user = User.objects.filter(id=user_id).first()
    template = Fingerprint.objects.filter(user=user).first()
    is_staff = request.POST.get('is-staff-check', '')
    door_list = Door.objects.all().order_by('name')
    for door in door_list:
        door_access = request.POST.get(door.name, '')
        if door_access == 'on':
            door.allowed_users.add(user)
            if(template):
                setTemplate(template.template)
        else:
            door.allowed_users.remove(user)
            if(template):
                deleteTemplate(template.template)
        door.save()

    if is_staff == 'on':
        is_staff = True
    else:
        is_staff = False

    user.is_staff = is_staff
    user.save()

    return redirect("/fingerprint/users_admin/%s/" %user.id)


@user_passes_test(lambda u: u.is_staff, login_url='/fingerprint/accounts/login/?priv=Admin')
def doors_admin(request):
    door_list = Door.objects.all().order_by('name')
    context = {'door_list': door_list,
               }
    context.update(csrf(request))
    return render_to_response("fingerprint/admin/doors_admin.html", context)


def add_door_admin(request):
    door_name = request.POST.get('door_name', '')
    if door_name.strip():
        Door.objects.create(name = door_name)
    return redirect("/fingerprint/doors_admin/")


def edit_door_admin(request, door_id):
    door = Door.objects.filter(id=door_id).first()
    user_list = User.objects.all().order_by('username')
    door_user_list = door.allowed_users.all().order_by('username')
    context = {'door': door,
               'user_list': user_list,
               'door_user_list': door_user_list, }
    context.update(csrf(request))
    return render_to_response("fingerprint/admin/edit_door_admin.html", context)


def save_admin_door_changes(request, door_id):
    door = Door.objects.filter(id=door_id).first()
    user_list = User.objects.all().order_by('username')
    for user in user_list:
        user_allowed = request.POST.get(user.username, '')
        template = Fingerprint.objects.filter(user=user).first()
        if user_allowed == 'on':
            door.allowed_users.add(user)
            if(template):
                setTemplate(template.template)
        else:
            door.allowed_users.remove(user)
            if(template):
                deleteTemplate(template.template)
    door.save()
    return redirect("/fingerprint/doors_admin/%s/" %door.id)
