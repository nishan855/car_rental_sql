import sqlite3 as db
from datetime import date
from datetime import datetime


def reload():
    while True:
        print("\n")
        print("                   ~~~MAIN MENU ~~~")
        print("              ~~~ AVAILABLE FEATURES ~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("             1. Add new customer")
        print("             2. Add info of new vehicle")
        print("             3. Add info of new reservation")
        print("             4. Handle return of rental car")
        print("             5. Check Outstanding balance ")
        print("             6. Search Vehicles")
        print("             0. Exit")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        pick = input("\nPick an option to continue: ")

        # requirement 1
        if pick == "1":
            name = input('\nName of the customer: ')
            name = (name.capitalize(),)

            query = 'INSERT INTO customer (Name) VALUES(?)'
            cur.execute(query, name)
            mdb.commit()

            if cur:
                print('\n"%s" has been added to the customers list.\n' % name)
            else:
                print("User addition failed. Please try again!")
        '''---------------------------------------End of part 1----------------------------------------------------------------'''

        # requirement 2
        if pick == '2':
            print("\nEnter new information about a vehicle.")
            """Asks vehicle ID"""
            VehicleID = input("Enter vehicle ID: ")

            '''Asks vehicle description'''
            description = input("Enter vehicle description: ")

            '''Asks vehicle year'''
            year = input("Enter manufactured year: ")

            '''Asks vehicle type'''
            print(
                "\nSelect the vehicle type. Pick the number for its appropriate body type: 1:Compact, 2:Medium, 3:Large, 4:SUV, 5:Truck, 6:VAN")
            type_ = input("Enter your choice here: ")

            '''Asks vehicle category'''
            print("\nPick the the number for the category of the vehicle: 0:Basic, 1:Luxury")
            category = input("Enter your choice here: ")

            query = 'INSERT INTO vehicle (Vehicle_ID, Description, Year, Type, Category) VALUES(?,?,?,?,?)'
            val = (VehicleID, description, year, type_, category)
            cur.execute(query, val)

            if cur:
                print("\nSuccess!\n%s is added to the database." % description)
            mdb.commit()
        '''-----------------------------------------End of part 2-----------------------------------------------------------------------------'''

        # requirement 3
        if pick == '3':
            # get all the vehicles that are available for rental
            query = "SELECT Description, CASE WHEN vehicle.Type = 1 THEN 'Compact' WHEN vehicle.Type = 2 THEN 'Medium'"\
                    " WHEN vehicle.Type = 3 THEN 'Large' WHEN vehicle.Type = 4 THEN 'SUV' WHEN vehicle.Type = 5 " \
                    "THEN 'Truck' WHEN vehicle.TYPE = 6 THEN 'Van' END AS Type, CASE WHEN vehicle.Category = 0 THEN 'Basic' " \
                    "WHEN vehicle.Category = 1 THEN 'Luxury' END AS Property FROM vehicle WHERE vehicle.Vehicle_ID NOT IN " \
                    "(SELECT Vehicle_ID FROM rental WHERE payment_date is 'NULL') ORDER BY Description ASC"
            cur.execute(query)
            data = cur.fetchall()
            # print(data)
            print("\nTotal vehicles available for rental: %s" % len(data))
            print("________________________________________________")
            print("\nModel                   Body type      Property")
            print("________________________________________________")
            for x in range(len(data)):
                print('{:25s}{:15s}{:s}'.format(data[x][0], data[x][1], data[x][2]))

            vehicle_choice = input("\nPlease select the vehicle that you want to rent: ")

            # get the VIN of the vehicle picked by the client
            query = "SELECT Vehicle_ID FROM vehicle WHERE Description = ?"
            cur.execute(query, (vehicle_choice,))
            data = cur.fetchall()
            print(data)
            vehicle_ID = data[0][0]

            # asking for start date of rental
            start_date = input(
                "\nFrom when do you want to start the rental? Please put the date in the format: year-month-day: ")

            # asking for return date of rental
            return_date = input(
                "\nWhen do you want to return the car? Please put the date in the format: year-month-day: ")

            rental_choice = int(input(
                "\nDo you want to rent on daily basis or weekly basis? To pick daily enter 1, for weekly enter 7: "))

            # prompt for the payment choice
            print("\nPerfect!\nNow one last question and you are good to go.\n")
            payment_choice = input(
                "Do you want to make the payment on start date or on the returned day? Please pick 'Yes' for start date, 'No' for returned date: ")

            # if the user picks yes, the payment_date column records the current date when the car was booked for rental
            if payment_choice in ['Yes', 'yes', 'YES']:
                payment_date = date.today()

            # payment day will be the date when the car is returned
            else:
                payment_date = return_date

            # register the picked vehicle for that client, insert into the table rental
            query = "INSERT INTO rental (Vehicle_ID, Qty, Start_date, Order_date, Return_date," \
                    " payment_date, Rental_type, Returned) VALUES(?,?,?,?,?,?,?,?)"
            val = (vehicle_ID, 1, start_date, date.today(), return_date, payment_date, rental_choice, 0)
            cur.execute(query, val)

            # calculate the total amount for the rental duration
            date_format = "%Y-%m-%d"
            a = datetime.strptime(start_date, date_format)  # start date of rental
            b = datetime.strptime(return_date, date_format)  # return date of rental
            delta = b - a  # get total rental days
            # print(delta.days)

            if cur:
                print("\nSuccess!")
                print("Your booking information is shown below.")
                print("________________________________________________________________________")
                print("Car                      Start date     Return date     Rental duration")
                print("________________________________________________________________________")
                print('{:25s}{:15s}{:s}{:8d} days\n'.format(vehicle_choice, start_date, return_date, delta.days))
            else:
                print('Booking failed! Please try again!')
            mdb.commit()
        '''--------------------------------------------------------------End of part 3--------------------------------------------------------------------------'''

        if pick == '4':
            customer_name = input("Customer name: ")

            return_date = input("Enter return date in the format: Year-month-day: ")

            vehicle_info = input("Enter vehicle description: ")

            # get the start date and rental type(weekly or daily basis) from the table rental
            query = "SELECT vehicle_ID, start_date, rental_type FROM rental " \
                    "WHERE Cust_ID IN (SELECT Cust_ID FROM customer WHERE Name =?) AND" \
                    " Vehicle_ID IN (SELECT Vehicle_ID FROM vehicle Where Description =?) AND Return_date =?"
            val = (customer_name, vehicle_info, return_date)
            cur.execute(query, val)


            data = cur.fetchall()
            vehicle_ID = data[0][0]
            start_date = data[0][1]
            rental_type = data[0][2]

            # calculate total duration of rental
            date_format = "%Y-%m-%d"
            a = datetime.strptime(start_date, date_format)  # start date of rental
            b = datetime.strptime(return_date, date_format)  # return date of rental
            delta = b - a  # get total rental days
            # print(delta.days)

            # get the daily and weekly rate of the vehicle
            query = "SELECT Weekly, Daily FROM rate INNER JOIN vehicle ON rate.Type = vehicle.Type " \
                    "AND rate.Category = vehicle.Category WHERE vehicle.Description = ?"
            val = (vehicle_info,)
            cur.execute(query, val)


            data = cur.fetchall()
            weekly_rate = data[0][0]
            daily_rate = data[0][1]
            # print(weekly_rate, daily_rate)

            # calculate the total payment for the specific rental type
            total_amount = 0

            if rental_type == 1:
                total_amount = delta.days * daily_rate
            elif rental_type == 7:
                if delta.days >= 7:
                    exact_days = delta.days % 7
                    exact_week = delta.days // 7
                    total_amount = exact_week * weekly_rate + exact_days * daily_rate

            print("\nTotal payment due: $", total_amount)

            # update the rental for the returned car
            query = "UPDATE rental SET Total_amount = ?, Returned = 1,payment_date=" \
                    " CASE WHEN payment_date='NULL' THEN '2020-01-01' ELSE payment_date" \
           " END WHERE Vehicle_ID= ? AND Return_date=?"
            val = (total_amount, vehicle_ID, return_date)
            cur.execute(query, val)

            if cur:
                print("Success!\nRental information has been updated.")

            mdb.commit()
        '''----------------------------------------------------End of part 4-----------------------------------------------------------------------------'''

        if pick == '5':
            print(
                "Pick from the options if you want to search by- \n1: Customer name\n2: Customer ID\n3: Part of customer name\n4: Show all results\n5: Return to main menu")
            filter = input("\nEnter your option: ")

            while True:
                if filter == '1':
                    name = input("Enter the full name of the customer: ")

                    query = "SELECT CustomerID, CustomerName, CASE WHEN SUM(RentalBalance) == 0 THEN '0.00' " \
                            "ELSE SUM(RentalBalance) END AS  RentalBalance FROM vRentalInfo WHERE CustomerName=? " \
                            "GROUP BY CustomerID"
                    cur.execute(query, (name,))

                    if cur:
                        data = cur.fetchall()
                        # print(data)
                        if data == []:
                            print("%s has not rented any vehicle yet.\n" % name)
                        else:
                            print("______________________________________________________")
                            print("Customer ID    Customer Name        Remaining balance")
                            print("______________________________________________________")

                            for i in data:
                                print('{:15s}{:21s}${}'.format(str(i[0]), i[1], i[2]))
                    else:
                        print('Failed to get the data from the database.')

                if filter == '2':
                    ID = input("Enter customer ID: ")

                    query = "SELECT CustomerID, CustomerName, CASE WHEN SUM(RentalBalance) == 0 THEN '0.00' " \
                            "ELSE SUM(RentalBalance) END AS RentalBalance FROM vRentalInfo " \
                            "WHERE CustomerID=? GROUP BY CustomerID"
                    cur.execute(query, (ID,))


                    if cur:
                        data = cur.fetchall()
                        # print(data)
                        if data == []:
                            print("Customer ID %s has not rented any vehicle yet." % ID)
                        else:
                            print("______________________________________________________")
                            print("Customer ID    Customer Name        Remaining balance")
                            print("______________________________________________________")

                            for i in data:
                                print('{:15s}{:21s}${}'.format(str(i[0]), i[1], i[2]))
                    else:
                        print('Failed to get the data from the database.')

                if filter == '3':
                    name = input("Enter the first name or last name: ")
                    name = name.capitalize()
                    query = (
                        "SELECT CustomerID, CustomerName, CASE WHEN SUM(RentalBalance) == 0 THEN '0.00' "
                        "ELSE SUM(RentalBalance)"
                        " END AS RentalBalance FROM vRentalInfo WHERE CustomerName LIKE ? OR CustomerName LIKE ?")
                    cur.execute(query, (name + '%', '%' + name))


                    try:
                        if cur:
                            data = cur.fetchall()
                            # print(data)
                            print("______________________________________________________")
                            print("Customer ID    Customer Name        Remaining balance")
                            print("______________________________________________________")

                            for i in data:
                                print('{:16s}{:22s}${}'.format(str(i[0]), i[1], i[2]))
                        else:
                            print('Failed to get the data from the database.')

                    except TypeError:
                        print("User not found in the database.")

                if filter == '4':
                    query = "SELECT CustomerID, CustomerName, CASE WHEN SUM(RentalBalance) == 0 THEN 0.00 " \
                            "ELSE CAST(SUM(RentalBalance) AS int) " \
                            "END AS  RentalBalance FROM vRentalInfo GROUP BY CustomerID ORDER BY RentalBalance"
                    cur.execute(query)
                    if cur:
                        data = cur.fetchall()
                        # print(data)
                        print("Payment due for the customers is shown below:")
                        print("______________________________________________________")
                        print("Customer ID    Customer Name        Remaining balance")
                        print("______________________________________________________")

                        for i in data:
                            print('{:15s}{:21s}${}'.format(str(i[0]), i[1], i[2]))
                        break
                    else:
                        print('Failed to get the data from the database.')

                if filter == '5':
                    reload()
        '''------------------------------------------------------------End of part 5a-----------------------------------------------------------------------------'''

        if pick == '6':
            print(
                "Pick an option: \n 1.List all vehicles \n 2. Search by VIN \n 3. Search by Description \n 4. Search "
                "by part of Description")

            opt = input("\nEnter a choice to search for vehicles:")

            if opt == '1':
                query1 = "Select DISTINCT VIN, Vehicle, CASE WHEN DAILY='null' THEN 'Not Applicable'" \
                         "ELSE Daily END AS DAILY  From vRentalInfo, vehicle,rate " \
                         "WHERE vRentalInfo.VIN = vehicle.Vehicle_ID AND vehicle.type = rate.type AND " \
                         "vehicle.Category = rate.Category ORDER BY DAILY "

                cur.execute(query1)
                if cur:
                    data = cur.fetchall()

                    print("All vehicles:")
                    print("___________________________________________________________________")
                    print("VIN                       Description                 Daily Rate")
                    print("___________________________________________________________________")

                    for i in data:
                        print('{:25s}{:30s}${:0.2f}'.format(str(i[0]), i[1], i[2]))

                else:
                    print('Failed to get the data from the database.')

            if opt == '2':
                vin = input("Enter the VIN number of the vehicle: ")

                query1 = "Select DISTINCT VIN, Vehicle, CASE WHEN DAILY='null' THEN 'Not Applicable' ELSE DAILY" \
                         "  END AS DAILY From vRentalInfo, vehicle, rate WHERE " \
                         "vRentalinfo.VIN=? AND vRentalInfo.VIN = vehicle.Vehicle_ID AND vehicle.type = rate.type AND "\
                         "vehicle.Category = rate.Category ORDER BY DAILY "

                cur.execute(query1, (vin,))
                if cur:
                    data = cur.fetchall()

                    print("All vehicles:")
                    print("___________________________________________________________________")
                    print("VIN                       Description                 Daily Rate")
                    print("___________________________________________________________________")

                    for i in data:
                        print('{:25s}{:30s}${:0.2f}'.format(str(i[0]), i[1], i[2]))

                else:
                    print('Failed to get the data from the database.')

        if opt == '3':
            desc = input("Enter the description of the vehicle: ")

            query1 = "Select DISTINCT VIN, Vehicle, CASE WHEN DAILY='null' THEN 'Not Applicable' ELSE DAILY" \
                     "  END AS DAILY From vRentalInfo, vehicle, rate WHERE " \
                     "vRentalinfo.Vehicle=? AND vRentalInfo.VIN = vehicle.Vehicle_ID AND vehicle.type = rate.type AND "\
                     "vehicle.Category = rate.Category  ORDER BY DAILY"

            cur.execute(query1, (desc,))
            if cur:
                data = cur.fetchall()

                print("All vehicles:")
                print("___________________________________________________________________")
                print("VIN                       Description                 Daily Rate")
                print("___________________________________________________________________")

                for i in data:
                    print('{:25s}{:30s}${:0.2f}'.format(str(i[0]), i[1], i[2]))

            else:
                print('Failed to get the data from the database.')

        if opt == '4':
            prt = input("Enter the part of description of the vehicle: ")

            query1 = "Select DISTINCT VIN, Vehicle, CASE WHEN DAILY='null' THEN 'Not Applicable' ELSE DAILY " \
                     "  END AS DAILY From vRentalInfo, vehicle, rate " \
                     "WHERE (vRentalinfo.Vehicle LIKE ? OR vRentalinfo.Vehicle LIKE ?) " \
                     "AND vRentalInfo.VIN = vehicle.Vehicle_ID AND vehicle.type = rate.type AND vehicle.Category = " \
                     "rate.Category ORDER BY DAILY"

            cur.execute(query1, ('%' + prt, prt + '%'))
            if cur:
                data = cur.fetchall()

                print("All vehicles:")
                print("___________________________________________________________________")
                print("VIN                       Description                 Daily Rate")
                print("___________________________________________________________________")

                for i in data:
                    print('{:25s}{:30s}${:0.2f}'.format(str(i[0]), i[1], i[2]))

            else:
                print('Failed to get the data from the database.')

        '''------------------------------------------------------------End of part 5b----------------------------------------------------------------------------- '''

        if pick == '0':
            print('\nProgram terminated!')
            exit()


if __name__ == '__main__':
    # connection to database
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()

    query = "UPDATE rental SET Total_amount = 100, Returned = 1,payment_date=" \
            " CASE WHEN payment_date='NULL' THEN '2020-01-01' ELSE payment_date" \
            " END WHERE Vehicle_ID= 'JTHFF2C26F135BX45' AND Return_date='2020-01-29'"

    cur.execute(query)
    mdb.commit()
    mdb.close()
