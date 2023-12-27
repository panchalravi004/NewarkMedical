from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.EmailBackEnd import EmailBackEnd
from app.models import *
from app.decorators import *
from app.templatetags.filterData import *
from app.script import create
def getCurrentURL(request):
    return request.META.get('HTTP_REFERER', '/default-url/')

@unathenticated_user
def REGISTER(request):
    return render(request,"registration/register.html")

@unathenticated_user
def LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST.get('pass')
        user = EmailBackEnd.authenticate(request,username=email,password=pwd)

        if user != None:
            login(request,user)
            position = getCurrentUserPosition(user)
            if position == 'Patient':
                patient = getPatient(user)
                return redirect('patient-details', patient.id)

            return redirect('home')
        else:
            messages.warning(request,'Email or Password Are Invalid !')
            return redirect('login')

    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@unathenticated_user
def CREATEACCOUNT(request):

    if request.method == "POST":
        email = request.POST.get('email')
        number = request.POST.get('number')
        pwd = request.POST.get('pass')
        re_pwd = request.POST.get('repass')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        userPosition = request.POST.get('userPosition')
        gender = request.POST.get('gender')
        userShift = request.POST.get('userShift')
        dept = request.POST.get('dept')

        uname = "{}{}".format(fname,lname)

        isUserExists = User.objects.filter(email=email)

        if isUserExists.exists():
            messages.warning(request,'User with email already exists !')
            return redirect(getCurrentURL(request))

        if pwd != re_pwd:
            messages.warning(request,'Password does not match !')
            return redirect(getCurrentURL(request))

        user = User(
            username=uname,
            first_name=fname,
            last_name=lname,
            email=email,
        )
        user.set_password(pwd)
        user.save()
        
        dept = Department.objects.get(id=int(dept))

        staff = Staff(
            user=user,
            department=dept,
            position=userPosition,
            gender=gender,
            shift=userShift,
            dob=None,
            address=address,
            number=number,
        )

        staff.save()

        # messages.success(request,'Email and Password Are Invalid !')
        return redirect('login')
    
    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
def LOGOUT(request):
    logout(request)
    return redirect('login')
