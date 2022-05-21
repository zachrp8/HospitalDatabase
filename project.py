from tkinter import *
from tkinter import ttk

import sqlite3
with sqlite3.connect('project.db') as db:
    cursor=db.cursor()



root = Tk()
root.title("Hospital Database")
photo=PhotoImage(file = "hopsital.png")
root.iconphoto(False, photo)
frame=Frame(root)
frame.pack()
botFrame = Frame(root)

def deleteExtra(name):
    temp=""
    for n in name:
        if not(n=='(' or n=='\'' or n==',' or n==')'):
            temp+=n
    return temp
def tupleToArray(arr1, number):
    y=0
    for n in number: #changing the count from tuple to int to use when creating the new array
        if not(n=='(' or n==',' or n==')'):
            y=n
    newArr = [""]*y
    j=0
    for i in arr1: #goes through array of tuples
        for n in i: #goes through each tuple
            if not(n=='(' or n==',' or n==')'):
                newArr[j]=n
                j+=1
    return newArr            
def strToDate(date):
    if len(date)==7:
        iter=0
        newDate=""
        for i in date:
            if (iter==1) or (iter==3):
                newDate+="/"
            newDate+=i
            iter+=1
        return newDate
    elif len(date)==8:
        iter=0
        newDate=""
        for i in date:
            if (iter==2) or (iter==4):
                newDate+="/"
            newDate+=i    
            iter+=1  
        return newDate

def getUserName(idnumber):
    cursor.execute("SELECT f_name FROM employee WHERE emp_id = ?", idnumber)
    name=str(cursor.fetchone())
    db.commit()
    newName=deleteExtra(name)
    return newName

def getPatientInfo(idnumber):
    cursor.execute("SELECT patient_id FROM treat_plan WHERE emp_id = ?", idnumber)
    arr=cursor.fetchall()
    db.commit()
    cursor.execute("SELECT COUNT(treat_id) FROM treat_plan WHERE emp_id = ?", idnumber)
    x=cursor.fetchone()
    db.commit()
    
    newArr=tupleToArray(arr, x)
   
    #destroy the previous frame
    for widget in frame.winfo_children():
        widget.grid_remove()
    #creates the treeview
    tree=ttk.Treeview(frame)
    tree['columns'] = ("ID", "FN", "LN", "Ailment")
    tree.column("#0", width=1, minwidth=0)
    tree.column("ID", anchor=CENTER, width=10)
    tree.column("FN", anchor=W)
    tree.column("LN", anchor=W)
    tree.column("Ailment", anchor=W)
    tree.heading("#0", text="Label", anchor=W)
    tree.heading("ID", text="ID", anchor=CENTER)
    tree.heading("FN", text="First Name", anchor=W)
    tree.heading("LN", text="Last Name", anchor=W)
    tree.heading("Ailment", text="Ailment", anchor=W)


    button4 = Button(frame, text="Press to enter Patient Info", command=enterPatientInfo)
    button4.grid(row=0, column=0, pady=10)
    button6 = Button(frame, text="Access Patient Info", command=viewPatientData)
    button6.grid(row=0, column=1, pady=10)
    backButton.grid(row=0, column=3, pady=10)
    iter=0
    for i in newArr:
        x=str(i)
        cursor.execute("SELECT f_name FROM patient WHERE patient_id = ?", (x,))
        f_name=cursor.fetchone()
        db.commit()
        f_name=deleteExtra(f_name)

        cursor.execute("SELECT l_name FROM patient WHERE patient_id = ?", (x,))
        l_name=cursor.fetchone()
        db.commit()
        l_name=deleteExtra(l_name)

        cursor.execute("SELECT ailment FROM treat_plan WHERE patient_id = ? AND emp_id = ?", (x, idnumber,))
        ailment=cursor.fetchone()
        db.commit()
        ailment=deleteExtra(ailment) #all data for a single tuple
        
        tree.insert(parent='', index='end', iid=iter, text='Parent',values=(x, f_name, l_name, ailment))
        iter+=1
    tree.grid(row=1, column=0, columnspan=3)
#enter new patient info    
def enterPatientInfo():
    for widget in botFrame.winfo_children():
        widget.grid_remove()

    botFrame.pack(side=BOTTOM)
    
    button2.grid(row=0,column=7)

    label3 = Label(botFrame, text="Enter new info: ")
    label3.grid(row=0, column=0)
    #bring the entries to the frame
    entry2.grid(row=0, columnspan=2, column=1)
    entry3.grid(row=0, columnspan=2, column=3)
    entry4.grid(row=0, columnspan=2, column=5)

    button3.grid(row=1, column=0)
    backButton.grid(row=0, column=4)
def viewPatientData():
    for widget in botFrame.winfo_children():
        widget.grid_remove()
    botFrame.pack(side=BOTTOM)

    entry5 = Entry(botFrame, width=25)
    entry5.grid(row=0,column=1, pady=10)
    label5 = Label(botFrame, text="Enter the Patient's ID")
    label5.grid(row=0, column=0, pady=10)
    button7 = Button(botFrame, text="Access", command=lambda:accessData(entry5.get()))
    button7.grid(row=0, column=2, pady=10)

def accessData(x):
    for widget in botFrame.winfo_children():
        widget.grid_remove()
    botFrame.pack(side=BOTTOM)

    label6 = Label(botFrame, text="Choose the data to view")
    label6.grid(row=0, column=0)
    accButton1 = Button(botFrame, text="Appointments", command=lambda:appt(x))
    accButton2 = Button(botFrame, text="Contact Info", command=lambda:contact(x))
    accButton3 = Button(botFrame, text="Room Info", command=lambda:room(x))
    accButton4 = Button(botFrame, text="Payment Data", command=lambda:payment(x))
    accButton1.grid(row=0, column=1)
    accButton2.grid(row=0, column=2)
    accButton3.grid(row=0, column=3)
    accButton4.grid(row=0, column=4)

def appt(a):
    for widget in frame.winfo_children():
        widget.grid_remove()
    cursor.execute("SELECT appt_number FROM appointment WHERE patient_id = ?", (a,))
    appointID=cursor.fetchall()
    cursor.execute("SELECT COUNT(appt_number) FROM appointment WHERE patient_id = ?", (a,))
    x=cursor.fetchone()
    db.commit()
    newArr = tupleToArray(appointID, x)

    apptTree=ttk.Treeview(frame)
    apptTree['columns'] = ("Patient Name", "Employee Name", "Date")
    apptTree.column("#0", width=1, minwidth=0)
    apptTree.column("Patient Name", anchor=W)
    apptTree.column("Employee Name", anchor=W)
    apptTree.column("Date", anchor=W)
    apptTree.heading("#0", text="Label", anchor=W)
    apptTree.heading("Patient Name", text="Patient Name", anchor=W)
    apptTree.heading("Employee Name", text="Employee Name", anchor=W)
    apptTree.heading("Date", text="Date", anchor=W)

    backButton.grid(row=0, column=4, pady=10)
    addAppt=Button(frame, text="Add Appointments", command=lambda:addAppointment(a))
    addAppt.grid(row=0,column=3)
    iter=0
    for i in newArr:
        x=str(i)
        #get patient name
        cursor.execute("SELECT patient_id FROM appointment WHERE appt_number= ?", (x,))
        patient=str(cursor.fetchone())
        db.commit()
        patient=deleteExtra(patient)
        cursor.execute("SELECT f_name FROM patient WHERE patient_id = ?", (patient,))
        f_name=str(cursor.fetchone())
        db.commit()
        f_name=deleteExtra(f_name)
        cursor.execute("SELECT l_name FROM patient WHERE patient_id = ?", (patient,))
        l_name=str(cursor.fetchone())
        db.commit()
        l_name=deleteExtra(l_name)
        p_name=f_name + " " + l_name
        

        #get employee name
        cursor.execute("SELECT emp_id FROM appointment WHERE appt_number=?", (x,))
        emp=str(cursor.fetchone())
        db.commit()
        emp=deleteExtra(emp) 
        cursor.execute("SELECT f_name from employee WHERE emp_id = ?", (emp,))
        f_name=str(cursor.fetchone())
        db.commit()
        f_name=deleteExtra(f_name)
        cursor.execute("SELECT l_name from employee WHERE emp_id = ?", (emp,))
        l_name=str(cursor.fetchone())
        db.commit()
        l_name=deleteExtra(l_name)
        emp_name= f_name + " " + l_name
        

        cursor.execute("SELECT date FROM appointment WHERE appt_number = ?", (x,))
        date=str(cursor.fetchone())
        db.commit()
        date=deleteExtra(date)
        newDate=strToDate(date)
        

        apptTree.insert(parent='', index='end', iid=iter, text='Parent',values=(p_name, emp_name, newDate))
        iter+=1
    apptTree.grid(row=1, column=0, columnspan=3)

def addAppointment(pat):
    apptLabel1 = Label(frame, text="Enter the date (For example: 4/26/2022 would be 4262022")
    apptLabel1.grid(row=0, column=0)
    apptEntry1.grid(row=0, column=1)
    apptButton1 = Button(frame, text="Enter", command=lambda:enter3(pat))
    apptButton1.grid(row=0, column=2)

def contact(a):
    for widget in frame.winfo_children():
        widget.grid_remove()
    cursor.execute("SELECT f_name FROM patient WHERE patient_id = ?", (a,))
    f_name=str(cursor.fetchone())
    db.commit()
    f_name=deleteExtra(f_name)
    cursor.execute("SELECT l_name FROM patient WHERE patient_id = ?", (a,))
    l_name=str(cursor.fetchone())
    db.commit()
    l_name=deleteExtra(l_name)
    p_name=f_name + " " + l_name
    
    cursor.execute("SELECT email FROM patient WHERE patient_id = ?", (a,)) 
    email=str(cursor.fetchone())
    db.commit()
    email=deleteExtra(email)

    cursor.execute("SELECT phone FROM patient WHERE patient_id = ?", (a,))
    phone=str(cursor.fetchone())
    db.commit()
    phone=deleteExtra(phone)

    cursor.execute("SELECT address FROM patient WHERE patient_id = ?", (a,))
    address=str(cursor.fetchone())
    db.commit()
    address=deleteExtra(address)

    cursor.execute("SELECT dob FROM patient WHERE patient_id = ?", (a,))
    dob=str(cursor.fetchone())
    db.commit()
    dob=deleteExtra(dob)
    dob=strToDate(dob)

    cursor.execute("SELECT age FROM patient WHERE patient_id = ?", (a,))
    age=str(cursor.fetchone())
    db.commit()
    age=deleteExtra(age)

    contactTree=ttk.Treeview(frame)
    contactTree['columns'] = ("p_name", "email", "phone", "address", "dob", "age")
    contactTree.column("#0", width=1, minwidth=0)
    contactTree.column("p_name", anchor=W)
    contactTree.column("email", anchor=W)
    contactTree.column("phone", anchor=W)
    contactTree.column("address", anchor=W)
    contactTree.column("dob", anchor=W)
    contactTree.column("age", anchor=W)
    contactTree.heading("#0", text="Label", anchor=W)
    contactTree.heading("p_name", text= "Patient Name", anchor=W)
    contactTree.heading("email", text= "Email Address", anchor=W)
    contactTree.heading("phone", text= "Phone Number", anchor=W)
    contactTree.heading("address", text= "Address", anchor=W)
    contactTree.heading("dob", text= "Date of Birth", anchor=W)
    contactTree.heading("age", text= "Age", anchor=W)

    backButton.grid(row=0, column=4, pady=10)
    addCon=Button(frame, text="Update Contact", command=lambda:addContact(a, p_name))
    addCon.grid(row=0,column=3)
    
    contactTree.insert(parent='', index='end', iid=iter, text='Parent',values=(p_name, email, phone, address, dob, age))
    contactTree.grid(row=1, column=0, columnspan=3)

def addContact(a, p_name):
    for widget in frame.winfo_children():
        widget.grid_remove()
    backButton.grid(row=0, column=7)
    contactLabel1 = Label(frame, text="Patient Name")
    contactLabel2 = Label(frame, text="Email Address")
    contactLabel3 = Label(frame, text="Phone Number")
    contactLabel4 = Label(frame, text="Address")
    contactLabel5 = Label(frame, text="Date of Birth")
    contactLabel6 = Label(frame, text="Age")
    contactLabel1.grid(row=0, column=1)
    contactLabel2.grid(row=0, column=2)
    contactLabel3.grid(row=0, column=3)
    contactLabel4.grid(row=0, column=4)
    contactLabel5.grid(row=0, column=5)
    contactLabel6.grid(row=0, column=6)
    contactLabel7 = Label(frame, padx=10, text="(For example: 4/26/2022 would be 4262022)", wraplength=100)
    contactLabel7.grid(row=1, column=0)
    contactLabel8 = Label(frame, text=p_name, relief=RAISED)
    contactLabel8.grid(row=1, column=1)

    contactEntry1.grid(row=1, column=2)
    contactEntry2.grid(row=1, column=3)
    contactEntry3.grid(row=1, column=4)
    contactEntry4.grid(row=1, column=5)
    contactEntry5.grid(row=1, column=6)
    contactButton1 = Button(frame, text="Enter", command=lambda:enter4(a), padx=10)
    contactButton1.grid(row=1, column=7)

def room(a):
    for widget in frame.winfo_children():
        widget.grid_remove()
    cursor.execute("SELECT f_name FROM patient WHERE patient_id = ?", (a,))
    f_name=str(cursor.fetchone())
    db.commit()
    f_name=deleteExtra(f_name)
    cursor.execute("SELECT l_name FROM patient WHERE patient_id = ?", (a,))
    l_name=str(cursor.fetchone())
    db.commit()
    l_name=deleteExtra(l_name)
    p_name=f_name + " " + l_name

    cursor.execute("SELECT room_number FROM patient_room WHERE patient_id = ?", (a,))
    roomNum=cursor.fetchall()
    cursor.execute("SELECT COUNT(room_number) FROM patient_room WHERE patient_id = ?", (a,))
    x=cursor.fetchone()
    db.commit()
    newArr=tupleToArray(roomNum, x)
    
    roomTree=ttk.Treeview(frame)
    roomTree['columns'] = ("Patient Name", "Room", "Floor Number", "desc")
    roomTree.column("#0", width=1, minwidth=0)
    roomTree.column("Patient Name", anchor=W)
    roomTree.column("Room", anchor=W)
    roomTree.column("Floor Number", anchor=W)
    roomTree.column("desc", anchor=W)
    roomTree.heading("#0", text="Label", anchor=W)
    roomTree.heading("Patient Name", text="Patient Name", anchor=W)
    roomTree.heading("Room", text="Room Number", anchor=W)
    roomTree.heading("Floor Number", text="Floor Number", anchor=W)
    roomTree.heading("desc", text="Room Description", anchor=W)

    backButton.grid(row=0, column=4, pady=10)
    addR=Button(frame, text="Add patient to room", command=lambda:addRoom(a))
    addR.grid(row=0,column=3)
    
    iter=0
    for i in newArr:
        strRoomNum=deleteExtra(i)
        cursor.execute("SELECT floor_number FROM room WHERE room_number = ?", (i,))
        floor=str(cursor.fetchone())
        db.commit()
        floor=deleteExtra(floor)

        cursor.execute("SELECT description FROM room WHERE room_number = ?", (i,))
        desc=str(cursor.fetchone())
        db.commit()
        desc=deleteExtra(desc)
        roomTree.insert(parent='', index='end', iid=iter, text='Parent',values=(p_name, strRoomNum, floor, desc))
    roomTree.grid(row=1, column=0, columnspan=3)
    
def addRoom(a): 
    roomLabel1 = Label(frame, text="Enter the room number")
    roomLabel1.grid(row=2, column=0, columnspan=2)
    roomEntry1.grid(row=3, column=1)
    
    roomButton1 = Button(frame, text="Enter", command=lambda:enter5(a), pady=5)
    roomButton1.grid(row=3, column=2)
    
def payment(a):
    for widget in frame.winfo_children():
        widget.grid_remove()
    cursor.execute("SELECT payment_id FROM patient_pay WHERE patient_id = ?", (a,))
    pay=cursor.fetchall()
    db.commit()
    cursor.execute("SELECT count(payment_id) FROM patient_pay WHERE patient_id = ?", (a,))
    x=cursor.fetchone()
    pay=tupleToArray(pay,x)
    
    payTree=ttk.Treeview(frame)
    payTree['columns'] = ("payment", "method", "insurance")
    payTree.column("#0", width=1, minwidth=0)
    payTree.column("payment", anchor=W)
    payTree.column("method", anchor=W)
    payTree.column("insurance", anchor=W)
    payTree.heading("#0", text="Label", anchor=W)
    payTree.heading("payment", text="Payment ID", anchor=W)
    payTree.heading("method", text="Payment Type", anchor=W)
    payTree.heading("insurance", text="Insurance Number", anchor=W)
    
    backButton.grid(row=0, column=4, pady=10)
    addPay=Button(frame, text="Add Payment Method", command=lambda:addPayment(a))
    addPay.grid(row=0,column=3)

    for i in pay:
        x=str(i)
        cursor.execute("SELECT method FROM payment_data WHERE payment_id = ?",(x,))
        method=str(cursor.fetchone())
        db.commit()
        method=deleteExtra(method)
        cursor.execute("SELECT insurance_number FROM payment_data WHERE payment_id = ?",(x,))
        insurNum=str(cursor.fetchone())
        db.commit()
        insurNum=deleteExtra(insurNum)

        payTree.insert(parent='', index='end', iid=iter, text='Parent',values=(i, method, insurNum))
    payTree.grid(row=1, column=0, columnspan=3)

def addPayment(a):
    payLabel1 = Label(frame, text="Enter your method and insurance number")
    payLabel1.grid(row=2, column=0, columnspan=2)
    payEntry1.grid(row=3, column=0)
    payEntry2.grid(row=3, column=1)

    payButton1 = Button(frame, text="Enter", command=lambda:enter6(a))
    payButton1.grid(row=3, column=2)

def enter():
    global val
    val=entry1.get()
    getPatientInfo(val)
    entry1.delete(0, END)

def enter2():
    f_name=str(entry2.get())
    l_name=str(entry3.get())
    ailment=str(entry4.get())
    entry2.delete(0,END)
    entry3.delete(0,END)
    entry4.delete(0,END)

    label4 = Label(botFrame, text="Succesful input")
    cursor.execute("SELECT COUNT(treat_id) FROM treat_plan WHERE emp_id = ?", val)
    x=cursor.fetchone()
    db.commit()
    y=0
    for n in x: #changing the count from tuple to int to use when creating the new array
        if not(n=='(' or n==',' or n==')'):
            y=n
    #inserting values into the patient table        
    cursor.execute(""" 
    INSERT INTO patient(f_name, l_name)
    Values(?,?)
    """, (f_name, l_name))
    #cursor.execute("""  #attempt to make a trigger
     #   CREATE TRIGGER update_treat_plan
      #      AFTER UPDATE ON patient
       #     WHEN old.f_name <> new.f_name
        #        OR old.l_name <> new.l_name
        #BEGIN
         #       INSERT INTO treat_plan(
          #          "emp_id",
           #         "patient_id",
            #        "ailment"
             #   )
      #  VALUES (
       #             ?, (SELECT max(patient_id) from patient), ?
        #)
        #""", (val, ailment))
    cursor.execute("SELECT max(patient_id) FROM patient")
    p_id = str(cursor.fetchone())
    db.commit()
    p_id=deleteExtra(p_id)
    cursor.execute("""
    INSERT INTO treat_plan(emp_id, patient_id, ailment)
    VALUES(?,?,?)
    """, (val, p_id, ailment))
    db.commit()
    cursor.execute("SELECT COUNT(treat_id) FROM treat_plan WHERE emp_id = ?", val)
    x=cursor.fetchone()
    db.commit()
    newY=0
    for n in x: #changing the count from tuple to int to use when creating the new array
        if not(n=='(' or n==',' or n==')'):
            newY=n
    if y<newY:
        label4.pack()

def enter3(pat):
    date=str(apptEntry1.get())
    apptEntry1.delete(0,END)
    
    #inserting values into the patient table        
    cursor.execute(""" 
    INSERT INTO appointment(patient_id, emp_id, date)
    VALUES(?,?,?)
    """, (pat, val, date))
    db.commit()

def enter4(a):
    #get all the data from the entry fields
    email=str(contactEntry1.get())    
    contactEntry1.delete(0, END)
    phone=str(contactEntry2.get())
    contactEntry2.delete(0, END)
    address=str(contactEntry3.get())
    contactEntry3.delete(0, END)
    dob=str(contactEntry4.get())
    contactEntry4.delete(0, END)
    age=str(contactEntry5.get())
    contactEntry5.delete(0, END)

    cursor.execute(""" 
    UPDATE patient
    set email = ?, 
    phone = ?,
    address = ?,
    dob = ?, 
    age = ?
    WHERE patient_id = ?
    """, (email, phone, address, dob, age, a))
    db.commit()
    
def enter5(a):
    room=str(roomEntry1.get())
    roomEntry1.delete(0, END)
    
    cursor.execute("""
    INSERT INTO patient_room(patient_id, room_number)
    VALUES(?,?)
    """, (a, room))    
    db.commit()


def enter6(a):
    method=str(payEntry1.get())
    payEntry1.delete(0, END)
    insur=str(payEntry2.get())
    payEntry2.delete(0, END)

    cursor.execute("""
    INSERT INTO payment_data(method, insurance_number)
    VALUES(?,?)
    """, (method, insur))
    db.commit()
    cursor.execute("SELECT max(payment_id) FROM payment_data")
    payment=str(cursor.fetchone())
    db.commit()
    payment=deleteExtra(payment)
    cursor.execute("INSERT INTO patient_pay(payment_id, patient_id) VALUES(?,?)", (payment, a))
    db.commit()

def back():
    for widget in botFrame.winfo_children():
        widget.grid_remove()
    for widget in frame.winfo_children():
        widget.grid_remove()
    botFrame.grid_remove()
    label1.grid(row=0, column=0)
    entry1.grid(row=0, column=1)
    button1.grid(row=0, column=2)
    
label1 = Label(frame, text="Enter your ID:")
label1.grid(row=0, column=0)
    
entry1 = Entry(frame, width=50)
entry1.grid(row=0, column=1)

button1 = Button(frame, text="Enter", command=enter)
button1.grid(row=0, column=2)

button2 = Button(botFrame, text="Enter", command=enter2)
button3 = Button(botFrame, text="Get Patient Info", command=lambda: getPatientInfo(val))
backButton = Button(frame, text="Back", command=back, padx=10)

entry2 = Entry(botFrame, text="First Name", width =30,)
entry3 = Entry(botFrame, text="Last Name", width =30)
entry4 = Entry(botFrame, text="Ailment", width =30)
apptEntry1 = Entry(frame, width=30)
contactEntry1 = Entry(frame, width=40)
contactEntry2 = Entry(frame, width=20)
contactEntry3 = Entry(frame, width=40)
contactEntry4 = Entry(frame, width=10)
contactEntry5 = Entry(frame, width=5)
roomEntry1 = Entry(frame, width=5)
payEntry1 = Entry(frame, width=10)
payEntry2 = Entry(frame, width=10)

root.mainloop()