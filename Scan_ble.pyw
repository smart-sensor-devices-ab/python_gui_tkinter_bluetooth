# Gjort av William 
# 2022-06-16 
# Smart Sensors Devices AB
# 
# libraries that is necessary for tkinter to work
import tkinter as tk
from tkinter import  ttk

# this is imported for the dongle and also for the "time.sleep()" commands
import serial
import time

# this is the library that is uesd to check the current time 
import datetime
now = datetime.datetime.now()

# this is what creates the main window
main_window = tk.Tk()

#changes the titel of the window
main_window.title('Scan for nearby Bluetooth devices')


# sets your port for the dongle
your_com_port = "COM18"  
connecting_to_dongle = True

#changes the size of the screens window
window_width = 900
window_height = 500

# get the screen dimension
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
# set the position of the window to the center of the screen
main_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# apply the grid layout
main_window.grid_columnconfigure(1, weight=1)
main_window.grid_rowconfigure(1, weight=1)


# create the text widget
text = tk.Text(main_window, height=30, width=30)
text.grid(row=1, column=1, sticky=tk.EW)


# this is the part of the code that communicates whit the dongle
print("Connecting to dongle...")
while connecting_to_dongle:
    try:
        console = serial.Serial(
            port=your_com_port,
            baudrate=57600,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=0,
        )
        if console.is_open.__bool__():
            connecting_to_dongle = False
    except:
        print("Dongle not connected. Please reconnect Dongle.")
        time.sleep(5)
print("Connected to Dongle.")

console.write(str.encode("AT+CENTRAL"))
console.write("\r".encode())
print("Putting dongle in Central role.")
time.sleep(0.1)

console.write(str.encode("AT+GAPSCAN=3"))
console.write("\r".encode())
time.sleep(0.1)
print("Looking for nearby Bluetooth devices ...")
dongle_output2 = console.read(console.in_waiting)
time.sleep(3)
print("Scan Complete!")
filtered = []

for dev in dongle_output2.decode().splitlines():
    if len(dev)>20:
        filtered.append(dev.split(maxsplit=1)[1])

seen = set()
out = []
for elem in filtered:
    prefix = elem.split(' ')[1]
    if prefix not in seen:
        seen.add(prefix)
        out.append(elem)

# sort list 
out.sort(key=lambda x:int(x.split()[3]), reverse=True)

# writes out the amount of bluetooth devices found on the main screen
text.insert('0.5', 'Amount of devices found: ' + str(len(out)) + '\n\n')

# funktion to get the current time
def get_time():
    return now.strftime('%H:%M:%S')

# prints out the time of the scan on the main screen
text.insert('1.0','The time of the scan: ' + str(get_time()) + '\n\n')

# writes out the results on the main screen
for i in range(0,len(out)):
    position = f'{i+5}.{len(out[i])}'
    tempStr = out[i] + "\n"
    text.insert(position,f' {tempStr}')

# is supposed to delet everyting on the list
out.clear()

#the funktion for the scan button
def button_clicked():
    # enables the programe to change the results on the main screen to the new ones after the user presses the scan button
    text['state'] = 'normal'
    # update the current time.
    now = datetime.datetime.now()
    # funktion to get the current time
    def get_time():
        return now.strftime('%H:%M:%S')
    # this simply puts a emty row betwen the results and the rest of the output on kommandotolken
    print()
    # this delets the previous output that is on the main screen
    text.delete('0.0', tk.END)

    # this is the part of the code that communicates whit the dongle 
    console.write(str.encode("AT+GAPSCAN=3"))
    console.write("\r".encode())
    time.sleep(0.1)
    
    dongle_output2 = console.read(console.in_waiting)
    time.sleep(3)
    filtered = []

    for dev in dongle_output2.decode().splitlines():
        if len(dev)>20:
            filtered.append(dev.split(maxsplit=1)[1])

    seen = set()
    out = []
    for elem in filtered:
        prefix = elem.split(' ')[1]
        if prefix not in seen:
            seen.add(prefix)
            out.append(elem)

    # sort list 
    out.sort(key=lambda x:int(x.split()[3]), reverse=True)

    
    #writes out the time of the scan on the main screen
    text.insert('1.0','The time of the scan: ' + str(get_time()) + '\n\n')

     # writes out the amount of bluetooth devices found on the main screen
    text.insert('0.0', 'Amount of devices found: ' + str(len(out)) + '\n\n')

    # writes out the results on the main screen
    for i in range(0,len(out)):
        position = f'{i+5}.{len(out[i])}'
        tempStr = out[i] + "\n" 
        text.insert(position,f' {tempStr}')

    # makes it so that you cant edite the results on the main screen
    text['state'] = 'disabled'

#what calls the function for the scan button. also fixes what the user will see as the buttons name.
main_button = ttk.Button(
    main_window,
    text='Scan again',
    command=lambda: button_clicked()
)
# creat the scan button 
main_button.grid(row=0, column=1, sticky=tk.EW)

# just an exit button.
exit_button = ttk.Button(
    main_window,
    text='Exit',
    command=lambda: main_window.quit()
)
# this determens were the exit button is located 
exit_button.grid(row=2, column=1, sticky=tk.EW)

# makes it so that you cant edite the results on the main screen
text['state'] = 'disabled'

# keeps the main window open
main_window.mainloop()

time.sleep(1)
console.close()