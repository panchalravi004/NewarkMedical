from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name
    
class Room(models.Model):
    number = models.CharField(max_length=100)
    floor = models.CharField(max_length=100)
    department = models.ForeignKey(Department,null=True,on_delete=models.SET_NULL)
    isAvailable = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.department.name+' '+self.number

class Allergy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name

class Diagnosis(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name
    
class Patient(models.Model):
    GENDER = [ 
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER)
    dob = models.DateField()
    address = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def patient_id(self):
        return "P_" + str(self.id)
        
    def __str__(self):
        return self.user.first_name

class Staff(models.Model):
    GENDER = [ 
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    POSITION = [
        ('NURSE','NURSE'),
        ('DOCTOR', 'DOCTOR'),
        ('RECEPTIONIST', 'RECEPTIONIST'),
    ]

    SHIFT = [
        ('9AM-5PM','9AM-5PM'),
        ('6PM-12AM', '6PM-12AM'),
        ('12AM-6AM', '12AM-6AM')
    ]

    user = models.OneToOneField(User, null=True, blank= True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True)
    position = models.CharField(max_length=100, choices=POSITION)
    gender = models.CharField(max_length=10, choices=GENDER)
    shift = models.CharField(max_length=35, choices=SHIFT)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def staff_id(self):
        if self.position == 'NURSE':
            return "N_" + str(self.id)
        elif self.position == 'DOCTOR':
            return "D_" + str(self.id)
        elif self.position == 'RECEPTIONIST':
            return "R_" + str(self.id)

    def __str__(self):
        return self.staff_id+' '+ self.user.first_name+' '+self.position

class Appointment(models.Model):
    STATUS = [ 
        ('Pending', 'Pending'),
        ('InProgress', 'InProgress'),
        ('Completed', 'Completed'),
    ]

    patient = models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Staff,null=True, related_name='doctor_appts',on_delete=models.SET_NULL)
    nurse = models.ForeignKey(Staff,null=True, related_name='nurse_appts',on_delete=models.SET_NULL)
    receptionits = models.ForeignKey(Staff,null=True, related_name='recep_appts',on_delete=models.SET_NULL)
    department = models.ForeignKey(Department,null=True,on_delete=models.SET_NULL)
    app_date = models.DateTimeField()
    status = models.CharField(max_length=35, choices=STATUS, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def app_id(self):
        return "A_" + str(self.id)
    
    def __str__(self):
        return str(self.patient.user.first_name + " " + str(self.app_date) + " " + self.doctor.user.first_name)
    
class PatientHasAllergy(models.Model):
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.SET_NULL)
    allergy = models.ForeignKey(Allergy, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.appointment.patient.user.first_name+' '+self.allergy.name
    
class PatientHasDiagnosis(models.Model):
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.SET_NULL)
    diagnosis = models.ForeignKey(Diagnosis, null=True, on_delete=models.SET_NULL)
    treatment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.appointment.patient.user.first_name

class ConditionCheck(models.Model):

    MENTAL_STATE = [
        ('Stable','Stable'),
        ('Mildly distressed','Mildly distressed'),
        ('Moderately distressed','Moderately distressed'),
        ('Severely distressed','Severely distressed'),
        ('Acutely psychotic','Acutely psychotic'),
    ]

    YES_NO = [
        ('Yes', 'Yes'),
        ('Sometimes','Sometimes'),
        ('No', 'No'),
    ]

    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.SET_NULL)
    nurse = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)

    heigth = models.CharField(max_length=5)
    weigth = models.CharField(max_length=5)

    urgency = models.CharField(max_length=15, choices=YES_NO)
    abnormal_breathing = models.CharField(max_length=15, choices=YES_NO)
    smokes = models.CharField(max_length=15, choices=YES_NO)
    drinks = models.CharField(max_length=15, choices=YES_NO)
    has_headache = models.CharField(max_length=15, choices=YES_NO)
    mental_state = models.CharField(max_length=50, choices=MENTAL_STATE)

    heart_rate = models.CharField(max_length=20)
    blood_presure = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)

    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.appointment.patient.user.first_name+' '+self.nurse.user.first_name+' '+str(self.created_date)

class Surgery(models.Model):
    STATUS = [ 
        ('Pending', 'Pending'),
        ('InProgress', 'InProgress'),
        ('Completed', 'Completed'),
    ]
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.SET_NULL)
    nurse = models.ForeignKey(Staff, null=True, related_name='nurse_surgery',on_delete=models.SET_NULL)
    surgeon = models.ForeignKey(Staff, null=True, related_name='surgeon_surgery',on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    surgery_date = models.DateTimeField()
    status = models.CharField(max_length=35, choices=STATUS, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.appointment.patient.user.first_name+' '+self.surgeon.user.first_name+' '+self.surgery_date+' '+self.status


