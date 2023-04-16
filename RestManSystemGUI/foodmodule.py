import random
import mysql.connector

import PySimpleGUI as sg

mydb = mysql.connector.connect(
    host="sql12.freemysqlhosting.net",
    user="sql12612684",
    password="fwX87sAhRW",
    database="sql12612684"
)
mycursor=mydb.cursor()

def add_food(Input_Values):
    sql="insert into food (Foodname,price) values (%s,%s)"
    val = (Input_Values[0], Input_Values[1])
    mycursor.execute(sql, val)
    mydb.commit()



def Food():
    sg.theme('DarkAmber')
    layout = [[sg.Text('Enter Food Name:', font=('Helvetica', 14)), sg.InputText()],
            [sg.Text('Enter Price of Food: ', font=('Helvetica', 14)), sg.InputText()],
            [sg.Button('Add', size=(10, 1)), sg.Button('Cancel', size=(10, 1))] ]
    window = sg.Window('Window Title', layout)
    while True:
            event, values = window.read()
            print("event:", event, "values:", values)
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            if event == 'Add':
                add_food(values)
                sg.popup('Food Item added successfully')
                break

    window.close()
    

 
