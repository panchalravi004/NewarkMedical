from django.contrib import admin
from app.models import *

admin.site.register(Department)
admin.site.register(Room)
admin.site.register(Allergy)
admin.site.register(Diagnosis)
admin.site.register(Patient)
admin.site.register(Staff)
admin.site.register(Appointment)
admin.site.register(PatientHasAllergy)
admin.site.register(PatientHasDiagnosis)
admin.site.register(ConditionCheck)
admin.site.register(Surgery)
    