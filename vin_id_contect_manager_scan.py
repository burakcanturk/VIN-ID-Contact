from serial import *
from time import sleep
from serial.tools.list_ports import *
from tkinter import *
from datetime import datetime
from locale import setlocale, LC_ALL
from sqlite3 import connect

screen = Tk()
screen.title("VIN-ID CONTECT")
total_width = screen.winfo_screenwidth()
total_height = screen.winfo_screenheight()
width = 500
height = 200
width_ratio = (total_width - width) // 2
height_ratio = (total_height - height) // 2
screen.geometry(f"{width}x{height}+{width_ratio}+{height_ratio}")

file = connect("manager.db")
cursor = file.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS port_info(com_port TEXT NOT NULL, baudrate TEXT NOT NULL)""")

port = 0
conversion = ""
ser = ""
start = False

direction = Label(text="Select the Port to Connect Your Arduino", fg="blue", font=("Bold", 15))
direction.pack()

selection_area = Frame()
selection_area.pack()

selected_port = ""
selected_baud = 9600

def scan():
    value = b""
    value2 = ""
    screen.destroy()  # 5UXXW3C53J0T80683
    print()
    print("------------------------YOUR PORT IS CONNECTED. PLEASE WAIT...-----------------")
    setlocale(LC_ALL, "")
    cursor.execute("""CREATE TABLE IF NOT EXISTS vin_numbers(vin_number TEXT NOT NULL CHECK(17), date_time TEXT NOT NULL, latitude FLOAT NOT NULL, longitude FLOAT NOT NULL)""")
    while True:
        conversion = ""
        value2 = ""
        moment = datetime.now()
        now = datetime.strftime(moment, "%c")
        val = ser.read()
        if not (val == b"\n"):
            value += val
        else:
            if len(value) == 17:
                for i in value:
                    value2 += chr(i)
                location = ()
                if value2 == "1HGEG644387712345":
                    location = (36.7813763, 34.5417612)
                elif value2 == "5UXXW3C53J0T80683":
                    location = (41.0040196, 28.7319876)
                elif value2 == "3G1YZ23J9P5800001":
                    location = (37.0588879, 37.3100964)
                vin = (value2, now, location[0], location[1])
                print(now, value2, location, sep="\t")
                cursor.execute("""INSERT INTO vin_numbers VALUES (?,?,?,?)""", vin)
                file.commit()
                sleep(0.1)
            value = b""

def select_port(x):
    global selected_port
    selected_port = x

def select_baud(x):
    global selected_baud
    selected_baud = x

selected_port_var = StringVar()
com_ports = []

for i in comports():
    if "USB-SERIAL CH340" in str(i):
        com_ports.append(str(i).split(" ")[0])

port_label = Label(selection_area, text="Port:", font=("Bold", 15))
port_label.grid(column=0, row=0)

if len(com_ports) > 0:
    port_selection = OptionMenu(selection_area, selected_port_var, *com_ports, command=select_port)
else:
    port_selection = OptionMenu(selection_area, selected_port_var, "", command=select_port)
port_selection.configure(fg="blue", font=("Bold", 15))
port_selection.grid(column=1, row=0)

def control():
    global selected_port_var
    global com_ports
    global port_selection
    global my_selected

    port_control = []
    selected_port_var = StringVar()

    for i in comports():
        if "USB-SERIAL CH340" in str(i):
            port_control.append(str(i).split(" ")[0])

    settings = port_selection["menu"]

    for i in port_control:
        if not (i in com_ports):
            port_selection.destroy()
            selected_port_var.set(selected_port)
            if len(port_control) > 0:
                port_selection = OptionMenu(selection_area, selected_port_var, *port_control, command=select_port)
                port_selection.configure(fg="blue", font=("Bold", 15))
            else:
                port_selection = OptionMenu(selection_area, selected_port_var, "", command=select_port)
                port_selection.configure(fg="blue", font=("Bold", 15))
            port_selection.grid(column=1, row=0)

    for i in com_ports:
        if not (i in port_control):
            port_selection.destroy()
            if selected_port in port_control:
                selected_port_var.set(selected_port)
            if len(port_control) > 0:
                port_selection = OptionMenu(selection_area, selected_port_var, *port_control, command=select_port)
                port_selection.configure(fg="blue", font=("Bold", 15))
            else:
                port_selection = OptionMenu(selection_area, selected_port_var, "", command=select_port)
                port_selection.configure(fg="blue", font=("Bold", 15))
            port_selection.grid(column=1, row=0)

    com_ports = port_control
    screen.after(1000, control)

def connect():
    global selected_port
    global selected_baud
    global ser

    try:
        ser = Serial(selected_port, selected_baud)
    except serialutil.SerialException:
        result_message.configure(text="Connection Failed", fg="red", font=("Bold", 15))
    else:
        result_message.configure(text="Connected", fg="green", font=("Bold", 15))
        cursor.execute("""SELECT com_port FROM port_info""")
        data = cursor.fetchall()
        values = (selected_port, selected_baud)
        if len(data) == 0:
            cursor.execute("""INSERT INTO port_info VALUES(?,?)""", values)
        else:
            cursor.execute(f"""UPDATE port_info SET com_port="{selected_port}\"""")
            cursor.execute(f"""UPDATE port_info SET baudrate="{selected_baud}\"""")
        screen.after(1000, scan)

baud_label = Label(selection_area, text="Baud:", font=("Bold", 15))
baud_label.grid(column=0, row=1)
bauds = [300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 74880, 115200, 230400, 250000, 500000, 1000000, 2000000]

selected_baud_var = StringVar()
baud_selection = OptionMenu(selection_area, selected_baud_var, *bauds, command=select_baud)
baud_selection.configure(fg="blue", font=("Bold", 15))
baud_selection.grid(column=1, row=1)

connect_signal = Button(text="Connect", font=("Bold", 15), command=connect)
connect_signal.pack()

result_message = Label()
result_message.pack()

screen.after(1000, control)

screen.mainloop()
