from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
# Create your views here.
def checksession(request):
    uid = request.session.get('log_id')

    if not uid:
        return None

    try:
        userdata = Login.objects.get(id=uid)
        is_doctor = userdata.role == "Doctor"

        if is_doctor:
            try:
                profile = DoctorProfile.objects.get(user=userdata)
            except DoctorProfile.DoesNotExist:
                profile = None
        else:
            try:
                profile = PatientProfile.objects.get(user=userdata)
            except PatientProfile.DoesNotExist:
                profile = None

        context = {
            'userdata': userdata,
            'is_doctor': is_doctor,
            'profile': profile,

        }
        return context
    except Login.DoesNotExist:
        return None


def index(request):
    context = checksession(request)
    if context is None:
        context = {}  # Initialize context as an empty dictionary if checksession returns None

    alldoctor = DoctorProfile.objects.all()
    alldepartment = Department.objects.all()
    context['doctordetails'] = alldoctor
    context['alldepartments'] = alldepartment
    return render(request,'home-medical-clinic.html',context)

def about(request):
    context = checksession(request)
    if context is None:
        context = {}  # Initialize context as an empty dictionary if checksession returns None

    alldoctor = DoctorProfile.objects.all()
    context['doctordetails'] = alldoctor
    return render(request,'about.html',context)

def contact(request):
    context = checksession(request)
    # if request.method == "POST":
    #     Name = request.POST.get('name')
    #     Email = request.POST.get('email')
    #     Subject = request.POST.get('subject')
    #     Message = request.POST.get('message')

    #     if Contact_detail.objects.filter(email=Email).exists():
    #         messages.error(request, 'You have already filled out contact details.')
    #         return redirect('contact')  # Assuming you have a URL pattern named 'contact1'
    #     else:
    #         contactdata = Contact_detail(name=Name, email=Email, subject=Subject, message=Message)
    #         contactdata.save()
    #         messages.success(request, 'Your contact details have been saved.')
    #         return redirect('index')  # Ensure 'index' is the name of your URL pattern or view function

    return render(request,'contact.html',context)


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name1')
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        phone = request.POST.get('phone1')
        role = request.POST.get('usertype')

        # Create a new Login object
        new_user = Login(name=name, email=email, password=password, phone=phone, role=role, status=1)

        # Check if id_proof1 exists in request.FILES
        if 'id_proof1' in request.FILES:
            id_proof = request.FILES['id_proof1']
            new_user.id_proof = id_proof

        # Save user based on their role
        if role == 'Doctor':
            messages.info(request, 'Registration done successfully. Please wait for your profile approval. It will take around 2-3 days.')
        else:
            messages.success(request, 'Data inserted successfully. You can login now.')

        new_user.save()

        # Redirect to a success page
        return redirect('index')

    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        Email1 = request.POST['email2']
        Password1 = request.POST['password2']
        try:
            user = Login.objects.get(email=Email1, password=Password1)

        except Login.DoesNotExist:
            user = None

        if user is not None:
            if user.role == "Doctor" and user.status == "0":
                print(user.role)
                print(user.status)
                messages.error(request, 'Your Profile is Under Approval Process. This may take upto 3 working days.')
            else:
                request.session['log_id'] = user.id
                request.session.save()
                messages.success(request, 'Login successful...')
                return redirect('/')
        else:
            messages.error(request, 'Invalid Email Id and Password. Please try again.')
            return redirect('/login1')

    return render(request,'login.html')

def logout(request):
    try:
        del request.session['log_id']
        messages.success(request,'your logout successfully.')
    except:
        pass
    return render(request,'home-medical-clinic.html')

def add_doctor_detail(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        department = request.POST.get('department')
        shift_hour = request.POST.get('shift_hour')
        consultation_fees = request.POST.get('consultation_fees')
        specialization = request.POST.get('specialization')
        bio = request.POST.get('bio')
        status = request.POST.get('status')
        Profile_image = request.FILES.get('doctorprofile_image')

        depart = Department.objects.get(id=department)

        userdata = DoctorProfile(user=Login(id=uid), department=depart, shift_hour=shift_hour, consultation_fees=consultation_fees,
                                  doctorprofile_image=Profile_image, specialization=specialization,
                                  status=status, bio=bio)
        userdata.save()
        messages.success(request, 'your profile data is saved.')
        return redirect(index)

    department = Department.objects.all()

    context.update({'departments': department})
    return render(request,'add_doctor.html', context)

def showdoctors(request):
    context = checksession(request)
    uid = request.session['log_id']
    alldoctordetails = DoctorProfile.objects.get(user=Login(id=uid))
    context.update({
        'alldetail': alldoctordetails,
    })
    return render(request,'showdoctor.html',context)

def editdoctor(request):
    context = checksession(request)
    uid = request.session['log_id']
    edituser = DoctorProfile.objects.get(user=Login(id=uid))
    department = Department.objects.all()

    context.update({
        'data': edituser,
        'departments': department,
    })
    return render(request,'editdoctorprofile.html',context)

def updatedoctor(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        department = request.POST.get('department')
        shift_hour = request.POST.get('shift_hour')
        consultation_fees = request.POST.get('consultation_fees')
        specialization = request.POST.get('specialization')
        bio = request.POST.get('bio')
        status = request.POST.get('status')
        object = DoctorProfile.objects.get(user=uid)
        object.department=Department(id=department)
        object.shift_hour=shift_hour
        object.consultation_fees=consultation_fees
        object.specialization=specialization
        object.bio=bio
        object.status=status

        if 'doctorprofile_image' in request.FILES:
            file = request.FILES['doctorprofile_image']
            object.doctorprofile_image = file
        object.save()
        messages.success(request, 'your profile has been completed..')

        return redirect('/showdoctors')

    return render(request,'edituserdetail.html',context)

def add_patient_detail(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        disease = request.POST.get('disease')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        Profession = request.POST.get('profession')
        bio = request.POST.get('bio')
        blood_type = request.POST.get('blood_type')
        Profile_image = request.FILES.get('userprofile_image')

        userdata = PatientProfile(user=Login(id=uid), disease=disease,address=address, gender=gender,userprofile_image=Profile_image, blood_type=blood_type,
                               profession=Profession, bio=bio)
        userdata.save()
        messages.success(request, 'your profile data is saved.')
        return redirect(index)
    return render(request,'addpatient.html', context)

def showuser(request):
    context = checksession(request)
    uid = request.session['log_id']
    alluserdetails = PatientProfile.objects.get(user=Login(id=uid))
    context.update({
        'alldetail': alluserdetails,
    })
    return render(request,'showpatient.html',context)

def editpatientprofile(request):
    context = checksession(request)
    uid = request.session['log_id']
    edituser = PatientProfile.objects.get(user=Login(id=uid))
    context.update({
        'data': edituser,
    })
    return render(request,'editprofile.html',context)

def update(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        disease = request.POST.get('disease')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        Profession = request.POST.get('profession')
        bio = request.POST.get('bio')
        blood_type = request.POST.get('blood_type')
        
        object = PatientProfile.objects.get(user=uid)
        object.disease=disease
        object.address=address
        object.gender=gender
        object.bio=bio
        object.Profession=Profession
        object.blood_type=blood_type
        object.bio=bio
        

        if 'userprofile_image' in request.FILES:
            file = request.FILES['userprofile_image']
            object.userprofile_image = file
        object.save()
        messages.success(request, 'your profile has been completed..')

        return redirect('/showuser')
    return render(request,'edituserdetail.html',context)

# def alldoctors(request):
#     context = checksession(request)
#     if context is None:
#         context = {}  # Initialize context as an empty dictionary if checksession returns None

#     alldoctor = DoctorProfile.objects.all()
#     context['doctordetails'] = alldoctor
#     return render(request,'team.html', context)


from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from datetime import datetime



def add_time_slot(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        dates = request.POST.getlist('dates[]')
        start_times = request.POST.getlist('start_times[]')
        end_times = request.POST.getlist('end_times[]')

        for date, start_time, end_time in zip(dates, start_times, end_times):
            start_dt = datetime.strptime(f"{date} {start_time}", '%Y-%m-%d %H:%M')
            end_dt = datetime.strptime(f"{date} {end_time}", '%Y-%m-%d %H:%M')

            # Ensure that end time is after start time
            if end_dt <= start_dt:
                raise ValidationError("End time must be after start time.")

            # Check if there are existing slots that overlap
            existing_slots = AvailableSlot.objects.filter(
                doctor=Login(id=uid),
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if existing_slots.exists():
                raise ValidationError("Time slot overlaps with an existing slot.")

            # Optional: Check if there is a gap between the slots for the same date
            # You can retrieve the existing slots on the date and compare their times
            previous_slots = AvailableSlot.objects.filter(
                doctor=Login(id=uid),
                date=date
            ).order_by('start_time')


            # If all validations pass, save the slot
            AvailableSlot.objects.create(
                doctor=Login(id=uid),
                date=date,
                start_time=start_time,
                end_time=end_time,
                is_booked=False
            )

        messages.success(request,' your slot added successfully.')
        return redirect('/')  # Redirect to a success page or another view

    return render(request, 'addtimeslot.html', context)


from django.shortcuts import render, get_object_or_404
from .models import DoctorProfile, AvailableSlot


def doc_detail(request, doctor_id):
    context = checksession(request)
    alldoc = DoctorProfile.objects.get(id=doctor_id)
    available_slots = AvailableSlot.objects.filter(doctor=alldoc.user).order_by('date', 'start_time')
    context.update({"alldetail": alldoc, 'available_slots': available_slots})
    return render(request, 'single_doctor.html', context)

def book_slot(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        slot = get_object_or_404(AvailableSlot, id=slot_id)

        if not slot.is_booked:
            slot.is_booked = True
            slot.save()

            # Create a new Appointment
            appointment = Appointment(
                doctor=slot.doctor,  # Assuming 'doctor' is a foreign key to the doctor
                user=Login(id=uid),  # Assuming the logged-in user is the one booking the slot
                schedule=slot,  # Linking the appointment to the selected slot
                status=1  # Default status to "Confirmed"
            )
            appointment.save()

            messages.success(request, 'Slot booked successfully and appointment registered!')
        else:
            messages.error(request, 'This slot has already been booked.')

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def appoint(request):
    context = checksession(request)
    uid = request.session['log_id']
    appointments = Appointment.objects.filter(doctor=Login(id=uid), status=1)  # Get all appointments for the doctor
    context.update({'appointmentdetail': appointments})
    return render(request, 'showappointment.html', context)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def cancel_appointment(request, appointment_id):
    # Ensure only POST requests can cancel appointments
    if request.method == "POST":
        # Get the appointment object
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Mark the associated time slot as available
        schedule = appointment.schedule
        if schedule:
            schedule.is_booked = False  # Mark the time slot as available
            schedule.save()  # Save the changes

        # Update the appointment status to 'Cancelled'
        appointment.status = 0
        appointment.save()  # Save the changes

        messages.success(request, "Appointment cancelled successfully.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('appoint')  # Redirect back to the appointments page

def doctor_user_details(request, user_id):
    context = checksession(request)
    try:
        # Get the Login instance using the user_id
        login_instance = Login.objects.get(id=user_id)

        # Get the PatientProfile associated with the Login instance
        user = PatientProfile.objects.get(user=login_instance)  # Assuming PatientProfile has a ForeignKey to Login

        # Get the first appointment and insurance details for the user
        appointment = Appointment.objects.filter(user=login_instance).first()
        insurance = Insurance.objects.filter(user=login_instance).first()

        # Get all treatments and prescriptions for the user
        treatments = Treatment.objects.filter(user=login_instance)
        prescriptions = Prescription.objects.filter(user=login_instance)

        # Pass data to template
        context.update({
            'user': login_instance,
            'appointment': appointment,
            'insurance': insurance,
            'treatments': treatments,
            'prescriptions': prescriptions,
        })

        return render(request, 'appointmentdetail.html', context)

    except Login.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found'})
    except PatientProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Patient profile not found'})


def add_insurance(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        insurance_type = request.POST.get('insurance_type')
        insurance_provider = request.POST.get('insurance_provider')
        coverage = request.POST.get('coverage')
        policy_number = request.POST.get('policy_number')
        validity_start = request.POST.get('validity_start')
        validity_end = request.POST.get('validity_end')
        status = request.POST.get('status')
        insurance_file = request.FILES.get('insurance_file')

        userdata = Insurance(user=Login(id=uid), insurance_type=insurance_type, insurance_provider=insurance_provider, coverage=coverage,
                                  policy_number=policy_number, validity_start=validity_start,validity_end=validity_end,
                                  status=status, insurance_doc=insurance_file)
        userdata.save()
        messages.success(request, 'your insurance data is saved.')
        return redirect(index)
    return render(request,'addinsurance.html',context)


def doctor_add_treatment(request, user_id):
    uid = request.session.get('log_id')
    if request.method == 'POST':
        # Get the logged-in doctor's Login instance
        doctor = Login.objects.get(id=uid)

        # Get the user (PatientProfile)
        user = Login.objects.get(id=user_id)

        # Get data from the form
        treatment_fees = request.POST['treatment_fees']
        suggestion = request.POST['suggestion']
        diagnosis = request.POST.get('diagnosis', '')
        follow_up_required = bool(request.POST.get('follow_up_required', False))

        # Create Treatment entry
        Treatment.objects.create(
            doctor=doctor,
            user=user,
            treatment_fees=treatment_fees,
            suggestion=suggestion,
            diagnosis=diagnosis,
            follow_up_required=follow_up_required
        )

        messages.success(request, 'Treatment details added successfully.')
        return redirect('doctor_user_details', user_id=user_id)

    # Optionally, handle the case where the request method is not POST
    messages.error(request, 'Invalid request method.')
    return redirect('doctor_user_details', user_id=user_id)

from django.http import JsonResponse
from .models import AvailableSlot

def get_doctor_schedules(request):
    doctor_id = request.GET.get('doctor_id')

    slots = AvailableSlot.objects.filter(
        doctor_id=doctor_id,
        is_booked=False
    )

    data = []
    for slot in slots:
        data.append({
            'id': slot.id,
            'label': f"{slot.date} ({slot.start_time} - {slot.end_time})"
        })

    return JsonResponse(data, safe=False)

from django.db import transaction

def add_appointment(request):
    doctors = DoctorProfile.objects.select_related('user','department')  # fetch all doctors
    uid = request.session['log_id']
    user = Login.objects.get(id=uid)
    
    if request.method == "POST":
        doctor_id = request.POST.get('doctor')
        schedule_id = request.POST.get('schedule')

        if not doctor_id or not schedule_id:
            messages.error(request, "Please fill all fields!")
            return redirect('add_appointment')

        # Fetch doctor & schedule objects
        doctor1=Login.objects.get(id=doctor_id)
        try:
            with transaction.atomic():
                schedule = AvailableSlot.objects.select_for_update().get(id=schedule_id)

                if schedule.is_booked:
                    messages.error(request, "Slot already booked!")
                    return redirect('add_appointment')

                schedule.is_booked = True
                schedule.save()
        # Save appointment to DB
                Appointment.objects.create(
                    user=user,
                    doctor=doctor1,
                    schedule=schedule,
                    status=1  # assuming 1 = confirmed
                )
        except Exception as e:
            messages.error(request, "Booking failed. Try again.")
            return redirect('add_appointment')

        messages.success(request, "Appointment booked successfully!")
        return redirect('user_appointment')  # change to your redirect route

    return render(request, 'add_appointment.html', {
        'doctors': doctors,
        'user':user
    })


def doctor_add_prescription(request, user_id):
    uid = request.session.get('log_id')
    if request.method == 'POST':
        # Get the logged-in doctor's Login instance
        doctor = Login.objects.get(id=uid)

        # Get the user's PatientProfile and then their Login instance
        user = Login.objects.get(id=user_id)

        # Get data from the form
        medication_detail = request.POST['medication_detail']
        dosage_instructions = request.POST['dosage_instructions']
        next_visit_date = request.POST.get('next_visit_date', None)

        # Create Prescription entry
        Prescription.objects.create(
            doctor=doctor,
            user=user,
            medication_detail=medication_detail,
            dosage_instructions=dosage_instructions,
            next_visit_date=next_visit_date
        )

        messages.success(request, 'Prescription details added successfully.')
        return redirect('doctor_user_details', user_id=user_id)

    # Optionally, handle the case where the request method is not POST
    messages.error(request, 'Invalid request method.')
    return redirect('doctor_user_details', user_id=user_id)




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Appointment, Payment, Treatment
import razorpay

import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment, Treatment, Payment


def user_appointment(request):
    context = checksession(request)
    uid = request.session['log_id']
    # Fetch and display the user's appointments
    appointments = Appointment.objects.filter(user__id=uid)
    context.update({'appointments': appointments})

    # Render the appointments page
    return render(request, 'user_booking_appointment.html', context)





def user_booking(request,id):
    context = checksession(request)
    try:
        # Get the appointment and login details form the appoinment
        appointment = Appointment.objects.get(id=id)
        login_instance = Login.objects.get(id=appointment.user_id)
    

        # Get Insurance details related to login instance
        insurance = Insurance.objects.filter(user=login_instance).first()


        # Get the PatientProfile associated with the Login instance
        user = PatientProfile.objects.get(user=login_instance)  # Assuming PatientProfile has a ForeignKey to Login


        # Get all treatments and prescriptions for the user
        treatments = Treatment.objects.filter(user=login_instance)
        prescriptions = Prescription.objects.filter(user=login_instance)

        #confirming payment 
        has_pay=Payment.objects.filter(appointment_id=id).exists()

        # Pass data to template
        context.update({
            'user': login_instance,
            'appointment': appointment,
            'insurance': insurance,
            'treatments': treatments,
            'prescriptions': prescriptions,
            'has_pay':has_pay,
        })

        return render(request, 'user_appointment_detail.html', context)

    except Login.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found'})
    except PatientProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Patient profile not found'})



def create_order(request, appoint_id):
    context = checksession(request)
    uid = request.session['log_id']
    try:
        # Fetch the logged-in user and related details
        login_instance = Login.objects.get(id=uid)
        user = PatientProfile.objects.get(user=login_instance)

        # Fetch appointment, insurance, and treatments
        appointment = Appointment.objects.filter(id=appoint_id).first()
        insurance = Insurance.objects.filter(user=login_instance).first()
        treatments = Treatment.objects.filter(user=login_instance)

        # Calculate the total treatment fees
        total_price = treatments.aggregate(total_fees=models.Sum('treatment_fees'))['total_fees'] or 0

        # Ensure all required data is available
        if not appointment or not insurance or not treatments.exists():
            messages.error(request, "Incomplete user data. Please check appointment, treatment, and insurance details.")
            return redirect('user_appointment')

        # Check if a payment has already been made for this appointment
        existing_payment = Payment.objects.filter(
            appointment=appointment,
        ).exists()

        if existing_payment:
            messages.error(request, "You have already paid for this appointment.")
            return redirect('user_appointment')

        # Razorpay payment logic (if POST request)
        if request.method == 'POST':
            razorpay_client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f'))

            razorpay_order = razorpay_client.order.create({
                "amount": int(total_price * 100),  # Amount in paisa
                "currency": "INR",
                "payment_capture": '1',
                "receipt": f"order_{uid}",
            })

            # Save payment details to the Payment model
            Payment.objects.create(
                user=login_instance,
                appointment=appointment,
                treatment=treatments.first(),
                insurance=insurance,
                total_price=total_price,
                payment_mode='online',
                payment_status='Pending',
                razorpay_order_id=razorpay_order['id'],
            )

            context.update({
                'razorpay_payment': {
                    'amount': total_price,
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_key_id': 'rzp_test_VQhEfe2NCXbbwI',
                    'currency': 'INR',
                },
                'user': user,
                'appointment': appointment,
                'insurance': insurance,
                'treatments': treatments,
            })

            return render(request, 'payment.html', context)

        # Handle GET request (generic appointment page)
        context.update({
            'user': user,
            'appointment': appointment,
            'insurance': insurance,
            'treatments': treatments,
        })
        return render(request, 'user_appointment_detail.html', context)

    except Login.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('user_appointment')
    except PatientProfile.DoesNotExist:
        messages.error(request, "Patient profile not found.")
        return redirect('user_appointment')
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('user_appointment')


from django.core.mail import send_mail


def payment_success(request):
    context = checksession(request)
    if request.method == 'POST':
        print("POST Data: ", request.POST)

        # Extract the Razorpay response details from the POST request
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')

        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            # Handle missing information
            return render(request, 'failure.html', {'status': 'Error: Missing payment details'})

        # Verify the payment signature with Razorpay
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        }

        try:
            client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f','rzp_test_SL4IDEG4m5muxw'))
            client.utility.verify_payment_signature(params_dict)

            # Fetch the Payment object and update its status
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.payment_status = 'Completed'
            payment.save()
            print("Payment Updated in DB: ", payment)
            # Send success email
            subject = 'Payment Successful'
            message = f"Dear {payment.user.name},\n\n" \
                      f"Thank you for  the {payment.treatment.treatment_fees} payment. Your payment was successful! \n\n" \
                      f"Best regards,\nYour Team"
            sender_email = 'dpoza8125@gmail.com'
            recipient_email = [payment.user.email]

            send_mail(subject, message, sender_email, recipient_email, fail_silently=False)
            context.update({'status': True})
            # Payment was successful
            return render(request, 'success.html', context)

        except razorpay.errors.SignatureVerificationError:
            # Handle invalid signature
            return render(request, 'failure.html', {'status': 'Signature verification failed.'})

        except Payment.DoesNotExist:
            # Handle invalid order
            return render(request, 'failure.html', {'status': 'Order does not exist.'})

        except Exception as e:
            # Handle any other errors
            return render(request, 'failure.html', {'status': f"Error: {str(e)}"})

    else:
        # Handle GET requests or other invalid methods
        messages.error(request, "Invalid request method. Please try again.")
        print("Invalid request method: ", request.method)
        return redirect('user_appointment')

from django.shortcuts import render
from django.http import HttpResponse


def offline_payment(request, appoint_id):
    uid = request.session['log_id']

    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appoint_id)
        address = request.POST.get("address")
        reference = request.POST.get("reference")
        remark = request.POST.get("remark")

        treatment = Treatment.objects.filter(user=Login(id=uid)).first()  # Get one treatment
        insurance = Insurance.objects.filter(user=Login(id=uid)).first()
        total_price = treatment.treatment_fees if treatment else 0  # Use single treatment's fees

        Payment.objects.create(
            user=Login(id=uid),
            appointment=appointment,
            treatment=treatment,
            insurance=insurance,
            total_price=total_price,
            address=address,
            offline_reference=reference,
            offline_remarks=remark,
            payment_mode='offline',  # Set payment mode
            payment_status='Pending',  # Set payment status
        )

        return HttpResponse("Offline payment details submitted successfully.")

    return HttpResponse("Invalid request method.")

def storefeedback(request):
    context = checksession(request)
    uid = request.session.get('log_id')  # Ensure user is logged in and has a session
    user = Login.objects.get(id=uid)


    if request.method == 'POST':
        order_id = request.POST.get('orders')
        ratings = request.POST.get('ratings')
        feedback_message = request.POST.get('feedback_message')

        if Review.objects.filter(user=order_id).exists():
            messages.error(request, 'you have already filled feedback.')
            return redirect('index')
        else:
        # Assuming 'product' is a ForeignKey in the Feedback model pointing to Product
            review = Review.objects.create(
                user=Login(id=uid),
                ratings=ratings,
                comment=feedback_message,
            )

        messages.success(request, "Review is submitted")
        return redirect(index)
    return render(request, 'feedback.html', context)


def find_doctors(request):
    context = checksession(request)
    if context is None:
        context = {}

    departments = Department.objects.all()
    # Get selected property type if any
    category_type = request.GET.get('category_type')
    doctors = DoctorProfile.objects.all()
    if category_type:
        doctors = doctors.filter(department__id=category_type)

    context['doctordetails'] = doctors
    context['alldepartments'] = departments
    return render(request, 'search_doctor.html', context)

from django.core.mail import send_mail
from django.conf import settings
import random


def forget_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email2')
 
        # Check if the email exists in your user table
        # Adjust the field/model name to match your project
        try:
            user = Login.objects.get(email=email)   # adapt to your model
        except User.DoesNotExist:
            # Show a vague message so we don't leak which emails are registered
            messages.error(
                request,
                'If that email is registered you will receive a reset link shortly.'
            )
            return redirect('forget')

        otp=random.randint(1000,9999)
        
        request.session['email']=email
        request.session['otp']={'otp1':otp,'expire':datetime.now().isoformat()}

 
        # Send email
        try:
            send_mail(
                subject='Password Reset Request – Mediax',
                message=(
                    f'Hello {user.name},\n\n'
                    f'You requested a password reset. Use otp below to set a new password:\n\n'
                    f'{otp}\n\n'
                    f'This otp is valid for 10 minutes. If you did not request this, please ignore this email.\n\n'
                    f'– Mediax Team'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(
                request,
                'Otp has been sent to your email.'
            )
        except Exception:
            messages.error(
                request,
                'Failed to send email. Please try again later.'
            )
 
        return redirect('verify_otp')
 
    return render(request, 'forget_pass.html')

from datetime import datetime, timedelta

def verify_otp(request):
    email = request.session.get('email')
    otp=request.session.get('otp')

    if not email:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('forget')
 
    if request.method == 'POST':
        entered_otp = ''.join(request.POST.getlist('otp[]'))
        entered_otp = int(entered_otp)

 
        if datetime.now() > datetime.fromisoformat(otp['expire']) + timedelta(minutes=10):
            messages.error(request, 'OTP has expired. Please request a new one.')
            return redirect('forget')
 
        if entered_otp != otp['otp1']:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_otp.html', {'email': email})
        
        del request.session['otp']
        request.session['otp_verified'] = True
        return redirect('reset_pass')
 
    return render(request, 'verify_otp.html', {'email': email})

def reset_password(request):
    email = request.session.get('email')
    verified = request.session.get('otp_verified', False)
 
    if not email or not verified:
        messages.error(request, 'Unauthorized. Please start the reset process again.')
        return redirect('forgot_password')
 
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
 
        try:
            user = Login.objects.get(email=email)
            user.password=new_password
            user.save()
 
            # Clean up session
            del request.session['email']
            del request.session['otp_verified']
            
 
            messages.success(request, 'Password reset successful! Please log in.')
            return redirect('login')
 
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('forgot_password')
 
    return render(request, 'reset_password.html')
