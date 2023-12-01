from .forms import AuthenticationForm
from .forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Ride,RideRequest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import  get_object_or_404
from datetime import datetime
from django.db import transaction
from .forms import RideForm
from django.utils import timezone
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email.endswith('@q3tech.com'):
                user = form.save()
                login(request, user)
                return redirect('sign_in')
            else:
                form.add_error('email', 'Registration allowed only for @q3tech.com addresses.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
@login_required
def log_out(request):
    logout(request)
    return redirect('sign_in')

# Home view
@login_required
def home(request):
    user = request.user
    #get rides which user has already requested 
    requested_rides=RideRequest.objects.filter(ride_status='Requested' , passengers=user)
    # Fetch rides where the user is not the employee or user is not in passenger and have available seats
    available_rides = Ride.objects.exclude(
        Q(employee_name=request.user) | Q(passengers=user)  | Q(riderequest__in=requested_rides)
    ).filter(available_seats__gt=0)

    # Fetch rides where the user is the employee
    booked_rides = RideRequest.objects.filter(ride__employee_name=user)
    context = {
        'user': user,
        'requested_rides' : requested_rides,
        'available_rides': available_rides,
        'booked_rides': booked_rides,
    }
    
    return render(request, 'home.html', context)




# Request ride and view details
@login_required
def ride_details(request,id):
    # Retrieve the Ride object with the given ride_id
    ride = Ride.objects.get(pk=id)
    return render(request, 'ride_details.html', {'ride': ride})


@login_required
def request_ride(request, id):
    ride = Ride.objects.get(pk=id)
    message = None
    existing_request = RideRequest.objects.filter(ride=ride, passengers=request.user).first()
    if request.method == 'POST':
        if ride.available_seats > 0:
            if not existing_request:
                ride_request = RideRequest.objects.create(ride=ride, ride_status='Requested')
                ride_request.passengers.add(request.user)
            
        else:
            message = "Not enough available seats."
            messages.error(request, message)
    
    return render(request, 'request_ride.html', {'ride': ride, 'user': request.user, 'message': message})

@login_required
def approve_request(request, id, request_id):
    ride_request = get_object_or_404(RideRequest, pk=request_id)
    if request.method == 'POST':
        # Handle the POST request for approval
        action = request.POST.get('action')
        if action == 'approve':
             with transaction.atomic():
                # Decrement available seats
                ride = ride_request.ride
                ride.available_seats -= 1
                ride.save()
                
                # Update ride request status to 'Approved'
                ride_request.ride_status = 'Approved'
                ride_request.save()
                
        return redirect('approved_ride_details', id=id)

    return render(request, 'approve_or_deny.html', {'ride_request': ride_request})  

@login_required
def deny_request(request, id, request_id):
    ride_request = get_object_or_404(RideRequest, pk=request_id)
    if request.method == 'POST':
        # Handle the POST request for denial
        action = request.POST.get('action')
        if action == 'deny':
            ride_request.delete()
            return redirect('home')

    return render(request, 'approve_or_deny.html', {'ride_request': ride_request})  

@login_required
def approved_ride_details(request, id):
    ride = Ride.objects.get(pk=id)
    
    # Fetch the user who made the request
    ride_request = ride.ride_requests().first()
    requester = ride_request.passengers.first() if ride_request else None

    # Update ride status to 'Approved'
    ride_request.approve()

    return render(request, 'approved_ride_details.html', {'ride': ride, 'requester': requester})







@login_required
def add_ride(request):
    if request.method == 'POST':
        ride = Ride(**{
                        "employee_name":request.user.username,
                        "total_seats":int(request.POST.get('available_seats')) +1,
                        "available_seats":request.POST.get('available_seats'),
                        "date":timezone.now(),
                        'passenger_location':request.POST.get('passenger_location'), 
                        'destination': request.POST.get('destination'),
                            })
        ride.save()
        return redirect('home')
    else:
        form = RideForm()
    return render(request, 'add_ride.html', {'form': form})

@login_required
def my_rides(request):
    # Get rides created by the signed-in user
    created_rides = Ride.objects.filter(Q(employee_name=request.user) | Q(riderequest__passengers=request.user, riderequest__ride_status='Approved'))

    return render(request, 'my_rides.html', {'created_rides': created_rides})


