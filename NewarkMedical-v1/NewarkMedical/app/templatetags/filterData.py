from django import template
import math
from django.db.models import Sum
from app.models import *
register = template.Library()

@register.simple_tag
def getDepartment():
    dept = Department.objects.all()
    return dept

@register.simple_tag
def getEllipsis(value, char=20):
    return str(value)[:char]

@register.simple_tag
def getCurrentUserPosition(user):
    staff = Staff.objects.filter(user=user)
    patient = Patient.objects.filter(user=user)
    position = 'Admin'
    if staff.exists():
        position = staff.first().position
    else:
        if patient.exists():
            position = 'Patient'
    return position

@register.simple_tag
def getPatient(user):
    patient = Patient.objects.filter(user=user)
    if patient.exists():
        return patient.first()
    return None