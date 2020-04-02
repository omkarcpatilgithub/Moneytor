
from django.urls import path
#from .views import article_list, article_detail, raw_input, clear_duplicates, after_duplicate_remove
from . import views
urlpatterns = [
    #path('rooms/', views.article_list),
    #path('detail/<int:pk>', views.article_detail),
    #path('clear_dup',views.clear_duplicates),
    # path('after_dup_remove',views.after_duplicate_remove),

    path('hotel', views.Hotel_detail),
    path('allBooked', views.raw_input),
    path('roomsAvailable', views.check_availability),
    path('multiBook', views.multi_booking),
    path('initialSetup', views.initial_setup),
    path('cancelBooking', views.cancel_booking),
]