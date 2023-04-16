import mysql.connector

import PySimpleGUI as sg

mydb = mysql.connector.connect(
    host="sql12.freemysqlhosting.net",
    user="sql12612684",
    password="fwX87sAhRW",
    database="sql12612684"
)
mycursor=mydb.cursor()


def add_employee(Input_Values):
    sql = "INSERT INTO employee (ename,emp_g,eage,emp_phone,pwd) VALUES (%s, %s, %s, %s, %s)"
    val = (Input_Values[0], Input_Values[1], Input_Values[2], Input_Values[3], Input_Values[4])
    mycursor.execute(sql, val)
    mydb.commit()



def Employee():
    sg.theme('DarkAmber')  

    layout = [
        [sg.Text('Enter the Employee Name:', font=('Helvetica', 14)), sg.InputText()],
        [sg.Text('Enter Employee Gender : ', font=('Helvetica', 14)), sg.InputText()],
        [sg.Text('Enter Employee age: ', font=('Helvetica', 14)), sg.InputText()],
        [sg.Text('enter employee phone number: ', font=('Helvetica', 14)), sg.InputText()],
        [sg.Text('Enter the password : ', font=('Helvetica', 14)), sg.InputText()],
        [sg.Button('Add', size=(10, 1)), sg.Button('Cancel', size=(10, 1))]
    ]

    window = sg.Window('Window Title', layout, size=(500, 300))
    while True:
                event, values = window.read()
                print("event:", event, "values:", values)
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                if event == 'Add':
                    add_employee(values)
                    sg.popup('Employee added successfully')
                    break

    window.close()

   