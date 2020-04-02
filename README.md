# Moneytor
Hotel management for Moneytor hotel
a REST API is created with Django framework,

--model is creted for following fields ['room','book_date','booked','name'] (models.py)

model is serialized with ModelSerializer (in serializers.py)

follwing urls implemented: (urls.py)

-path('rooms/', article_list), : to get all the entries of rooms OR post a new entry (in json format)

-path('detail/int:pk', article_detail), : to get/put/delete single entry with its id (pk)

-path('allbooked',raw_input), : to get only booked rooms with their dates

-path('clear_dup',clear_duplicates), : to clear duplicates wichever created ( this function fires a row sql query)

-path('after_dup_remove',after_duplicate_remove) : to get all entries available after clearing duplicates

according functions are written in views.py

#######################################################################
form are added to take input from user
