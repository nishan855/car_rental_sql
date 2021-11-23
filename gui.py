from tkinter import *
import sqlite3 as db

from datetime import date
from datetime import datetime

mdb = db.connect("car_rental.db")
cur = mdb.cursor()

root = Tk()
root.geometry("400x400")

root.title('Car Rental Application')



my_menu = Menu(root)
root.config(menu=my_menu)

# frames for adding customer
cust_frame = Frame(root, width=400, height=400, bg="grey")

#frame for adding vehicles
vehicle_frame = Frame(root, width=400, height=400, bg="grey")

#frames for new rental
rent_frame=Frame(root, width=400, height=400, bg="grey")
rent_frame1=Frame(root, width=400, height=400, bg="grey")

ui_frame=Frame(root, width=400, height=400, bg="grey")
canvas = Canvas(ui_frame,width=1200,height=1000)
ui_frame.pack()
canvas.pack()
img = PhotoImage(file="frontImage.png")
canvas.create_image(0, 0, anchor=NW, image=img)


def hide_frames():
    ui_frame.pack_forget()
    canvas.pack_forget()
    cust_frame.pack_forget()
    vehicle_frame.pack_forget()
    rent_frame.pack_forget()
    rent_frame1.pack_forget()
    ret_frame.pack_forget()
    bal_frame.pack_forget()
    bal_frame1.pack_forget()
    bal_frame2.pack_forget()
    bal_frame3.pack_forget()
    srch_frame.pack_forget()
    srch_frame1.pack_forget()
    srch_frame2.pack_forget()
    srch_frame3.pack_forget()



# entries for adding  new customer
cust_name_lab = Label(cust_frame, text="Name", bg="grey", font='Helvetica 20 bold')
cust_name_lab.grid(row=1, column=0)
info = StringVar()
cust_name = Entry(cust_frame, width=50)
cust_name.grid(row=1, column=1, padx=20, ipady=10)
label1 = Label(cust_frame, text="New Customer has been added to database.",
               font='Helvetica 15 bold')


# adding customer
def cust_add():
    hide_frames()
    label1.grid_forget()
    cust_frame.pack(fill="both", expand=1)
    submit_btn = Button(cust_frame, text=" Add Customer", width=5, bg="orange", command=submit_cust)
    submit_btn.grid(row=2, column=0, columnspan=2, pady=20, padx=100, ipadx=100)


# submit to add new customer
def submit_cust():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()
    cur.execute("INSERT INTO customer (Name) VALUES (:cust_name)",
                {
                    'cust_name': cust_name.get()
                })
    mdb.commit()
    mdb.close()
    label1.grid(row=5, column=1)

    print("yjjjjjjjjj")
    #///////////////////////////////////////////
    #//////////////////////////////////////////////
    #//////////////////////////////////////////////
#################################################################################################################
# entries for adding  new vechile
vecid_lab = Label(vehicle_frame, text="Vehicle ID", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
vecid = Entry(vehicle_frame, width=50)
vecid.grid(row=1, column=1, padx=20, ipady=10)

desc_lab = Label(vehicle_frame, text="Description", bg="grey", font='Helvetica 20 bold').grid(row=2, column=0)
desc00= Entry(vehicle_frame, width=50)
desc00.grid(row=2, column=1, padx=20, ipady=10)

year_lab = Label(vehicle_frame, text="Year", bg="grey", font='Helvetica 20 bold').grid(row=3, column=0)
year= Entry(vehicle_frame, width=50)
year.grid(row=3, column=1, padx=20, ipady=10)

type_lab = Label(vehicle_frame, text="Type", bg="grey", font='Helvetica 20 bold').grid(row=4, column=0)
type_lab1 = Label(vehicle_frame, text="**Enter 1:Compact, 2:Medium, 3:Large, 4:SUV, 5:Truck, 6:VAN",fg='blue', bg="grey", font='Helvetica 15').grid(row=4, column=2)
type1 = Entry(vehicle_frame, width=50)
type1.grid(row=4, column=1, padx=20, ipady=10)

categ_lab = Label(vehicle_frame, text="Category", bg="grey", font='Helvetica 20 bold').grid(row=5, column=0)
categ_lab1 = Label(vehicle_frame, text="**Enter  0:Basic, 1:Luxury ",fg='blue',bg="grey", font='Helvetica 15').grid(row=5, column=2)
categ = Entry(vehicle_frame, width=50)
categ.grid(row=5, column=1, padx=20, ipady=10)
label2 = Label(vehicle_frame, text="New Vehicle has been added to database.",
               font='Helvetica 15 bold')


def vec_add():
    hide_frames()
    label2.grid_forget()
    vehicle_frame.pack(fill="both", expand=1)
    submit_vbtn = Button(vehicle_frame, text=" Add vehicle", width=5, bg="orange", command=submit_vech)
    submit_vbtn.grid(row=6, column=0, columnspan=2, pady=20, padx=100, ipadx=100)



# submit to add new customer
def submit_vech():
    mdb1 = db.connect("car_rental.db")
    cur1= mdb1.cursor()
    VehicleID=vecid.get()
    description=desc00.get()
    yr= year.get()
    type= type1.get()
    category= categ.get()
    query = 'INSERT INTO vehicle (Vehicle_ID, Description, Year, Type, Category) VALUES(?,?,?,?,?)'
    val = (VehicleID, description, yr, type, category)
    cur1.execute(query, val)
    mdb1.commit()
    mdb1.close()
    label2.grid(row=7, column=1)


# customer menu
customer_menu = Menu(my_menu)
my_menu.add_cascade(label="Customer", menu=customer_menu)
customer_menu.add_command(label="Add Customer", command=cust_add)

# Vehicle menu
vec_menu = Menu(my_menu)
my_menu.add_cascade(label="Vehicles", menu=vec_menu)
vec_menu.add_command(label="Add Vehicle", command=vec_add)

#view all rental vehicles
##############################################################################################################
def see_all():
    hide_frames()
    rent_frame.pack(fill="both", expand=1)
    mdb1 = db.connect("car_rental.db")
    cur1 = mdb1.cursor()
    query = "SELECT Description, CASE WHEN vehicle.Type = 1 THEN 'Compact' WHEN vehicle.Type = 2 THEN 'Medium'" \
            " WHEN vehicle.Type = 3 THEN 'Large' WHEN vehicle.Type = 4 THEN 'SUV' WHEN vehicle.Type = 5 " \
            "THEN 'Truck' WHEN vehicle.TYPE = 6 THEN 'Van' END AS Type, CASE WHEN vehicle.Category = 0 THEN 'Basic' " \
            "WHEN vehicle.Category = 1 THEN 'Luxury' END AS Property FROM vehicle WHERE vehicle.Vehicle_ID NOT IN " \
            "(SELECT Vehicle_ID FROM rental WHERE payment_date is 'NULL') ORDER BY Description ASC"
    cur1.execute(query)
    data = cur1.fetchall()
    rentals_head = Label(rent_frame, text="Model                           Body Type                         Property",fg='blue',bg='white',font='Helvetica 6 bold')
    rentals_head.grid(row=0, column=2, columnspan=2)
    print_vec=''
    for x in range(len(data)):
        print_vec +=str(data[x][0]).rjust(20, " ")+" "+str(data[x][1]).rjust(20," ")+" "+str(data[x][2]).rjust(20," ")+ "\n"

    all_rentals=Label(rent_frame,text=print_vec,bg='white',font='Helvetica 6 bold')
    all_rentals.grid(row=1,column=2,columnspan=2)
    mdb1.close()

#entries for renting new vehicles
desc_lab = Label(rent_frame1, text="Description", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
desc = Entry(rent_frame1, width=50)
desc.grid(row=1, column=1, padx=20, ipady=10)

start_lab = Label(rent_frame1, text="Start date", bg="grey", font='Helvetica 20 bold').grid(row=2, column=0)
start_lab1 = Label(rent_frame1, text="**Please put the date in the format: year-month-day",fg='blue', bg="grey", font='Helvetica 15').grid(row=2, column=2)
start= Entry(rent_frame1, width=50)
start.grid(row=2, column=1, padx=20, ipady=10)

return_lab = Label(rent_frame1, text="Return Date", bg="grey", font='Helvetica 20 bold').grid(row=3, column=0)
return_lab1 = Label(rent_frame1, text="**Please put the date in the format: year-month-day",fg='blue', bg="grey", font='Helvetica 15').grid(row=3, column=2)
returnd= Entry(rent_frame1, width=50)
returnd.grid(row=3, column=1, padx=20, ipady=10)

plan_lab = Label(rent_frame1, text="Rental plan", bg="grey", font='Helvetica 20 bold').grid(row=4, column=0)
plan_lab1 = Label(rent_frame1, text="**To pick daily enter 1, for weekly enter 7",fg='blue', bg="grey", font='Helvetica 15').grid(row=4, column=2)
plan = Entry(rent_frame1, width=50)
plan.grid(row=4, column=1, padx=20, ipady=10)

pay_lab = Label(rent_frame1, text="Payment On", bg="grey", font='Helvetica 20 bold').grid(row=5, column=0)
pay_lab1 = Label(rent_frame1, text="pick 'Yes' for payment on start date, 'No' for return date",fg='blue', bg="grey", font='Helvetica 15').grid(row=5, column=2)
pay= Entry(rent_frame1, width=50)
pay.grid(row=5, column=1, padx=20, ipady=10)

succ = Label(rent_frame1, text="New Customer has been added to database.",
               font='Helvetica 15 bold')

def rent_vech():
    hide_frames()
    label2.grid_forget()
    rent_frame1.pack(fill="both", expand=1)
    submit_rbtn = Button(rent_frame1, text="Rent", width=5, bg="orange", command=submit_rent)
    submit_rbtn.grid(row=6, column=0, columnspan=2, pady=20, padx=100, ipadx=100)

def submit_rent():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()
    attr= desc.get()
    start_date=start.get()
    payment_choice=pay.get()
    return_date=returnd.get()
    rental_choice=plan.get()



    query = "SELECT Vehicle_ID FROM vehicle WHERE Description = ? AND " \
            " vehicle.Vehicle_ID NOT IN (SELECT Vehicle_ID FROM rental WHERE payment_date is 'NULL')"
    cur.execute(query, (attr,))

    data = cur.fetchall()


    if data:
        vehicle_ID = data[0][0]

    else:
       succal = Label(rent_frame1, text="Vehicle not available right now.", bg='grey', font='Helvetica 15 bold')
       succal.grid(row=8, column=0, columnspan=2)



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
        succ = Label(rent_frame1, text="!!!!!!!!!!!!!! Success !!!!!!!!!!!!!!!!",fg='green',bg='grey',font='Helvetica 15 bold')
        succ.grid(row=7, column=0, columnspan=2)
        succ1 = Label(rent_frame1, text="Car              Start Date              Return Date              Duration", bg='grey', fg='blue',font='Helvetica 15 bold')
        succ2 = Label(rent_frame1, text=str(attr)+"              "+str(start_date)+"              "+str(return_date)+"              "+str(delta.days)+ " days", bg='grey',font='Helvetica 15 bold')
        succ1.grid(row=8, column=0, columnspan=2)
        succ2.grid(row=9, column=0, columnspan=2)


    else:
        succ4 = Label(rent_frame1, text="Booking failed! Please try again!", bg='grey', font='Helvetica 15 bold')

        succ4.grid(row=7, column=0, columnspan=2)

    mdb.commit()
    mdb.close()

# rental menu
rent_menu = Menu(my_menu)
my_menu.add_cascade(label="Rentals", menu=rent_menu)
rent_menu.add_command(label="All available vehicles",command=see_all)
rent_menu.add_command(label="Rent a Vehicle", command=rent_vech)

##############################################################################################
#frame for return
ret_frame = Frame(root, width=400, height=400, bg="grey")

#entries for handling return
cname_lab = Label(ret_frame, text="Customer name", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
cname = Entry(ret_frame, width=50)
cname.grid(row=1, column=1, padx=20, ipady=10)

ret11_lab = Label(ret_frame, text="Return date", bg="grey", font='Helvetica 20 bold').grid(row=2, column=0)
ret11_lab1 = Label(ret_frame, text="**Please put the date in the format: year-month-day",fg='blue', bg="grey", font='Helvetica 15').grid(row=2, column=2)
ret11 = Entry(ret_frame, width=50)
ret11.grid(row=2, column=1, padx=20, ipady=10)

des11_lab = Label(ret_frame, text="Description", bg="grey", font='Helvetica 20 bold').grid(row=3, column=0)
des11= Entry(ret_frame, width=50)
des11.grid(row=3, column=1, padx=20, ipady=10)

succ1 = Label(ret_frame, text="Success!! Vehicle returned Successfully.",
               font='Helvetica 15 bold', fg='blue')



#callback
def retn_vec():
    hide_frames()
    succ1.grid_forget()
    ret_frame.pack(fill="both", expand=1)
    submit_rtnn = Button(ret_frame, text="Return", width=5, bg="orange", command=submit_rtnv)
    submit_rtnn.grid(row=4, column=0, columnspan=2, pady=20, padx=100, ipadx=100)

def submit_rtnv():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()

    customer_name= cname.get()
    vehicle_info = des11.get()
    return_date= ret11.get()



    # get the start date and rental type(weekly or daily basis) from the table rental
    query = "SELECT vehicle_ID, start_date, rental_type FROM rental WHERE Cust_ID IN (SELECT Cust_ID FROM customer WHERE Name =?) AND Vehicle_ID IN (SELECT Vehicle_ID FROM vehicle Where Description =?) AND Return_date =?"
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
    query = "SELECT Weekly, Daily FROM rate INNER JOIN vehicle ON rate.Type = vehicle.Type AND rate.Category = vehicle.Category WHERE vehicle.Description = ?"
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



    # update the rental for the returned car
    query = "UPDATE rental SET Total_amount = ?, Returned = 1,payment_date=" \
            " CASE WHEN payment_date='NULL' THEN ? ELSE payment_date" \
            " END WHERE Vehicle_ID=? AND Return_date=?"

    val = (total_amount, return_date, vehicle_ID, return_date)
    cur.execute(query, val)


    succ2=Label(ret_frame, text="Amount due: $"+ str(total_amount) ,
               font='Helvetica 15 bold', fg='red')

    if cur:
        succ1.grid(row=5,column=0)
        succ2.grid(row=6,column=0)

    mdb.commit()
    mdb.close()




# return menu
ret_menu = Menu(my_menu)
my_menu.add_cascade(label="Return Vehicle", menu=ret_menu)
ret_menu.add_command(label="Handle Return", command=retn_vec)

#######################################################################################################################

#frames for checking balance
bal_frame=Frame(root, width=400, height=400, bg="grey")
bal_frame1=Frame(root, width=400, height=400, bg="grey")
bal_frame2=Frame(root, width=400, height=400, bg="grey")
bal_frame3=Frame(root, width=400, height=400, bg="grey")

#entries for handling remaining balances
cust_id1_lab = Label(bal_frame1, text="Customer ID", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
cust_id1= Entry(bal_frame1, width=50)
cust_id1.grid(row=1, column=1, padx=20, ipady=10)

cust_name1_lab = Label(bal_frame2, text="Customer Name", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
cust_name1= Entry(bal_frame2, width=50)
cust_name1.grid(row=1, column=1, padx=20, ipady=10)

cust_npart_lab = Label(bal_frame3, text="Part of name", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
cust_npart= Entry(bal_frame3, width=50)
cust_npart.grid(row=1, column=1, padx=20, ipady=10)


def ck_def():
    hide_frames()
    bal_frame.pack(fill="both", expand=1)
    query = "SELECT CustomerID, CustomerName, CASE WHEN SUM(RentalBalance) == 0 THEN 0.00 ELSE CAST(SUM(RentalBalance) AS int) END AS  RentalBalance FROM vRentalInfo GROUP BY CustomerID ORDER BY RentalBalance"
    cur.execute(query)
    if cur:
        data = cur.fetchall()
        succc1 = Entry(bal_frame, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succc1.grid(row=1, column=0)
        succc1.insert(END, "Customer ID")

        succ111 = Entry(bal_frame, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=1, column=1)
        succ111.insert(END, "Name")

        succ111 = Entry(bal_frame, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=1, column=2)
        succ111.insert(END, "Remaining Balance")

        i = 2
        for d in data:
            for j in range(len(d)):
                e = Entry(bal_frame, width=22, fg='blue', font='Helvetica 12 bold')
                e.grid(row=i, column=j)
                if j==2:
                    if d[j]==0.00:
                       e.insert(END,"$ 0.00")
                    else:
                        e.insert(END,"$"+ str(d[j]))
                else:
                    e.insert(END, d[j])
            i = i + 1


    else:
        print('Failed to get the data from the database.')

def ck_id():
    hide_frames()
    bal_frame1.pack(fill="both", expand=1)
    submit_id = Button(bal_frame1, text="Check", width=5, bg="orange", command=submit_ckid)
    submit_id.grid(row=3, column=0, columnspan=2, pady=20, padx=100, ipadx=100)

def submit_ckid():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()
    ID=cust_id1.get()
    wid = bal_frame1.winfo_children()

    if len(wid) > 3:
        for i in range(4, len(wid)):
            wid[i].destroy()
    query = "SELECT CustomerID, CustomerName, CASE WHEN SUM(RentalBalance) == 0 THEN '0.00' ELSE SUM(RentalBalance) END AS RentalBalance FROM vRentalInfo WHERE CustomerID=? GROUP BY CustomerID"
    cur.execute(query, (ID,))
    if cur:
        data = cur.fetchall()
        if data == []:
            print("Customer ID %s has not rented any vehicle yet." % ID)
            succ01 = Label(bal_frame1, text="Customer ID " +ID +"has not rented any vehicle yet", bg='grey', font='Helvetica 15 bold')
            succ01.grid(row=4, column=0, columnspan=2)
        else:
            succc1 = Entry(bal_frame1, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succc1.grid(row=4, column=0)
            succc1.insert(END, "Customer ID")

            succ111 = Entry(bal_frame1, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succ111.grid(row=4, column=1)
            succ111.insert(END, "Name")

            succ111 = Entry(bal_frame1, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succ111.grid(row=4, column=2)
            succ111.insert(END, "Remaining Balance")
            i = 5
            for d in data:
                for j in range(len(d)):
                    e = Entry(bal_frame1, width=22, fg='blue', font='Helvetica 12 bold')
                    e.grid(row=i, column=j)
                    if j == 2:
                        if d[j] == 0.00:
                            e.insert(END, "$ 0.00")
                        else:
                            e.insert(END, "$" + str(d[j]))
                    else:
                        e.insert(END, d[j])
                i = i + 1


def ck_name():
    hide_frames()
    bal_frame2.pack(fill="both", expand=1)
    submit_nm = Button(bal_frame2, text="Check", width=5, bg="orange", command=submit_cknm)
    submit_nm.grid(row=2, column=0, columnspan=2, pady=20, padx=100, ipadx=100)

def submit_cknm():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()
    name=cust_name1.get()
    #name = name.capitalize()

    wid = bal_frame2.winfo_children()

    if len(wid) > 3:
        for i in range(4, len(wid)):
            wid[i].destroy()

    query = "SELECT CustomerID, CustomerName, CASE WHEN SUM(RentalBalance) == 0 THEN '0.00' ELSE SUM(RentalBalance) END AS  RentalBalance FROM vRentalInfo WHERE CustomerName=? GROUP BY CustomerID"
    cur.execute(query, (name,))

    if cur:
        prnt_dat = ''
        data = cur.fetchall()
        if data == []:
            succ01 = Label(bal_frame2, text="Customer ID " + name + "has not rented any vehicle yet", bg='grey',
                           font='Helvetica 15 bold')
            succ01.grid(row=3, column=0, columnspan=2)
        else:
            i = 4
            succc1 = Entry(bal_frame2, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succc1.grid(row=3, column=0)
            succc1.insert(END, "Customer ID")

            succ111 = Entry(bal_frame2, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succ111.grid(row=3, column=1)
            succ111.insert(END, "Name")

            succ111 = Entry(bal_frame2, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succ111.grid(row=3, column=2)
            succ111.insert(END, "Remaining Balance")

            for d in data:
                for j in range(len(d)):
                    e = Entry(bal_frame2, width=22, fg='blue', font='Helvetica 12 bold')
                    e.grid(row=i, column=j)
                    if j == 2:
                        if d[j] == 0.00:
                            e.insert(END, "$ 0.00")
                        else:
                            e.insert(END, "$" + str(d[j]))
                    else:
                        e.insert(END, d[j])
                i = i + 1

###################################################################################################
def ck_part():
    hide_frames()
    bal_frame3.pack(fill="both", expand=1)
    submit_bp = Button(bal_frame3, text="Check", width=5, bg="orange", command=submit_prt)
    submit_bp.grid(row=2, column=0, columnspan=2, pady=20, padx=100, ipadx=100)

def submit_prt():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()
    name=cust_npart.get()
    wid = bal_frame3.winfo_children()

    if len(wid) > 3:
        for i in range(4, len(wid)):
            wid[i].destroy()
    query = (
        "SELECT CustomerID, CustomerName, CASE WHEN SUM(RentalBalance) == 0 THEN '0.00' ELSE SUM(RentalBalance) END AS RentalBalance FROM vRentalInfo WHERE CustomerName LIKE ? OR CustomerName LIKE ?")
    cur.execute(query, (name + '%', '%' + name))
    if cur:
        data = cur.fetchall()
        if data == []:
            succ01 = Label(bal_frame3, text="Customer has not rented any vehicle yet", bg='grey', font='Helvetica 15 bold')
            succ01.grid(row=3, column=0, columnspan=2)
        else:
            succc1 = Entry(bal_frame3, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succc1.grid(row=3, column=0)
            succc1.insert(END, "Customer ID")

            succ111 = Entry(bal_frame3, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succ111.grid(row=3, column=1)
            succ111.insert(END, "Name")

            succ111 = Entry(bal_frame3, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
            succ111.grid(row=3, column=2)
            succ111.insert(END, "Remaining Balance")

            i=4
            for d in data:
                for j in range(len(d)):
                    e = Entry(bal_frame3, width=22, fg='blue', font='Helvetica 12 bold')
                    e.grid(row=i, column=j)
                    if j == 2:
                        if d[j] == 0.00:
                            e.insert(END, "$ 0.00")
                        else:
                            e.insert(END, "$" + str(d[j]))
                    else:
                        e.insert(END, d[j])
                i = i + 1


# remaining balance
bal_menu = Menu(my_menu)
my_menu.add_cascade(label="Check Balance", menu=bal_menu)
bal_menu.add_command(label="Check default", command=ck_def)
bal_menu.add_separator()
bal_menu.add_command(label="Check by Customer ID", command=ck_id)
bal_menu.add_separator()
bal_menu.add_command(label="Check by Name", command=ck_name)
bal_menu.add_separator()
bal_menu.add_command(label="Check by part of Name", command=ck_part)

############################################################################################################################################

#frames for searcing vehicles
srch_frame=Frame(root, width=400, height=400, bg="grey")
srch_frame1=Frame(root, width=400, height=400, bg="grey")
srch_frame2=Frame(root, width=400, height=400, bg="grey")
srch_frame3=Frame(root, width=400, height=400, bg="grey")

#entries for handling remaining balances
sr_vin_lab= Label(srch_frame1, text="VIN", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
sr_vin= Entry(srch_frame1, width=50)
sr_vin.grid(row=1, column=1, padx=20, ipady=10)

sr_desc_lab = Label(srch_frame2, text="Description", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
sr_desc= Entry(srch_frame2, width=50)
sr_desc.grid(row=1, column=1, padx=20, ipady=10)

sr_dpart_lab = Label(srch_frame3, text="Part of Description", bg="grey", font='Helvetica 20 bold').grid(row=1, column=0)
sr_dpart= Entry(srch_frame3, width=50)
sr_dpart.grid(row=1, column=1, padx=20, ipady=10)

def srch_def():
    hide_frames()
    srch_frame.pack(fill="both", expand=1)
    query= "Select DISTINCT VIN, Vehicle, CASE WHEN DAILY='null' THEN 'Not Applicable'" \
             "ELSE Daily END AS DAILY  From vRentalInfo, vehicle,rate " \
             "WHERE vRentalInfo.VIN = vehicle.Vehicle_ID AND vehicle.type = rate.type AND " \
             "vehicle.Category = rate.Category ORDER BY DAILY "
    cur.execute(query)
    if cur:
        data = cur.fetchall()
        succc1 = Entry(srch_frame, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succc1.grid(row=1, column=0)
        succc1.insert(END, "VIN")

        succ111 = Entry(srch_frame, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=1, column=1)
        succ111.insert(END, "Description")

        succ111 = Entry(srch_frame, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=1, column=2)
        succ111.insert(END, "Daily Rate")
        i=2
        for d in data:
            for j in range(len(d)):
                e=Entry(srch_frame, width=22,fg='blue',font='Helvetica 12 bold')
                e.grid(row=i,column=j)
                if j==2:
                    if isinstance(d[j],float):
                       e.insert(END, "$" + str(d[j]))
                    elif isinstance(d[j],int):
                        e.insert(END,"$"+str(d[j])+".00")
                else:
                    e.insert(END,d[j])
            i = i+1


    else:
        print('Failed to get the data from the database.')

def srch_vin():
    hide_frames()
    srch_frame1.pack(fill="both", expand=1)
    submit_svin = Button(srch_frame1, text="Search", width=5, bg="orange", command=submit_vinsrch)
    submit_svin.grid(row=2, column=0, columnspan=2, pady=20, padx=100, ipadx=100)

def submit_vinsrch():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()
    vin=sr_vin.get()
    wid = srch_frame1.winfo_children()

    if len(wid) > 3:
        for i in range(4, len(wid)):
            wid[i].destroy()

    query1 = "Select DISTINCT VIN, Vehicle, CASE WHEN DAILY='null' THEN 'Not Applicable' ELSE DAILY" \
             "  END AS DAILY From vRentalInfo, vehicle, rate WHERE " \
             "vRentalinfo.VIN=? AND vRentalInfo.VIN = vehicle.Vehicle_ID AND vehicle.type = rate.type AND " \
             "vehicle.Category = rate.Category ORDER BY DAILY "

    cur.execute(query1, (vin,))
    if cur:
        data = cur.fetchall()
        succc1 = Entry(srch_frame1, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succc1.grid(row=3, column=0)
        succc1.insert(END, "VIN")

        succ111 = Entry(srch_frame1, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=3, column=1)
        succ111.insert(END, "Description")

        succ111 = Entry(srch_frame1, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=3, column=2)
        succ111.insert(END, "Daily Rate")

        i = 4
        for d in data:
            for j in range(len(d)):
                e = Entry(srch_frame1, width=22, fg='blue', font='Helvetica 12 bold')
                e.grid(row=i, column=j)
                if j == 2:
                    if isinstance(d[j],float):
                       e.insert(END, "$" + str(d[j]))
                    elif isinstance(d[j],int):
                        e.insert(END,"$"+str(d[j])+".00")
                else:
                    e.insert(END, d[j])
            i = i + 1

    else:
        print('Failed to get the data from the database.')

def srch_desc():
    hide_frames()
    srch_frame2.pack(fill="both", expand=1)
    submit_sdesc = Button(srch_frame2, text="Search", width=5, bg="orange", command=submit_desrch)
    submit_sdesc.grid(row=2, column=0, columnspan=2, pady=20, padx=100, ipadx=100)


def submit_desrch():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()
    desc = sr_desc.get()

    wid = srch_frame2.winfo_children()

    if len(wid) > 3:
        for i in range(4, len(wid)):
            wid[i].destroy()

    query1 = "Select DISTINCT VIN, Vehicle, CASE WHEN DAILY='null' THEN 'Not Applicable' ELSE DAILY" \
             "  END AS DAILY From vRentalInfo, vehicle, rate WHERE " \
             "vRentalinfo.Vehicle=? AND vRentalInfo.VIN = vehicle.Vehicle_ID AND vehicle.type = rate.type AND " \
             "vehicle.Category = rate.Category  ORDER BY DAILY"

    cur.execute(query1, (desc,))

    if cur:
        data = cur.fetchall()
        succc1 = Entry(srch_frame2, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succc1.grid(row=3, column=0)
        succc1.insert(END, "VIN")

        succ111 = Entry(srch_frame2, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=3, column=1)
        succ111.insert(END, "Description")

        succ111 = Entry(srch_frame2, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=3, column=2)
        succ111.insert(END, "Daily Rate")
        i = 4
        for d in data:
            for j in range(len(d)):
                e = Entry(srch_frame2, width=22, fg='blue', font='Helvetica 12 bold')
                e.grid(row=i, column=j)
                if j == 2:
                    if isinstance(d[j],float):
                       e.insert(END, "$" + str(d[j]))
                    elif isinstance(d[j],int):
                        e.insert(END,"$"+str(d[j])+".00")
                else:
                    e.insert(END, d[j])
            i = i + 1
    else:
        print('Failed to get the data from the database.')

def srch_dpart():
    hide_frames()
    srch_frame3.grid_forget()
    srch_frame3.pack(fill="both", expand=1)
    submit_sdesc1 = Button(srch_frame3, text="Search", width=5, bg="orange", command=submit_desrch1)
    submit_sdesc1.grid(row=2, column=0, columnspan=2, pady=20, padx=100, ipadx=100)




def submit_desrch1():
    mdb = db.connect("car_rental.db")
    cur = mdb.cursor()
    prt = sr_dpart.get()

    wid= srch_frame3.winfo_children()

    if len(wid)>3:
        for i in range (4,len(wid)):
            wid[i].destroy()


    query1 = "Select DISTINCT VIN, Vehicle, CASE WHEN DAILY='null' THEN 'Not Applicable' ELSE DAILY " \
             "  END AS DAILY From vRentalInfo, vehicle, rate " \
             "WHERE (vRentalinfo.Vehicle LIKE ? OR vRentalinfo.Vehicle LIKE ?) " \
             "AND vRentalInfo.VIN = vehicle.Vehicle_ID AND vehicle.type = rate.type AND vehicle.Category = " \
             "rate.Category ORDER BY DAILY"

    cur.execute(query1, ('%' + prt, prt + '%'))

    if cur:
        data = cur.fetchall()
        succc1 = Entry(srch_frame3, width=22, fg='blue',bg='yellow', font='Helvetica 12 bold')
        succc1.grid(row=3, column=0)
        succc1.insert(END, "VIN")

        succ111 = Entry(srch_frame3, width=22, fg='blue',bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=3, column=1)
        succ111.insert(END, "Description")

        succ111 = Entry(srch_frame3, width=22, fg='blue', bg='yellow', font='Helvetica 12 bold')
        succ111.grid(row=3, column=2)
        succ111.insert(END, "Daily Rate")



        i = 4
        for d in data:
            for j in range(len(d)):
                e = Entry(srch_frame3, width=22, fg='blue', font='Helvetica 12 bold')
                e.grid(row=i, column=j)
                if j == 2:
                    if isinstance(d[j],float):
                       e.insert(END, "$" + str(d[j]))
                    elif isinstance(d[j],int):
                        e.insert(END,"$"+str(d[j])+".00")
                else:
                    e.insert(END, d[j])
            i = i + 1


    else:
        print('Failed to get the data from the database.')





# Search vehicles
srch_menu = Menu(my_menu)
my_menu.add_cascade(label="Search Vehicles", menu=srch_menu)
srch_menu.add_command(label="Search default", command=srch_def)
srch_menu.add_separator()
srch_menu.add_command(label="Search by VIN", command=srch_vin)
srch_menu.add_separator()
srch_menu.add_command(label="Search by Description", command=srch_desc)
srch_menu.add_separator()
srch_menu.add_command(label="Search by part of Description", command=srch_dpart)

# frames


root.mainloop()
