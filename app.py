import dbconnect as db



def main():
    flag = True
    
    print(' select the number for following')
    while (flag):
        print('=========================================================')
        print("1. New single booking")
        
        print("2. cancel a booking")

        print("3. check availability for a time period")

        print("4. multi days booking")
        
        print("5. show all bookings")

        print("7. EXIT")
        
        
        b=int(input("\nEnter your choice:"))
        if (b==1):
            print('which room you want to book between 101-110')
            roomid = str(input())
            
            print('for whom?....')
            name = str(input())
            
            print('select date in format YYYY-MM-DD')
            date = str(input())
            
            db.insert(roomid, date, name)
            print("your booking is done for", name)
            
        if (b==2):
            db.cancelBooking()            

        if (b==3):

            db.room_avaibility()

        if (b==4):

            db.booking_for_specific_time_period()
            
        if (b==5):
            db.show_all_bookings()
        
        if (b==7):
            flag = False
            quit()
        print()
        print()
        print('do you want to continue? y/n')
        yn = str(input())
        if(yn.lower() == 'n'):
            flag=False
        

main()