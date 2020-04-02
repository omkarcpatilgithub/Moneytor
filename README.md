# Moneytor
Hotel management for Moneytor hotel
a REST API is created with Django framework,

--model is creted for following fields ['room','book_date','booked','name'] (models.py)

--model is serialized with ModelSerializer (in serializers.py)


--follwing urls implemented: (urls.py)

  localhost <ip>  /initialSetup :	Please run this Initial setup before going further
	
  localhost <ip>  /hotel	:	for single room booking
  
  localhost <ip>  /allBooked :	To see all the booked rooms
  
  localhost <ip>  /roomsAvailable: Available rooms for a time period
  
  localhost <ip>  /multiBook : 	Booking for multiple days

  localhost <ip>  /cancelBooking :If you want to Cancel a single booking
  
  
  
  
  according functions are written in views.py
    path('hotel', views.Hotel_detail),
    path('allBooked', views.raw_input),
    path('roomsAvailable', views.check_availability),
    path('multiBook', views.multi_booking),
    path('initialSetup', views.initial_setup),
    path('cancelBooking', views.cancel_booking),

#######################################################################
form are added to take input from user
Gui is also added for simplicity


#######################################################################
To implement
=> download or clone this repository in your system.
=> goto to the folder
=> open terminal
=> python manage.py makemigrations
=> python manage.py migrate
=> python manage.py runserver

Note: please first call /initialSetup then all others
