import mysql.connector
from datetime import date, timedelta,datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database='moneytor'

)

#print(mydb)
mycursor = mydb.cursor()

def selectall():
    # select everythin
    table = 'hotel'
    query = 'select * from ' + table
    mycursor.execute(query)
    m = mycursor.fetchall()
    
    return m

# insert a new record with booked 1
def insert(roomid, date, name):
    # insert new entry
    
    query = "INSERT INTO hotel VALUES (NULL, '"+roomid+"', '"+date+"', '1', '"+name+"')"
    mycursor.execute(query)
    clear_duplicates()
    mycursor.execute('commit')
    return 
    

    
# if any duplicates are present in database then removes all previous and keeps latest one
def clear_duplicates():
    # to clear ducplicates
    query = '''DELETE FROM hotel
        WHERE ID NOT IN
        (
            SELECT MAX(ID) AS MaxRecordID
            FROM hotel
            GROUP BY roomid, book_date
        )'''
    mycursor.execute(query)
    mycursor.execute('commit')
    

# select specific date entries
def specific_date():
    date = str(input())
    query = "select * from hotel where book_date ='"+date+"'"
    mycursor.execute(query)
    m = mycursor.fetchall()

    return m



# select specific room entry
def specific_room():
    roomid = str(input())
    query = "select * from hotel where roomid ='"+roomid+"'"
    mycursor.execute(query)
    m = mycursor.fetchall()

    return m


    
# shows result in proper format
def showresult(result):
    print('roomid\t booking date\t booked\t Name')
    for x in result:
        print(x[1],'\t',x[2],'\t',x[3],'\t',x[4])
        
        
# cancel booking after asking the roomid and the booked date      
def cancelBooking():
    print('enter room you want to cancel')
    roomid = str(input())
    print('for which date want to cancel')
    date = str(input())
    query = "UPDATE hotel SET booked = '0', name = '' WHERE roomid = '"+roomid+"' and book_date='"+date+"'"
    mycursor.execute(query)
    affected_rows = mycursor.rowcount
    clear_duplicates()
    mycursor.execute('commit')
    
    return affected_rows  


def check_result():
    roomid = str(input())
    date = str(input())
    query = "select * from hotel where roomid ='"+roomid+"'and book_date='"+date+"'"
    mycursor.execute(query)
    m = mycursor.fetchall()
    if (m == []):
        print('seems wrong input')
    else:
        print('input is valid..... ')

        
# giving result of all the rooms which are available for certain period
def room_avaibility():
    print('select from date in format YYYY-MM-DD')
    startdate = str(input())
    print('select end date in format YYYY-MM-DD')
    endate = str(input())
    query = "SELECT roomid FROM hotel WHERE book_date >= '"+startdate+"' AND book_date < '"+endate+"' GROUP BY roomid HAVING sum(booked=1)=0"
    mycursor.execute(query)
    m = mycursor.fetchall()
    print()
    print('following rooms are available from',startdate, 'to',endate)
    for i in m:
        print(i[0])
        

def show_all_bookings():
    query = "SELECT * FROM hotel WHERE booked = '1'"
    mycursor.execute(query)
    m = mycursor.fetchall()
    showresult(m)
        

def booking_for_specific_time_period():
    print('which room you want to book between 101-110')
    roomid = str(input())

    print('for whom?....')
    name = str(input())

    print('select from date in format YYYY-MM-DD')
    my_string = str(input())

    # Create date object in given time format yyyy-mm-dd
    my_date = datetime.strptime(my_string, "%Y-%m-%d")
    #print(my_date)

    print('select end date in format YYYY-MM-DD')
    enddate = str(input())
    my_dateend = datetime.strptime(enddate, "%Y-%m-%d")
    #print(my_dateend)

    sdate = my_date.date()  # start date
    edate = my_dateend.date()   # end date

    delta = edate - sdate       # as timedelta


    for i in range(delta.days + 1):
        day = str(sdate + timedelta(days=i))
        insert(roomid, day, name)

