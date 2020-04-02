from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer, RoomSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .forms import HotelForm, CheckAvailabilityForm, MultiBookingForm, CancelBookingForm
from datetime import date, timedelta,datetime
from . import sqls
import django

# Create your views here.

def clear_duplicates():     # as this was a trial to get called by other function
    ## deletes all duplicate entries wrt room and date,  executes raw sql query
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM api_basic_article WHERE ID NOT IN ( SELECT MAX(ID) AS MaxRecordID FROM api_basic_article GROUP BY room, book_date)")

        row = cursor.fetchone()
        print('clear duplicates done')

    return row
@api_view(['GET'])      # mentioning what all requests this function ( attached to a url) is going to have
def after_duplicate_remove(request):
    ## removes duplicates and shows whole list
    clear_duplicates()
    # article_list(request)
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    print(' printing article list after clearing duplicates')
    return Response(serializer.data)


    #return Response('lets see what happens next',status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])       # mentioning what all requests this function ( attached to a url) is going to have
def article_list(request):
    if request.method == 'GET':
        clear_duplicates()
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        # #################################################
        # query = 'Select * from api_basic_article where booked = 1'
        # a = []
        # queryset = Article.objects.raw(query)
        # # for p in Article.objects.raw(query):
        # #     print(p.room, p.booked)
        # #     a.append(p.room)        #a.append(p.room, p.booked)  # this is giving error
        #
        # # return JsonResponse(queryset, safe=False)
        # ###################################################

        # return JsonResponse(serializer.data, safe=False)  # this for JsonResponse only
        print(' printing article list done')
        return Response(serializer.data)



    elif request.method == 'POST':
        # data = JSONParser().parse(request)  ## THIS IS FOR JSON
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])   # mentioning what all requests this function ( attached to a url) is going to have
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExistt:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])   # mentioning what all requests this function ( attached to a url) is going to have
def Hotel_detail(request):
    if request.method == 'GET':
        print('got the get request')
        form = HotelForm()      # creating instance of HotelForm which we made in forms.py

        title = 'Welcome to Moneytor inn'
        short_decription = 'Book room for a Single day, you can always check current bookings at "/allBooked"'
        args = {'form': form, 'Title': title, 'short_description': short_decription}
        return render(request, 'forms.html', args)        # sending form object to fit in forms.html ( wherever it is mentinoed) to render the paged

    if request.method == 'POST':
        print('got the post request')
        form = HotelForm(request.POST)
        if form.is_valid():                 # checking whether form that we got from post method is valid or not
            room = form.cleaned_data['room']        # this is what you should do to store the data from forms
            date = form.cleaned_data['book_date']
            name = form.cleaned_data['name']
            print('VALID', room,date,name)
            form.save()                             # save it on database ( models)
            return Response('changes are made check at /allbooked')


@api_view(['GET'])  ## mentioning what all requests this function ( attached to a url) is going to have
def raw_input(request):
    ## TODO
    ## convert raw query set (list) into django queryset,
    # which can be converted into json formate to response

    if request.method == 'GET':
        # objectQuerySet = Article.objects.filter(booked=1)
        # print(type(objectQuerySet))
        # serializer = ArticleSerializer(objectQuerySet, many=True)
        # return Response(serializer.data)

        ## serializing a queryset of raw query and give json response
        ## TODO
        # with connection.cursor() as cursor:
        query = "select * FROM api_basic_article WHERE booked = 1"
        queryset = Article.objects.raw(query)
        serializer = ArticleSerializer(queryset, many=True)

        print('and it happened.... yaayyyy')

        form = HotelForm()  # creating instance of HotelForm which we made in forms.py
        # args = {{'form': form, 'posts':queryset}}
        # return render(request, 'forms.html',{'form': form} )
        return Response(serializer.data)

        # cursor.execute(query)
        # queryset = cursor.fetchall()
        # django.db.models.query.QuerySet(queryset)

        # serializer = ArticleSerializer(queryset, many=True)
        # return Response(serializer.data)
    # return Response('all done')



@api_view(['GET','POST'])
def check_availability(request):
    if request.method == 'GET':
        form = CheckAvailabilityForm()      # creating instance of HotelForm which we made in forms.py

        title = 'Check Availability of Rooms'
        short_decription = 'select start and end dates to get rooms available in the period'
        args = {'form': form, 'Title': title, 'short_description': short_decription}
        return render(request, 'forms.html', args)        # sending form object to fit in forms.html ( wherever it is mentinoed) to render the paged


    if request.method == 'POST':
        print('got the post request')
        form = CheckAvailabilityForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            #name = form.cleaned_data['name']
            #print(str(start_date))

            query = "SELECT id, room FROM api_basic_article WHERE book_date >= '"+str(start_date)+"' AND book_date < '"+str(end_date)+"' GROUP BY room HAVING sum(booked=1)=0"
            queryset = Article.objects.raw(query)
            #print(queryset)
            serializer = RoomSerializer(queryset, many=True)
            return Response(serializer.data)


@api_view(['GET','POST'])
def multi_booking(request):
    # delete_everything()
    if request.method == 'GET':
        form = MultiBookingForm()      # creating instance of HotelForm which we made in forms.py

        title = 'Booking for a Time period'
        short_decription =  ''
        args = {'form': form, 'Title': title, 'short_description': short_decription}
        return render(request, 'forms.html', args)        # sending form object to fit in forms.html ( wherever it is mentinoed) to render the paged



    if request.method == 'POST':
        print('got the post request')
        form = MultiBookingForm(request.POST)

        if form.is_valid():
            room = form.cleaned_data['room']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            name = form.cleaned_data['name']

            # query = "SELECT id, room FROM api_basic_article WHERE book_date >= '"+str(start_date)+"' AND book_date < '"+str(end_date)+"' GROUP BY room HAVING sum(booked=1)=0"
            # queryset = Article.objects.raw(query)

            sdate = start_date  # start date
            edate = end_date      # end date

            delta = edate - sdate  # as timedelta
            with connection.cursor() as cursor:
                for i in range(delta.days + 1):
                    day = str(sdate + timedelta(days=i))
                    print(day)
                    query = "INSERT INTO api_basic_article (`id`, `room`, `book_date`, `booked`, `name`) VALUES (NULL, '" + str(room) + "', '" + str(day) + "', '1', '" +str(name)+ "')"
                    print(query)
                    cursor.execute(query)
                    #row = cursor.fetchone()

            response = "Booking is done for Mr/Ms "+str(name)+" from "+str(start_date)+" till "+str(end_date)
            print(response)
            # serializer = ArticleSerializer(queryset, many=True)
            return Response(response)


  # for deleting you might use objects.all().delete()


## to delete all entries on database simply call this function from any function
@api_view(['GET'])
def delete_everything(request):
    Article.objects.all().delete()
    print('everything is deleted')
    return Response('All wiped out')


@api_view(['GET'])
def initial_setup(request):

        a = sqls.sql()
        query = a.initial_insert
        with connection.cursor() as cursor:
            cursor.execute(query)
        return Response('You are good to go ahead, please go on other links')


## Cacelling one entry with room and date
@api_view(['GET','POST'])   # mentioning what all requests this function ( attached to a url) is going to have
def cancel_booking(request):
    if request.method == 'GET':
        print('got the get request cancel')
        form = CancelBookingForm()      # creating instance of HotelForm which we made in forms.py
        title = 'Cancel a Booking'
        short_decription = 'Enter room number and date of booking to be cancelled, you can check all bookings at "/allBooked"'

        args = {'form': form, 'Title': title, 'short_description': short_decription}
        return render(request, 'forms.html', args)        # sending form object to fit in forms.html ( wherever it is mentinoed) to render the paged

    if request.method == 'POST':
        print('got the post request cancel')
        form = CancelBookingForm(request.POST)
        row = 999
        if form.is_valid():                 # checking whether form that we got from post method is valid or not
            print('form is valid')
            room = form.cleaned_data['room']        # this is what you should do to store the data from forms
            date = form.cleaned_data['date']
            print('VALID', room,date)
            with connection.cursor() as cursor:

                query = "UPDATE api_basic_article SET booked = '0', name = 'NoBody' WHERE room = '" + str(room) + "' and book_date='" + str(date)+"'"
                cursor.execute(query)
                row = cursor.rowcount
                print('cursor query ran')

                print(row)

        if(row == 0):
            return Response('Seem you hava entered wrong room or date')
        else:
            return Response (' Booking cancellation succesfull')