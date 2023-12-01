from django.db import models
from django.contrib.auth.models import User



class Ride(models.Model):
    
    employee_name = models.CharField(max_length=100)

    passengers = models.ManyToManyField(User, blank=True)
    total_seats = models.PositiveIntegerField(blank=True, null=True)
    available_seats = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    passenger_location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Calculate available seats based on the number of booked passengers
        print(self.__dict__, args , kwargs)
        if not self.id:
            booked_passengers_count=0
        else:
            booked_passengers_count = self.passengers.count()
        if not booked_passengers_count:
            super(Ride, self).save(*args, **kwargs)
            self.passengers.add(User.objects.get(username=self.employee_name))
        if self.total_seats is not None:
            self.available_seats = self.total_seats - booked_passengers_count
        else:
            pass
        super(Ride, self).save(*args, **kwargs)

    
    def __str__(self):
        return f"Ride ID: {self.id}, Employee: {self.employee_name}, Source: {self.passenger_location}, Destination: {self.destination}, Date/Time: {self.date}"

    def ride_requests(self):
        return self.riderequest_set.all()

class RideRequest(models.Model):
    req_id = models.AutoField(primary_key=True)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(User)
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
        ('Requested', 'Requested'),
    ]
    ride_status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='Requested')

    def approve(self):
        if self.ride_status == 'Requested':
            self.ride.passengers.add(self.passengers.first())

            self.ride.save()
            print("Ride approved successfully.")
            self.ride_status = 'Approved'
            self.save()

    def deny(self):
        if self.ride_status == 'Requested':
            self.ride_status = 'Denied'
            self.save()
    def __str__(self):
        first_passenger = self.passengers.first()
        requester_username = first_passenger.username if first_passenger else "Unknown"
        return f"{requester_username}'s request for {len(self.passengers.all())} passengers on {self.ride.employee_name}"
