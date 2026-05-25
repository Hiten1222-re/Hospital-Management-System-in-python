from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

# Create your models here.

class Login(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default="admin@123")
    phone = models.CharField(max_length=20, null=True, blank=True)

    ROLE = (
        ('User', 'User'),
        ('Doctor', 'Doctor'),
    )
    role = models.CharField(max_length=10, choices=ROLE)

    STATUS = (
        ("0", "unapproved"),
        ("1", "approved")
    )
    status = models.CharField(max_length=10, choices=STATUS, default='0')

    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True, default=None)

    def pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.id_proof.url))
    pic.allow_tags = True

    def __str__(self):
        return self.name

class Contact_detail(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=30)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.department_name

class PatientProfile(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    disease = models.CharField(max_length=60)
    address = models.CharField(max_length=70)
    GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Other'),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES)
    profession = models.CharField(max_length=100)  # User's profession
    bio = models.TextField(blank=True, null=True)  # Brief introduction
    blood_type = models.CharField(max_length=10)
    userprofile_image = models.ImageField(upload_to='media/', blank=True, null=True)

    def user_image(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.userprofile_image.url))

    user_image.allow_tags = True

    def __str__(self):
        return self.user.name

class DoctorProfile(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    shift_hour = models.TimeField()
    consultation_fees = models.IntegerField()
    specialization = models.CharField(max_length=30)
    bio = models.TextField(blank=True, null=True)  # Brief introduction
    status = models.IntegerField(choices=[(0, 'Unavailable'), (1, 'Available')], default=1)
    doctorprofile_image = models.ImageField(upload_to='media/', blank=True, null=True)
    def doctor_image(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.doctorprofile_image.url))

    doctor_image.allow_tags = True

    def __str__(self):
        return self.user.name

class AvailableSlot(models.Model):
    doctor = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='available_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.name} - {self.date} {self.start_time} - {self.end_time}"

    # Optional: Ensure valid slot times

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time.')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['doctor', 'date', 'start_time', 'end_time'], name='unique_slot')
        ]


class Appointment(models.Model):
    doctor = models.ForeignKey(
        'Login',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Doctor'},
        related_name='appointment_as_doctor',  # Custom reverse relation name
        default=''
    )
    user = models.ForeignKey(
        'Login',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'User'},
        related_name='appointment_as_user',  # Custom reverse relation name
        default=''
    )
    schedule = models.ForeignKey(AvailableSlot,on_delete=models.CASCADE)
    status = models.IntegerField(choices=[(0, 'Cancelled'), (1, 'Confirmed')], default=1)
    booking_date = models.DateField(auto_now_add=True)  # Date when the appointment was booked
    consultation_notes = models.TextField(null=True, blank=True)  # Optional notes from the doctor

    def __str__(self):
        return f"Appointment of {self.user} with {self.doctor} on {self.schedule.date}"

class Treatment(models.Model):
    doctor = models.ForeignKey(
        'Login',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Doctor'},
        related_name='treatments_as_doctor',  # Custom reverse relation name
        default=''
    )
    user = models.ForeignKey(
        'Login',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'User'},
        related_name='treatments_as_user',  # Custom reverse relation name
        default=''
    )
    treatment_date = models.DateField(auto_now_add=True)  # Date of treatment
    treatment_fees = models.IntegerField()
    suggestion = models.TextField()
    diagnosis = models.TextField(null=True, blank=True)  # Optional field for doctor's diagnosis
    follow_up_required = models.BooleanField(default=False)  # Flag for follow-up treatments

    def __str__(self):
        return f"Treatment for {self.user} by {self.doctor} on {self.treatment_date}"
class Prescription(models.Model):
    doctor = models.ForeignKey(
        'Login',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Doctor'},
        related_name='prescriptions_as_doctor',  # Custom reverse relation name
        default=''
    )
    user = models.ForeignKey(
        'Login',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'User'},
        related_name='prescriptions_as_user',  # Custom reverse relation name
        default=''
    )
    medication_detail = models.CharField(max_length=80)
    dosage_instructions = models.TextField()  # Dosage and usage instructions
    issue_date = models.DateField(auto_now_add=True)  # Date when the prescription was issued
    next_visit_date = models.DateField(null=True, blank=True)  # Optional follow-up date

    def __str__(self):
        return f"Prescription for {self.user.name} by {self.doctor.name} on {self.issue_date}"
class Insurance(models.Model):
    user = models.ForeignKey(
        'Login',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'User'},
        related_name='insurances',  # Custom reverse relation name
        default=''
    )
    insurance_type = models.CharField(max_length=25)
    insurance_provider = models.CharField(max_length=25)
    coverage = models.CharField(max_length=25)
    policy_number = models.CharField(max_length=50, unique=True)  # Unique policy number
    validity_start = models.DateField()  # Policy start date
    validity_end = models.DateField()  # Policy end date
    status = models.CharField(choices=[('Active', 'Active'), ('Expired', 'Expired')], max_length=10, default='Active')
    insurance_doc = models.FileField(upload_to='id_proofs/', null=True, blank=True, default=None)

    def pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.insurance_doc.url))
    pic.allow_tags = True

    def __str__(self):
        return f"Insurance Policy {self.policy_number} ({self.status})"

from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    # Payment Modes
    PAYMENT_MODE_CHOICES = [
        ('online', 'Online Payment'),
        ('offline', 'Offline Payment'),
    ]

    # Payment Status
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(Login, on_delete=models.CASCADE)  # Reference to User
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)  # Reference to User
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)  # Reference to User
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)  # Reference to User
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)  # Payment mode
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')  # Payment status
    payment_date = models.DateTimeField(auto_now_add=True)  # Timestamp for payment
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    offline_reference = models.CharField(max_length=255, blank=True, null=True)  # Reference number for offline payment
    offline_remarks = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    address = models.TextField(blank=True, null=True)  # Optional remarks for offline payments

    def __str__(self):
        return f"{self.user.name} - {self.total_price} ({self.payment_mode})"

    class Meta:
        ordering = ['-payment_date']


class Review(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    ratings = models.IntegerField()
    comment = models.CharField(max_length=300, default="")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.user.name}"