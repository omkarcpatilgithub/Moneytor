
from django.urls import path
#from .views import article_list, article_detail, raw_input, clear_duplicates, after_duplicate_remove
from . import views
urlpatterns = [
    path('rooms/', views.article_list),
    path('detail/<int:pk>', views.article_detail),
    path('allbooked',views.raw_input),
    path('clear_dup',views.clear_duplicates),
    path('after_dup_remove',views.after_duplicate_remove),
    path('hotel2', views.Hotel_detail2)


]