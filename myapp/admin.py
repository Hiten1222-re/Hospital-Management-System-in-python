from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'password', 'phone', "role", "status","id_proof")
    search_fields = ('name', 'email')

@admin.register(Contact_detail)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'timestamp')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_name']

@admin.register(PatientProfile)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'disease', 'address','gender','profession','bio','blood_type','user_image')

@admin.register(DoctorProfile)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'shift_hour', 'consultation_fees','specialization','bio', 'status','doctorprofile_image')

@admin.register(AvailableSlot)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_booked')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'schedule','status','booking_date','consultation_notes')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'treatment_date','treatment_fees','suggestion','diagnosis','follow_up_required')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'medication_detail','dosage_instructions','issue_date','next_visit_date')

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('user', 'insurance_type', 'insurance_provider','coverage','policy_number','validity_start','validity_end','status','insurance_doc')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment','treatment', 'insurance','total_price','payment_mode','payment_status','payment_date','razorpay_order_id','razorpay_payment_id','razorpay_signature','offline_reference','offline_remarks','address')

@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'ratings', 'comment', 'timestamp')