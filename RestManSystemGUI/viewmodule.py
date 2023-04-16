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

def View():


        layout = [
            [sg.Text('Select the search criteria:', font=('Arial', 14))],
            [sg.Radio('Employee', 'RADIO1', default=True, key='emp', font=('Arial', 12)), sg.Radio('Customer', 'RADIO1', key='cust', font=('Arial', 12)), sg.Radio('Food', 'RADIO1', key='food', font=('Arial', 12))],
            [sg.Text('Enter the ID:', font=('Arial', 14)), sg.InputText(key='id')],
            [sg.Button('Search', size=(10, 1)), sg.Button('Exit', size=(10, 1))]
        ]

      
        window = sg.Window('Search', layout, size=(500, 200))





        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            if values['emp']:
                s = int(values['id'])
                rl = (s,)
                sql = "SELECT * FROM employee WHERE Emp_id = %s"
                mycursor.execute(sql, rl)
                res = mycursor.fetchall()
                if not res:
                    sg.popup('No Employee Found')
                else:
                    header_list = [i[0] for i in mycursor.description]
                    data = [[str(j) for j in i] for i in res]
                    table_layout = [[sg.Table(values=data, headings=header_list, max_col_width=25, auto_size_columns=False, justification='center')]]
                    sg.Window('Employee Search Results', table_layout).read()

            elif values['cust']:
                s = int(values['id'])
                rl = (s,)
                sql = "SELECT * FROM customer WHERE c_id = %s"
                mycursor.execute(sql, rl)
                res = mycursor.fetchall()
                if not res:
                    sg.popup('No Customer Found')
                else:
                    header_list = [i[0] for i in mycursor.description]
                    data = [[str(j) for j in i] for i in res]
                    table_layout = [[sg.Table(values=data, headings=header_list, max_col_width=25, auto_size_columns=False, justification='center')]]
                    sg.Window('Customer Search Results', table_layout).read()

            elif values['food']:

                s = int(values['id'])
                a = (s,)
                sql = "SELECT * FROM food WHERE Food_id = %s"
                mycursor.execute(sql, a)
                res2 = mycursor.fetchall()
                if not res2:
                    sg.popup('No Food Item Found')
                else:
                    header_list = [i[0] for i in mycursor.description]
                    data = [[str(j) for j in i] for i in res2]
                    table_layout = [[sg.Table(values=data, headings=header_list, max_col_width=25, auto_size_columns=False, justification='center')]]
                    sg.Window('Food Item Search Results', table_layout).read()


        window.close()


    



