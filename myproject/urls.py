"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views  # Import your views from the app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('login1', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('add_patient_detail', views.add_patient_detail, name='add_patient_detail'),
    path('showuser', views.showuser, name='showuser'),
    path('editpatientprofile', views.editpatientprofile, name='editpatientprofile'),
    path('update', views.update, name='update'),
    path('add_doctor_detail', views.add_doctor_detail, name='add_doctor_detail'),
    path('showdoctors', views.showdoctors, name='showdoctors'),
    path('editdoctor', views.editdoctor, name='editdoctor'),
    path('updatedoctor', views.updatedoctor, name='updatedoctor'),
    # path('alldoctors', views.alldoctors, name='alldoctors'),
    path('add_insurance', views.add_insurance, name='add_insurance'),
    path('add_time_slot', views.add_time_slot, name='add_time_slot'),
    path('book-slot/', views.book_slot, name='book_slot'),
    path('appoint', views.appoint, name='appoint'),
    path('add_appointment', views.add_appointment, name='add_appointment'),
    path('get-schedules/', views.get_doctor_schedules, name='get_schedules'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('doc_detail/<int:doctor_id>', views.doc_detail, name='doc_detail'),
    path('doctor/user/<int:user_id>', views.doctor_user_details, name='doctor_user_details'),
    path('doctor/user/<int:user_id>/add_treatment/', views.doctor_add_treatment, name='doctor_add_treatment'),
    path('doctor/user/<int:user_id>/add_prescription/', views.doctor_add_prescription, name='doctor_add_prescription'),
    path('user_appointment', views.user_appointment, name='user_appointment'),
    path('user_booking/user/<int:id>', views.user_booking, name='user_booking'),
    path('create_order/<int:appoint_id>', views.create_order, name='create_order'),
    path('offline-payment/<int:appoint_id>', views.offline_payment, name='offline_payment'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('storefeedback', views.storefeedback, name='storefeedback'),
    path('find_doctors', views.find_doctors, name='find_doctors'),
    path('forget_pass', views.forget_pass, name='forget'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('reset_pass', views.reset_password, name='reset_pass'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)