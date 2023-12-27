from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views,user_login

admin.site.site_header = "NMA Admin"
admin.site.site_title = "NMA Admin Portal"
admin.site.index_title = "Welcome to NMA Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE,name="base"),
    path('', views.HOME,name="home"),
    # path('manage-allergy/', views.MANAGE_ALLERGY, name="manage-allergy"),
    # path('manage-appointment/', views.MANAGE_APPOINTMENT, name="manage-appointment"),
    # path('manage-diagnoses/', views.MANAGE_DIAGNOSES, name="manage-diagnoses"),
    # path('manage-member/', views.MANAGE_MEMBER, name="manage-member"),
    path('manage-patient/', views.MANAGE_PATIENT, name="manage-patient"),
    # path('manage-rooms/', views.MANAGE_ROOMS, name="manage-rooms"),
    path('view-surgery-records/', views.VIEW_SURGERY_RECORDS, name="view-surgery-records"),
    path('patient-add/', views.PATIENT_ADD, name="patient-add"),
    
    path('patient-details/<int:id>', views.PATIENT_DETAILS, name="patient-details"),
    path('appointment-details/<int:id>', views.APPOINTMENT_DETAILS, name="appointment-details"),
    
    # path('member-add/', views.MEMBER_ADD, name="member-add"),
    path('appointment-add/', views.APPOINTMENT_ADD, name="appointment-add"),
    # path('room-add/', views.ROOM_ADD, name="room-add"),
    # path('diagonses-add/', views.DIAGONSES_ADD, name="diagonses-add"),
    # path('allergy-add/', views.ALLERGY_ADD, name="allergy-add"),
    path('appointment-add-diagnoses/', views.APPOINTMENT_ADD_DIAGNOSES, name="appointment-add-diagnoses"),
    path('appointment-add-allergy/', views.APPOINTMENT_ADD_ALLERGY, name="appointment-add-allergy"),
    path('appointment-add-checkup/', views.APPOINTMENT_ADD_CHECKUP, name="appointment-add-checkup"),
    path('appointment-add-surgery/', views.APPOINTMENT_ADD_SURGERY, name="appointment-add-surgery"),
    path('appointment-update-status/<int:id>/<str:status>', views.APPOINTMENT_UPDATE_STATUS, name="appointment-update-status"),
    path('surgery-update-status/<int:id>/<str:status>', views.SURGERY_UPDATE_STATUS, name="surgery-update-status"),
    
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/register', user_login.REGISTER,name="register"),
    path('accounts/create-account', user_login.CREATEACCOUNT,name="create-account"),
    path('dologin/', user_login.LOGIN,name="dologin"),
    path('logout/',user_login.LOGOUT,name='logout'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

