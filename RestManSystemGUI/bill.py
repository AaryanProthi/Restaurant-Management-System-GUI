import mysql.connector
import random
import PySimpleGUI as sg

mydb = mysql.connector.connect(
    host="sql12.freemysqlhosting.net",
    user="sql12612684",
    password="fwX87sAhRW",
    database="sql12612684"
)
mycursor = mydb.cursor()

def billgenerator():
    s = 0
    Orderfid = random.randint(1,(2**63)-1)

    layout = [        
        [sg.Text('Enter customer id for bill:', font=('Arial', 16)), sg.InputText(key='cid')],
        [sg.Text('Enter employee id for bill:', font=('Arial', 16)), sg.InputText(key='empid')],
        [sg.Text('Enter date of order:', font=('Arial', 16)), sg.InputText(key='date')],
        [sg.Text('Select food item to be ordered:', font=('Arial', 16))],
        [sg.Listbox(values=['coffee', 'dal makhani', 'tea', 'paneer tikka', 'chicken tikka'], key='food')],
        [sg.Text('Enter quantity:', font=('Arial', 16)), sg.InputText(key='quantity')],
        [sg.Button('Add to order', font=('Arial', 14)), sg.Button('Finish order', font=('Arial', 14))],
        [sg.Text('Order Summary', font=('Arial', 18))],
        [sg.Table(values=[], headings=['Food Item', 'Quantity', 'Cost'], key='order_summary', font=('Arial', 14))],
        [sg.Text('Total Bill:', font=('Arial', 16)), sg.Text('0', key='total_bill', font=('Arial', 16))],
        [sg.Button('Done', font=('Arial', 14))]
    ]

    window = sg.Window('Bill Generator', layout, size=(700, 525), font=('Arial', 14))


    order_summary = []
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        
        if(event == 'Done'):
            break

        if event == 'Add to order':
            food = values['food'][0]
            quantity = int(values['quantity'])

            if food == 'coffee':
                cost = quantity * 40
                order_summary.append([food, quantity, cost])
                s += cost
            elif food == 'dal makhani':
                cost = quantity * 300
                order_summary.append([food, quantity, cost])
                s += cost
            elif food == 'tea':
                cost = quantity * 30
                order_summary.append([food, quantity, cost])
                s += cost
            elif food == 'paneer tikka':
                cost = quantity * 220
                order_summary.append([food, quantity, cost])
                s += cost
            elif food == 'chicken tikka':
                cost = quantity * 250
                order_summary.append([food, quantity, cost])
                s += cost

            window['total_bill'].update(str(s))

        if event == 'Finish order':
            cid = int(values['cid'])
            empid = int(values['empid'])
            date = values['date']

            for item in order_summary:
                list = [Orderfid, f"{item[0]}({item[1]})"]
                val = (list)
                sql = 'insert into bill values(%s, %s)'
                mycursor.execute(sql, val)
                mydb.commit()

            sql2 = 'select orderid, group_concat(fooditem) from bill group by orderid having orderid=%s'
            val2 = (Orderfid,)
            mycursor.execute(sql2, val2)
            result = mycursor.fetchall()

            sql3 = 'insert into orderfood values(%s, %s, %s, %s, %s)'
            val3 = (Orderfid, s, date, cid, empid)
            mycursor.execute(sql3, val3)
            mydb.commit()

            window['order_summary'].update(order_summary)
            window['total_bill'].update(str(s))
    window.close()

    mydb.close()

                