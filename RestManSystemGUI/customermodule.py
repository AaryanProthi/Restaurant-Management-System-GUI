import mysql.connector
from tabulate import *
import PySimpleGUI as sg

mydb = mysql.connector.connect(
    host="sql12.freemysqlhosting.net",
    user="sql12612684",
    password="fwX87sAhRW",
    database="sql12612684"
)

mycursor=mydb.cursor()

def add_customer(Input_Values):
    sql="insert into customer (name,cphone,paymenttype,email,date) values (%s,%s,%s,%s,%s)"
    val = (Input_Values[0], Input_Values[1], Input_Values[2], Input_Values[3], Input_Values[4])
    mycursor.execute(sql, val)
    mydb.commit()
    


def Customer():
        sg.theme('DarkAmber')
        layout =[ 
                [sg.Text('Enter the Customer Name:', font=('Helvetica', 14)), sg.InputText()],
                [sg.Text('Enter Customer Phone Number : ', font=('Helvetica', 14)), sg.InputText()],
                [sg.Text('Enter Payment Method ((1) credit card/(2) Debit Card/(3) Cash) : ', font=('Helvetica', 14)), sg.InputText()],
                [sg.Text('Enter Email ID: ', font=('Helvetica', 14)), sg.InputText()],
                [sg.Text('Enter Date : ', font=('Helvetica', 14)), sg.InputText()],
                [sg.Button('Add', size=(10, 1)), sg.Button('Cancel', size=(10, 1))] ]
        window = sg.Window('Window Title', layout)
        while True:
                event, values = window.read()
                print("event:", event, "values:", values)
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                if event == 'Add':
                    add_customer(values)
                    sg.popup('Customer added successfully')
                    break

        window.close()
    
    


    
