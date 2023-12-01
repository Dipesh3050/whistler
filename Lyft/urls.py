from django.urls import path
from . import views


urlpatterns = [
    

    path('', views.home, name='home'),
    path('ride_details/<int:id>', views.ride_details, name='ride_details'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('register/', views.register, name='register'),
    path('log_out/', views.log_out, name='log_out'),
    path('request_ride/<int:id>',views.request_ride,name='request_ride'),
    path('approve_request/<int:id>/<int:request_id>/', views.approve_request, name='approve_request'),
    path('deny_request/<int:id>/<int:request_id>/', views.deny_request, name='deny_request'),
    path('approved_ride_details/<int:id>/', views.approved_ride_details, name='approved_ride_details'),
    path('add_ride/',views.add_ride,name='add_ride'),
    path('my_rides/', views.my_rides, name='my_rides'),
]