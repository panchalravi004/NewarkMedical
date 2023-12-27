from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from app.models import *
from app.decorators import *

def getCurrentURL(request):
    return request.META.get('HTTP_REFERER', '/default-url/')

def BASE(request):
          
    return render(request,"base.html")

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def HOME(request):
    appList = Appointment.objects.all().order_by('-status','-app_date')
    deptList = Department.objects.all().order_by('-created_date')
    patientList = Patient.objects.all().order_by('-created_date')
    doctorList = Staff.objects.filter(position='DOCTOR').order_by('-created_date')
    nurseList = Staff.objects.filter(position='NURSE').order_by('-created_date')
    surgeryList = Surgery.objects.filter(status='InProgress').order_by('-surgery_date')

    data = {
        'appList':appList,
        'deptList':deptList,
        'patientList':patientList,
        'doctorList':doctorList,
        'nurseList':nurseList,
        'surgeryList':surgeryList
    }

    return render(request,"home.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'DOCTOR', 'RECEPTIONIST'])
def MANAGE_ALLERGY(request):
    allergyList = Allergy.objects.all().order_by('-created_date')
    data = {
        'allergyList':allergyList
    }

    return render(request,"manage-allergy.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def MANAGE_APPOINTMENT(request):
    
    appList = Appointment.objects.all().order_by('app_date','-status')
    deptList = Department.objects.all().order_by('-created_date')
    patientList = Patient.objects.all().order_by('-created_date')
    doctorList = Staff.objects.filter(position='DOCTOR').order_by('-created_date')
    nurseList = Staff.objects.filter(position='NURSE').order_by('-created_date')

    data = {
        'appList':appList,
        'deptList':deptList,
        'patientList':patientList,
        'doctorList':doctorList,
        'nurseList':nurseList
    }

    return render(request,"manage-appointment.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'DOCTOR', 'RECEPTIONIST'])
def MANAGE_DIAGNOSES(request):
    diagnosesList = Diagnosis.objects.all().order_by('-created_date')

    data = {
        'diagnosesList':diagnosesList
    }

    return render(request,"manage-diagnoses.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'DOCTOR', 'RECEPTIONIST'])
def MANAGE_MEMBER(request):
    
    memberList = Staff.objects.all().order_by('-created_date')

    data = {
        'memberList':memberList
    }

    return render(request,"manage-member.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def MANAGE_PATIENT(request):

    patientList = Patient.objects.all().order_by('-created_date')
    
    data = {
        'patientList':patientList
    }

    return render(request,"manage-patient.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'DOCTOR', 'RECEPTIONIST'])
def MANAGE_ROOMS(request):

    roomList = Room.objects.all().order_by('-created_date')
    
    data = {
        'roomList':roomList
    }

    return render(request,"manage-rooms.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def PATIENT_ADD(request):

    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        uname = "{}{}".format(fname,lname)

        user = User(
            username=uname,
            first_name=fname,
            last_name=lname,
            email=email,
        )
        user.set_password(email)
        user.save()

        patient = Patient(
            user=user,
            number=mobile,
            gender=gender,
            dob=dob,
            address=address
        )
        patient.save()

        # print(patient.patient_id)

        return redirect('patient-details',patient.id)
    
    data = {}

    return render(request,"patient-add.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def MEMBER_ADD(request):
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
        return redirect('manage-member')
    
    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def APPOINTMENT_ADD(request):
    if request.method == "POST":
        patient = request.POST.get('patient')
        doctor = request.POST.get('doctor')
        nurse = request.POST.get('nurse')
        dept = request.POST.get('dept')
        appDate = request.POST.get('appDate')

        patient = Patient.objects.get(id=int(patient))
        doctor = Staff.objects.get(id=int(doctor)) if doctor else None
        nurse = Staff.objects.get(id=int(nurse)) if nurse else None
        reception = Staff.objects.filter(user=request.user)
        dept = Department.objects.get(id=int(dept))

        appointment = Appointment(
            patient=patient,
            department=dept,
            app_date=appDate,
            status='Pending',
        )
        if doctor:
            appointment.doctor= doctor
        if nurse:
            appointment.nurse= nurse
        if reception.exists():
            appointment.receptionits= reception.first()
        appointment.save()

        return redirect(getCurrentURL(request))

    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'DOCTOR', 'RECEPTIONIST'])
def ROOM_ADD(request):
    if request.method == "POST":
        number = request.POST.get('number')
        floor = request.POST.get('floor')
        dept = request.POST.get('dept')
        isAvailable = request.POST.get('isAvailable')

        dept = Department.objects.get(id=int(dept))

        room = Room(
            number=number,
            floor=floor,
            department=dept,
            isAvailable=bool(isAvailable),
        )
        room.save()
        return redirect('manage-rooms')
    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'DOCTOR', 'RECEPTIONIST'])
def DIAGONSES_ADD(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        print('title '+title)
        print('description '+description)

        diagnoses = Diagnosis(
            name=title,
            description=description
        )
        diagnoses.save()

        return redirect('manage-diagnoses')
    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'DOCTOR', 'RECEPTIONIST'])
def ALLERGY_ADD(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        print('title '+title)
        print('description '+description)

        allergy = Allergy(
            name=title,
            description=description
        )
        allergy.save()

        return redirect('manage-allergy')
    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def APPOINTMENT_ADD_DIAGNOSES(request):
    if request.method == "POST":
        appId = request.POST.get('id')
        diaId = request.POST.get('diagnoses')
        treatment = request.POST.get('treatment')

        appId = Appointment.objects.get(id = int(appId))
        diaId = Diagnosis.objects.get(id = int(diaId))

        isExists = PatientHasDiagnosis.objects.filter(appointment=appId,diagnosis=diaId)
        
        if not isExists.exists():
            addDiagnoses = PatientHasDiagnosis(
                appointment=appId,
                diagnosis=diaId,
                treatment=treatment,
            )
            addDiagnoses.save()

        return redirect(getCurrentURL(request))

    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def APPOINTMENT_ADD_ALLERGY(request):
    if request.method == "POST":
        appId = request.POST.get('id')
        allId = request.POST.get('allergy')

        appId = Appointment.objects.get(id = int(appId))
        allId = Allergy.objects.get(id = int(allId))

        isExists = PatientHasAllergy.objects.filter(appointment=appId,allergy=allId)
        
        if not isExists.exists():
                
            addAllergy = PatientHasAllergy(
                appointment=appId,
                allergy=allId
            )
            addAllergy.save()

        return redirect(getCurrentURL(request))

    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def APPOINTMENT_ADD_CHECKUP(request):
    if request.method == "POST":
        appointment = request.POST.get('id')
        nurse = request.POST.get('nurse')
        heigth = request.POST.get('heigth')
        weigth = request.POST.get('weigth')
        urgency = request.POST.get('urgency')
        abnormal_breathing = request.POST.get('abnormal_breathing')
        smokes = request.POST.get('smokes')
        drinks = request.POST.get('drinks')
        has_headache = request.POST.get('has_headache')
        mental_state = request.POST.get('mental_state')
        heart_rate = request.POST.get('heart_rate')
        blood_presure = request.POST.get('blood_presure')
        temperature = request.POST.get('temperature')

        appointment = Appointment.objects.get(id=appointment)
        nurse = Staff.objects.get(id=nurse)

        checkup = ConditionCheck(
            appointment=appointment,
            nurse=nurse,
            heigth=heigth,
            weigth=weigth,
            urgency=urgency,
            abnormal_breathing=abnormal_breathing,
            smokes=smokes,
            drinks=drinks,
            has_headache=has_headache,
            mental_state=mental_state,
            heart_rate=heart_rate,
            blood_presure=blood_presure,
            temperature=temperature
        )
        checkup.save()

        return redirect(getCurrentURL(request))

    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def APPOINTMENT_ADD_SURGERY(request):
    if request.method == "POST":
        appointment = request.POST.get('id')
        nurse = request.POST.get('nurse')
        surgeon = request.POST.get('surgeon')
        room = request.POST.get('room')
        surgeryDate = request.POST.get('surgeryDate')
        status = request.POST.get('status')

        appointment = Appointment.objects.get(id=appointment)
        nurse = Staff.objects.get(id=nurse)
        surgeon = Staff.objects.get(id=surgeon)
        room = Room.objects.get(id=room)

        surgery = Surgery(
            appointment=appointment,
            nurse=nurse,
            surgeon=surgeon,
            room=room,
            surgery_date=surgeryDate,
            status=status
        )
        surgery.save()

        return redirect(getCurrentURL(request))

    messages.warning(request,'Invalid request method !')
    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def APPOINTMENT_UPDATE_STATUS(request,id,status):
    appointment = Appointment.objects.get(id=int(id))
    if status == 'Pending':
        appointment.status = 'InProgress'
        appointment.save()

    if status == 'InProgress':
        appointment.status = 'Completed'
        appointment.save()

    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST'])
def SURGERY_UPDATE_STATUS(request,id,status):
    surgery = Surgery.objects.get(id=int(id))
    if status == 'Pending':
        room = surgery.room
        room.isAvailable = False
        room.save()
        surgery.status = 'InProgress'
        surgery.save()

    if status == 'InProgress':
        room = surgery.room
        room.isAvailable = True
        room.save()
        surgery.status = 'Completed'
        surgery.save()


    return redirect(getCurrentURL(request))

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST','Patient'])
def PATIENT_DETAILS(request,id):

    patientData = Patient.objects.get(id=int(id))
    deptList = Department.objects.all().order_by('-created_date')
    doctorList = Staff.objects.filter(position='DOCTOR').order_by('-created_date')
    nurseList = Staff.objects.filter(position='NURSE').order_by('-created_date')
    nextAppointment = Appointment.objects.filter(~Q(status='Completed'), patient=patientData).order_by('app_date')
    lastCompletedAppointment = Appointment.objects.filter(~Q(status='Pending'), patient=patientData).order_by('app_date')
    appAllergyList = PatientHasAllergy.objects.filter(appointment = lastCompletedAppointment.first())
    data = {
        'patientData':patientData,
        'appAllergyList':appAllergyList,
        'deptList':deptList,
        'doctorList':doctorList,
        'nurseList':nurseList
    }
    if nextAppointment.exists():
        data['nextAppointment'] = nextAppointment.first()
    else:
        data['nextAppointment'] = None

    return render(request,"patient-details.html", data)

@login_required
@allowed_users(allowed_roles=['Admin', 'NURSE', 'DOCTOR', 'RECEPTIONIST','Patient'])
def APPOINTMENT_DETAILS(request,id):
    
    appointmentData = Appointment.objects.get(id=int(id))
    appDiagnosesList = PatientHasDiagnosis.objects.filter(appointment = appointmentData)
    appAllergyList = PatientHasAllergy.objects.filter(appointment = appointmentData)
    appCheckupList = ConditionCheck.objects.filter(appointment = appointmentData).order_by('-created_date')
    appSurgeryList = Surgery.objects.filter(appointment = appointmentData).order_by('-surgery_date')
    
    diagnosesList = Diagnosis.objects.all().order_by('-created_date')
    allergyList = Allergy.objects.all().order_by('-created_date')
    nurseList = Staff.objects.filter(position='NURSE').order_by('-created_date')
    surgeonList = Staff.objects.filter(position='DOCTOR').order_by('-created_date')
    roomList = Room.objects.filter(isAvailable=True).order_by('-created_date')
    data = {
        'appointmentData':appointmentData,
        'appDiagnosesList':appDiagnosesList,
        'appAllergyList':appAllergyList,
        'appCheckupList':appCheckupList,
        'appSurgeryList':appSurgeryList,
        'diagnosesList':diagnosesList,
        'allergyList':allergyList,
        'nurseList':nurseList,
        'surgeonList':surgeonList,
        'roomList':roomList
    }

    return render(request,"appointment-details.html", data)

@login_required
def VIEW_SURGERY_RECORDS(request):
    surgeryList = Surgery.objects.all().order_by('-surgery_date')

    data = {
        'surgeryList':surgeryList
    }

    return render(request,"view-surgery-records.html", data)