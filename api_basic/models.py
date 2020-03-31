from django.db import models

# Create your models here.

class Article(models.Model):

    room = models.IntegerField(default=101)
    book_date = models.DateField()
    booked = models.IntegerField(default=0)
    name = models.CharField(max_length=20,default='Nobody')
    #
    # title = models.CharField(max_length=100,default='the secret')
    # author = models.CharField(max_length=100,default='david')
    # #email = models.EmailField(max_length=50,'oc@gmail.com')
    # date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.room,self.book_date,self.booked
        # return self.title