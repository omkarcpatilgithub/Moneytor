from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .forms import  HotelForm2
import django

# Create your views here.


# for p in Person.objects.raw('SELECT id, first_name FROM myapp_person'):
# ...     print(p.first_name, # This will be retrieved by the original query
# ...           p.last_name) # This will be retrieved on demand

@api_view(['GET'])
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
        #with connection.cursor() as cursor:
            query = "select * FROM api_basic_article WHERE booked = 1"
            queryset = Article.objects.raw(query)
            serializer = ArticleSerializer(queryset, many=True)

            print('and it happened.... yaayyyy')
            return Response(serializer.data)




            # cursor.execute(query)
            # queryset = cursor.fetchall()
            # django.db.models.query.QuerySet(queryset)

            #serializer = ArticleSerializer(queryset, many=True)
            #return Response(serializer.data)
        # return Response('all done')

def clear_duplicates():
    ## deletes all duplicate entries wrt room and date,  executes raw sql query
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM api_basic_article WHERE ID NOT IN ( SELECT MAX(ID) AS MaxRecordID FROM api_basic_article GROUP BY room, book_date)")
        #cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()
        print('clear duplicates done')

    return row
@api_view(['GET'])
def after_duplicate_remove(request):
    ## removes duplicates and shows whole list
    clear_duplicates()
    # article_list(request)
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    print(' printing article list after clearing duplicates')
    return Response(serializer.data)


    #return Response('lets see what happens next',status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
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


@api_view(['GET','PUT','DELETE'])
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


@api_view(['GET','POST'])
def Hotel_detail2(request):
    if request.method == 'GET':
        print('got the get request')
        form = HotelForm2()
        return render(request, 'forms.html', {'form': form})

    if request.method == 'POST':
        print('got the post request')
        form = HotelForm2(request.POST)
        if form.is_valid():
            print('VALID')
            form.save()
            return Response('changes are made check at admin once')

