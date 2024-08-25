# NOTE: VIN NUMBER OR PLATE SEARCH WITHIN TIME RANGE WILL BE ADDED
from tkinter import *
from time import sleep
from datetime import datetime
from serial import *
from sqlite3 import connect

PLATES = {
    "33NV172": "5UXXW3C53J0T80683"
}

file = connect("manager.db")
cursor = file.cursor()

def displayData(data, single=0):
    if single == 0:
        for i in range(len(data)):
            text = "NO: " + str(i + 1) + "\t" + "VIN: " + data[i][0] + "\t\t" + "DATE: " + data[i][1] + "\t\t" + "LOCATION: " + str(data[i][2]) + "," + str(data[i][2]) + '\n'
            displayText(text)
    else:
        text = "VIN: " + data[0] + "\t\t\t" + "DATE: " + data[1] + '\n'
        displayText(text)

def fetchData(vin):
    if len(vin) == 17:
        cursor.execute("""SELECT * FROM vin_numbers WHERE vin_number=\"{}\"""".format(vin))
        data = cursor.fetchall()
        if data == []:
            print("NO RECORDED INFORMATION FOUND FOR THIS VIN")
            displayText("NO RECORDED INFORMATION FOUND FOR THIS VIN\n")
            return 0
        else: return data
    else:
        print("ENTER A VALID VIN")
        displayText("ENTER A VALID VIN\n")
        return 0
        
def checkTimeRange(type, time):
    now = datetime.now().strftime("%c")
    try:
        print(time, type)
        if time[2]=="." and time[5]=="." and time[10]==" " and time[13]==":" and time[16]==":": 
            return now
        elif (not len(time) == 17): return 0
        elif int(time[0:2]) > 31 or int(time[3:5]) > 12: return 0
        elif int(time[9:11]) > 23 or int(time[12:14]) > 59 or int(time[15:17]) > 59: return 0
        else: return 1
    except:
        return 0                

def clearDatabase():
    confirmation = input("THIS WILL CLEAR THE ENTIRE DATABASE. TYPE 'yes' TO ACCEPT, OR PRESS ENTER TO CANCEL: ")
    if confirmation == 'yes':
        cursor.execute("DELETE FROM manager")
        file.commit()
        print("DATABASE CLEARED")
    else: print("CANCELED")
    
    
win = Tk()
win.title("VIN ID QUERY PANEL")
win.geometry("800x750")
win.resizable(True, True)

title_label = Label(win, text = "VIN-ID QUERY PANEL")
vin_label = Label(win, text = "VIN")
plate_label = Label(win, text = "PLATE")
date_label = Label(win, text = "DATE")
start_date_label = Label(win, text = "START DATE:")
end_date_label = Label(win, text = "END DATE:")

vin_entry = Entry(win)
plate_entry = Entry(win)
start_date_entry = Entry(win)
end_date_entry = Entry(win)

list_box = Text(win, width=100, height=50)

def displayText(text):    
    list_box.config(state = NORMAL)
    list_box.insert(INSERT, str(text))
    list_box.config(state = DISABLED)
    
def searchByVin():
    vin = vin_entry.get()
    data = fetchData(vin)
    if data != 0: displayData(data)
    displayText("--------------------------------------------------\n")

def searchByPlate():
    plate = plate_entry.get()
    if plate in PLATES:
        vin = PLATES.get(plate)
        data = fetchData(vin)
        displayData(data)
    else:
        print("THIS PLATE IS NOT REGISTERED")
        displayText("THIS PLATE IS NOT REGISTERED\n")
    displayText("--------------------------------------------------\n")
    
def searchByDate():
    start_date = start_date_entry.get()
    control = checkTimeRange(1, start_date)
    if control == 0:
        print("INVALID FORMAT")
        displayText("INVALID DATE-TIME FORMAT\n")
        displayText("--------------------------------------------------\n")
        return
    else:
        end_date = end_date_entry.get()
        control = checkTimeRange(2, end_date)
        if control == 0:
            print("INVALID FORMAT")
            displayText("INVALID DATE-TIME FORMAT\n")
            displayText("--------------------------------------------------\n")
            return
        elif (not control == 0) and (not control == 1): end_date = control
        print("START DATE: " + start_date + '\n')
        print("END DATE: " + str(end_date) + '\n\n')
        displayText("START DATE: " + start_date + '\n')
        displayText("END DATE: " + str(end_date) + '\n\n')
        i = 1
        global data
        cursor.execute("SELECT * FROM vin_numbers")
        data = cursor.fetchone()
        index = 0
        while start_date > data[1]:
            index += 1
            data = cursor.fetchone()
            print(data)
        while start_date <= data[1] and data[1] <= end_date:
            data = cursor.fetchone()
            displayData(data, 1)
    displayText("--------------------------------------------------\n")
                
vin_query_button = Button(win, text = "QUERY BY VIN", command = searchByVin)
plate_query_button = Button(win, text = "QUERY BY PLATE", command = searchByPlate)
date_query_button = Button(win, text = "QUERY BY DATE", command = searchByDate)

title_label.grid(columnspan = 4)
vin_label.grid(row = 1)
plate_label.grid(row = 1, column = 1)
date_label.grid(row = 1, column = 3)
start_date_label.grid(row = 2, column = 2, sticky = E)
end_date_label.grid(row = 3, column = 2, sticky = E)

vin_entry.grid(row = 2)
plate_entry.grid(row = 2, column = 1)
start_date_entry.grid(row = 2, column = 3)
end_date_entry.grid(row = 3, column = 3)

vin_query_button.grid(row = 4)
plate_query_button.grid(row = 4, column = 1)
date_query_button.grid(row = 4, column = 3)

list_box.grid(row = 5, columnspan = 4, sticky = "nsew")

win.mainloop()
