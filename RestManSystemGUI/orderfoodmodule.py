import mysql.connector
import random
import PySimpleGUI as sg

mydb = mysql.connector.connect(
    host="sql12.freemysqlhosting.net",
    user="sql12612684",
    password="fwX87sAhRW",
    database="sql12612684"
)
mycursor=mydb.cursor()

def add_foodOrder(Input_Values):
    OrderF_id=random.randint(1,(2**63)-1)
    sql="insert into orderfood values (%s, %s, %s, %s, %s)"
    val=(OrderF_id, Input_Values[0], Input_Values[1], Input_Values[2], Input_Values[3])
    mycursor.execute(sql, val)
    mydb.commit()
    

def OrderFood():
    sg.theme('DarkAmber')
    layout = [[sg.Text('Enter total price:'), sg.InputText()],
            [sg.Text('Enter Date: '), sg.InputText()],
            [sg.Text('Enter customer id: '), sg.InputText()],
            [sg.Text('Enter employee id:'), sg.InputText()],
            [sg.Button('Add'), sg.Button('Cancel')] ]
    window = sg.Window('Window Title', layout)
    while True:
            event, values = window.read()
            print("event:", event, "values:", values)
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            if event == 'Add':
                add_foodOrder(values)
                sg.popup('Order added successfully')
                break

    window.close()




