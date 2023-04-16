from foodmodule import *
from viewmodule import *
from employeemodule import *
from customermodule import *
from orderfoodmodule import *
from bill import *
import mysql.connector
from tabulate import *
import platform
import os
import PySimpleGUI as sg



mydb = mysql.connector.connect(
    host="sql12.freemysqlhosting.net",
    user="sql12612684",
    password="fwX87sAhRW",
    database="sql12612684"
)
mycursor=mydb.cursor()

def open_bill_window():

        layout = [
            [sg.Text('Enter order ID to be searched: '), sg.Input(key='order_id')],
            [sg.Button('Search'), sg.Button('Exit')],
            [sg.Table(values=[], headings=['Food Items'], key='food_items',font=('Arial', 14), justification='center')],
            [sg.Table(values=[], headings=['Price', 'Date', 'Customer ID', 'Employee ID'], key='order_info',font=('Arial', 14), justification='center')]
        ]


        window = sg.Window('Order Search', layout, )

        while True:
            event, values = window.read()


            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break


            if event == 'Search':
                order_id = int(values['order_id'])


                sql1 = 'SELECT GROUP_CONCAT(fooditem) FROM bill GROUP BY orderid HAVING orderid=%s'
                val1 = (order_id,)
                mycursor.execute(sql1, val1)
                food_items = mycursor.fetchall()


                window['food_items'].update(values=food_items)


                sql2 = 'SELECT Total_price, date, c_id, emp_id FROM orderfood WHERE orderid=%s'
                val2 = (order_id,)
                mycursor.execute(sql2, val2)
                order_info = mycursor.fetchall()


                window['order_info'].update(values=order_info)


        window.close()

def open_food_window():
    font = ('Axial', 18)
    layout = [[sg.Text("Enter 1 : To Add to Food Menu", font=font, size=(25, 1))],
                [sg.Text('_'*50, text_color='white')],
              [sg.Text("Enter 2 : To Add Food Order Details", font=font, size=(25, 1))],
              [sg.Text('_'*50, text_color='white')],
              [sg.Text("Enter 3 : To View Food Menu", font=font, size=(25, 1))],
              [sg.Text('_'*50, text_color='white')],
              [sg.Text("Enter 4 : To View Food Orders", font=font, size=(25, 1))],
              [sg.Text('_'*50, text_color='white')],
              [sg.Text("Enter 5 : To Update Food Menu", font=font, size=(25, 1))],
              [sg.Text('_'*50, text_color='white')],
              [sg.Text("Enter 6 : To Delete Items from Food Menu", font=font, size=(32, 1))],
              [sg.Text('_'*50, text_color='white')],
              [sg.InputText(font=font, size=(30, 1))],
              [sg.Button('Ok', font=font, size=(10, 1)), sg.Button('Cancel', font=font, size=(10, 1))]
              ]
    food_window = sg.Window("Second Window", layout)

    while True:
        event, values = food_window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
            
        if(event =='Ok' and values[0]=='1'):
            Food()
        if(event=='Ok' and values[0]=='2'):
            OrderFood()
        if(event=='Ok' and values[0]=='3'):
            mycursor.execute('select * from food')
            myresult = mycursor.fetchall()
            toprow = ['FoodID', 'FoodName', 'FoodPrice']
            tbl1 = sg.Table(values=myresult, headings=toprow,
            auto_size_columns=True,
            display_row_numbers=False,
            justification='center', key='-TABLE-',
            selected_row_colors='red on yellow',
            enable_events=True,
            expand_x=True,
            expand_y=True,
            enable_click_events=True)
            layout = [[tbl1]]
            window = sg.Window("Table Demo", layout, size=(715, 200), resizable=True)
            while True:
                event, values = window.read()
                print("event:", event, "values:", values)
                if event == sg.WIN_CLOSED:
                    break
        if(event=='Ok' and values[0]=='4'):
            mycursor.execute('select * from orderfood')
            myresult = mycursor.fetchall()
            toprow = ['OrderID', 'TotalPrice', 'Date', 'CustID', 'EmpID']
            tbl1 = sg.Table(values=myresult, headings=toprow,
            auto_size_columns=True,
            display_row_numbers=False,
            justification='center', key='-TABLE-',
            selected_row_colors='red on yellow',
            enable_events=True,
            expand_x=True,
            expand_y=True,
            enable_click_events=True)
            layout = [[tbl1]]
            window = sg.Window("Table Demo", layout, size=(715, 200), resizable=True)
            while True:
                event, values = window.read()
                print("event:", event, "values:", values)
                if event == sg.WIN_CLOSED:
                    break

                
        if(event=='Ok' and values[0]=='5'):
            layout = [
                    [sg.Text('Enter Food ID:'), sg.Input(key='foodid')],
                    [sg.Text('Enter 1 for Name')],
                    [sg.Text('Enter 2 for Price')],
                    [sg.Text('Enter Choice:'), sg.Input(key='choice')],
                    [sg.Button('Update')],
                    [sg.Output(size=(60, 10))],
                    ]

            window = sg.Window('Food Details').Layout(layout)

            while True:
                event, values = window.Read()
                if event is None:
                    break

                empid = int(values['foodid'])
                choice = int(values['choice'])

                if choice == 1:
                    n = sg.PopupGetText('Enter New Name:')
                    s = "update food set Foodname=%s where Food_id=%s;"
                    val = (n, empid)
                    mycursor.execute(s, val)
                    mydb.commit()

                elif choice == 2:
                    n = sg.PopupGetText('Enter New Price:')
                    s = "update food set price=%s where Food_id=%s;"
                    val = (n, empid)
                    mycursor.execute(s, val)
                    mydb.commit()

                else:
                    print("entered wrong choice")

                a = sg.PopupYesNo('Do you want to update more data?')
                if a == 'No':
                    sg.popup('Food Item updated successfully')
                    break
                else:
                    s = "select * from food where Food_id=%s"
                    val = [empid]
                    print("Updated Food Details are:")
                    mycursor.execute(s, val)
                    res = mycursor.fetchall()
                    print(res)

            window.close()
            
            
        if(event=='Ok' and values[0]=='6'):
            layout = [
                [sg.Text("Enter food id which is to be deleted:")],
                [sg.InputText(key="food_id")],
                [sg.Button("Delete")],
                [sg.Text("", key="result")],
                [sg.Text("Do you want to delete more data?"), sg.Radio("Yes", "delete_more", key="yes"), sg.Radio("No", "delete_more", default=True, key="no")],
                [sg.Button("Exit")]
            ]


            window = sg.Window("Delete Food", layout)


            while True:
                event, values = window.read()


                if event == sg.WINDOW_CLOSED or event == "Exit":
                    break


                if event == "Delete":
                    fid = int(values["food_id"])
                    sql = 'delete from food where Food_id=%s'
                    val = [fid]
                    mycursor.execute(sql, val)
                    mydb.commit()
                    window["result"].update("Record deleted")


                if values["yes"]:
                    continue
                else:
                    break


            window.close()
    food_window.close()

def open_cust_window():
    font = ('Axial', 18)
    layout = [[sg.Text("Enter 1 : To Add Customers", font=font, size=(25, 1))],
                [sg.Text('_'*50, text_color='white')],
              [sg.Text("Enter 2 : To Display Customers", font=font, size=(25, 1))],
              [sg.Text('_'*50, text_color='white')],
              [sg.Text("Enter 3 : To Update Customers", font=font, size=(25, 1))],
              [sg.Text('_'*50, text_color='white')],
              [sg.Text("Enter 4 : To Delete Customers", font=font, size=(25, 1))],
              [sg.Text('_'*50, text_color='white')],
              [sg.InputText(font=font, size=(30, 1))],
              [sg.Button('Ok', font=font, size=(10, 1)), sg.Button('Cancel', font=font, size=(10, 1))]
              ]
    cust_window = sg.Window("Second Window", layout)
    while True:
        event, values = cust_window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if(event =='Ok' and values[0]=='1'):
            Customer()
        if (event=='Ok' and values[0]=='2'):
            mycursor.execute('select * from customer')
            myresult = mycursor.fetchall()
            toprow = ['CustID', 'Name', 'PhoneNo', 'PaymentType', 'Email', 'Date']
            tbl1 = sg.Table(values=myresult, headings=toprow,
                            auto_size_columns=True,
                            display_row_numbers=False,
                            justification='center', key='-TABLE-',
                            selected_row_colors=('red', 'yellow'),
                            enable_events=True,
                            expand_x=True,
                            expand_y=True,
                            enable_click_events=True,
                            font=('Helvetica', 14))
            layout = [[tbl1]]
            window = sg.Window("Table Demo", layout, size=(1000, 500), resizable=True)
            while True:
                event, values = window.read()
                print("event:", event, "values:", values)
                if event == sg.WIN_CLOSED:
                    break
        
        if(event == 'Ok' and values[0]=='3'):
            layout = [
                    [sg.Text("Enter customer id to be updated:"), sg.Input(key="-CID-")],
                    [sg.Text("Enter choice:"), sg.Radio("Customer name", "RADIO1", key="-NAME-"), sg.Radio("Phone number", "RADIO1", key="-PHONE-"), sg.Radio("Email ID", "RADIO1", key="-EMAIL-")],
                    [sg.Text("New value:"), sg.Input(key="-NEWVAL-")],
                    [sg.Button("Update"), sg.Button("Quit")]
                    ]


            window = sg.Window("Customer Database Update", layout)


            while True:
                event, values = window.read()
                if event == "Quit" or event == sg.WIN_CLOSED:
                    break
                elif event == "Update":
                    cid = int(values["-CID-"])
                    if values["-NAME-"]:
                        s = "update customer set name=%s where c_id=%s"
                        val = (values["-NEWVAL-"], cid)
                    elif values["-PHONE-"]:
                        s = "update customer set cphone=%s where c_id=%s"
                        val = (int(values["-NEWVAL-"]), cid)
                    elif values["-EMAIL-"]:
                        s = "update customer set email=%s where c_id=%s"
                        val = (values["-NEWVAL-"], cid)
                    else:
                        sg.popup("Entered wrong choice")
                        continue
                    
                    mycursor.execute(s, val)
                    mydb.commit()
                    
                    sg.popup("Customer details updated")
                    
                    a = sg.popup_yes_no("Do you want to update more data?")
                    if a == "No":
                        break


            window.close()
            
        if(event == 'Ok' and values[0]=='4'):
            layout = [
                [sg.Text('Enter customer ID which is to be deleted:'), sg.Input(key='cid')],
                [sg.Button('Delete'), sg.Button('Exit')],
                [sg.Output(size=(60, 10))]
            ]


            window = sg.Window('Customer Data Deletion', layout)


            while True:
                event, values = window.read()


                if event == sg.WIN_CLOSED or event == 'Exit':
                    break


                if event == 'Delete':
                    try:
                        cid = int(values['cid'])


                        sql = 'delete from customer where c_id=%s'
                        val = [cid]
                        mycursor.execute(sql, val)
                        mydb.commit()


                        print('Record deleted.')

                    except Exception as e:

                        print(f'Error: {str(e)}')

                # ask the user if they want to delete more data
                a = sg.popup_yes_no('Do you want to delete more data?')
                if a.lower() == 'no':
                    break


            window.close()
            
    cust_window.close()
            

def open_emp_window():
    font = ('Axial', 18)
    layout = [[sg.Text('Enter 1: To Add Employee', font=font, size=(25, 1))],
          [sg.Text('_'*50, text_color='white')],
          [sg.Text('Enter 2: To Display Employee', font=font, size=(25, 1))],
          [sg.Text('_'*50, text_color='white')],
          [sg.Text('Enter 3: To Update Employee', font=font, size=(25, 1))],
          [sg.Text('_'*50, text_color='white')],
          [sg.Text('Enter 4: To Delete Employee', font=font, size=(25, 1))],
          [sg.Text('_'*50, text_color='white')],
          [sg.InputText(font=font, size=(30, 1))],
          [sg.Button('Ok', font=font, size=(10, 1)),           sg.Button('Cancel', font=font, size=(10, 1))]]


    window = sg.Window('Second Window', layout)

    choice = None
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        
        if(event =='Ok' and values[0]=='1'):
            Employee()
        
        
        if (event=='Ok' and values[0]=='2'):
            mycursor.execute('select * from employee')
            myresult = mycursor.fetchall()
            sg.theme('DarkAmber')  

            toprow = ['EmpID', 'Name', 'Gender', 'Age', 'Phone', 'Password']
            tbl1 = sg.Table(values=myresult, headings=toprow,
                            auto_size_columns=True,
                            display_row_numbers=False,
                            justification='center', key='-TABLE-',
                            selected_row_colors=('red', 'yellow'),
                            enable_events=True,
                            expand_x=True,
                            expand_y=True,
                            enable_click_events=True,
                            font=('Helvetica', 14))

            layout = [[tbl1]]
            window = sg.Window("Table Demo", layout, size=(1000, 500), resizable=True)
            while True:
                event, values = window.read()
                print("event:", event, "values:", values)
                if event == sg.WIN_CLOSED:
                    break
                
        if(event=='Ok' and values[0]=='3'):
            layout = [
                    [sg.Text('Enter Employee ID:', font=('Helvetica', 14)), sg.Input(key='empid')],
                    [sg.Text('Enter 1 for Name', font=('Helvetica', 14))],
                    [sg.Text('Enter 2 for Gender', font=('Helvetica', 14))],
                    [sg.Text('Enter 3 for Age', font=('Helvetica', 14))],
                    [sg.Text('Enter 4 for PhoneNo', font=('Helvetica', 14))],
                    [sg.Text('Enter 5 for Password', font=('Helvetica', 14))],
                    [sg.Text('Enter Choice:', font=('Helvetica', 14)), sg.Input(key='choice')],
                    [sg.Button('Update', size=(10, 1))],
                    [sg.Output(size=(60, 10))],
                    ]

            window = sg.Window('Employee Details').Layout(layout)

            while True:
                event, values = window.Read()
                if event is None:
                    break

                empid = int(values['empid'])
                choice = int(values['choice'])

                if choice == 1:
                    n = sg.PopupGetText('Enter New Name:')
                    s = "update employee set ename=%s where Emp_id=%s;"
                    val = (n, empid)
                    mycursor.execute(s, val)
                    mydb.commit()

                elif choice == 2:
                    n = sg.PopupGetText('Enter New Gender:')
                    s = "update employee set emp_g=%s where Emp_id=%s;"
                    val = (n, empid)
                    mycursor.execute(s, val)
                    mydb.commit()

                elif choice == 3:
                    n = sg.PopupGetText('Enter New Age:', numeric=True)
                    s = "update employee set eage=%s where Emp_id=%s;"
                    val = (n, empid)
                    mycursor.execute(s, val)
                    mydb.commit()

                elif choice == 4:
                    n = sg.PopupGetText('Enter New Phone Number:', numeric=True)
                    s = "update employee set emp_phone=%s where Emp_id=%s;"
                    val = (n, empid)
                    mycursor.execute(s, val)
                    mydb.commit()

                elif choice == 5:
                    n = sg.PopupGetText('Enter New Password:')
                    s = "update employee set pwd=%s where Emp_id=%s;"
                    val = (n, empid)
                    mycursor.execute(s, val)
                    mydb.commit()

                else:
                    print("entered wrong choice")

                a = sg.PopupYesNo('Do you want to update more data?')
                if a == 'No':
                    sg.popup('Employee updated successfully')
                    break
                else:
                    s = "select * from employee where Emp_id=%s"
                    val = [empid]
                    print("Updated employee details are:")
                    mycursor.execute(s, val)
                    res = mycursor.fetchall()
                    print(res)


            window.close()
            
        if(event == 'Ok' and values[0]=='4'):
            layout = [
                [sg.Text("Enter employee id which is to be deleted:", font=('Helvetica', 14))],
                [sg.Input(key="empid")],
                [sg.Button("Delete", size=(10, 1)), sg.Button("Exit", size=(10, 1))]
                     ]


            window = sg.Window("Employee Deletion", layout)


            while True:
                event, values = window.read()


                if event == sg.WIN_CLOSED or event == "Exit":
                    break


                empid = values["empid"]


                sql = 'delete from employee where Emp_id=%s'
                val = [empid]
                mycursor.execute(sql, val)
                mydb.commit()
                print('record deleted')


                a = sg.PopupYesNo("Do you want to delete more data?", title="Confirmation")

                if a == "No":
                    sg.popup('Employee deleted successfully')
                    break


            window.close()

        
    window.close()


def MenuSet():
    

    sg.theme('DarkAmber')   

    font = ('Axial', 18)
    layout = [[sg.Text('Enter 1: Employee module', font=font, size=(25, 1))],
            [sg.Text('_'*50, text_color='white')],
          [sg.Text('Enter 2: Customer module', font=font, size=(25, 1))],
            [sg.Text('_'*50, text_color='white')],
          [sg.Text('Enter 3: Food module', font=font, size=(25, 1))],
            [sg.Text('_'*50, text_color='white')],
          [sg.Text('Enter 4: Search Database', font=font, size=(25, 1))],
            [sg.Text('_'*50, text_color='white')],
          [sg.Text('Enter 5: Generate Bill', font=font, size=(25, 1))],
            [sg.Text('_'*50, text_color='white')],
          [sg.Text('Enter 6: View Billed Items', font=font, size=(25, 1))],
            [sg.Text('_'*50, text_color='white')],
          [sg.InputText(font=font, size=(30, 1))],
          [sg.Button('Ok', font=font, size=(10, 1)),           sg.Button('Cancel', font=font, size=(10, 1))]]


    window = sg.Window('Restaurant Management System', layout, size=(700, 500))




    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': 
            break
        if(event=='Ok' and values[0] == '1'):
            open_emp_window()
        if(event=='Ok' and values[0] == '2'):
            open_cust_window()
        if(event=='Ok' and values[0]=='3'):
            open_food_window()
        if(event=='Ok' and values[0]=='4'):
            View()
        if(event=='Ok' and values[0]=='5'):
            billgenerator()
        if(event=='Ok' and values[0]=='6'):
            open_bill_window()
    window.close()


def RunAgain():
    RunAgn=input("\nwant to run again Y/N")
    while RunAgn.lower()=='y':
        if(platform.system()=="Windows"):
            print(os.system('cls'))
        else:
            print(os.system('clear'))
        MenuSet()
        RunAgn=input("\nwant to run again Y/N")
    else:
        print("Good Bye... HAVE A NICE DAY")


MenuSet()
RunAgain()