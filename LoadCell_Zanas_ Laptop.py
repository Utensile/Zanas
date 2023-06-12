import serial
import time
import codecs
import winsound
import threading
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
#HELLO WORLD
# Function to handle opening the serial port
def open_serial_port():
    # Get the serial port name and baud rate from the input fields
    port_name = port_name_entry.get()
    baud_rate = baud_rate_entry.get()

    # Attempt to open the serial port
    try:
        # Open the serial port
        ser = serial.Serial(port_name, baud_rate)

        # If successful, close the window
        root.withdraw()

        # Open a new window using Tkinter
        window = tk.Tk()
        window.title("Zanas Load-Cell")  # Add title to the window

        global maxf;
        maxf=0;
        
        def parachute():
            ser.write(b'2')
            Ignite_Motor['text']= "Parachute Deployed!"
            Ignite_Motor['foreground']= "#91030a"
            window.update()
            winsound.Beep(1000, 500)
            if button['text']=="Ignite Motor":
                Ignite_Motor['text']='Waiting for Ignition...'
                Ignite_Motor['foreground']= gray
            else:
                if button['text']=="Activate":
                    Ignite_Motor['text']='Waiting for Activation...'
                    Ignite_Motor['foreground']= gray
                else:
                    Ignite_Motor['foreground']= '#DDDDDD'
                    Ignite_Motor['text']= "Motor Ignited"         
            window.update()

        def stopIgnition():
            global stop
            stop=1
        
        def Ignite_Motor():
            global stop
            stop=0
            if button['text']=="Activate":
                Ignite_Motor['text']='Waiting for Ignition..'
                Ignite_Motor['foreground']= gray
                button['text']="Ignite Motor"
                button['bg']="#91030a"
                stop=0
            else:
                if button['text']=="Ignite Motor":
                    for i in range(5, 0, -1):
                        if(stop!=1):
                            Ignite_Motor['text'] = 'Ignition in {}'.format(i)
                            window.update()
                        if(stop!=1):
                            winsound.Beep(800, 300)
                        if(stop!=1):
                            time.sleep(0.7)
                        else:
                            break
                    if(stop!=1):
                        ser.write(b'1')
                        Ignite_Motor['text']= "Motor Ignited!!!"
                        root.update()
                        winsound.Beep(1000, 1000)
                        Ignite_Motor['text']= "Motor Ignited"
                        Ignite_Motor['foreground']= '#DDDDDD'
                        button['text']="Reset"
                        button['bg']=gray
                    else:
                        Ignite_Motor['text']='Waiting for Ignition...'
                        Ignite_Motor['foreground']= gray
                        button['text']="Ignite_Motor"
                        button['bg']="#91030a"
                    window.update()
                else:
                    if button['text']=="Reset":
                        Ignite_Motor['text']='Waiting for Activation...'
                        Ignite_Motor['foreground']= gray
                        button['text']='Activate'
                        button['bg']=gray
        
        # Make the new window fullscreen
        window.attributes('-fullscreen', True)
        window.configure(bg="#282424")
    
        #window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        # Set the font size and color for the serial reader window
        serial_label_font = ('Helvetica', 72)
        serial_label_color = 'white'
        alt_label_font = ('Helvetica', 36, "bold")
        
        crimson = '#DC143C'
        gray="#8C92AC"

        # Add a label to the window for displaying serial data
        #peso (g)
        alt_label1 = ttk.Label(window, text="Peso:", font=alt_label_font, foreground=crimson, background="#282424", justify = 'center')
        alt_label1.grid(row=0, column = 0, columnspan = 3)
        serial_label1 = ttk.Label(window, text="5 Data...", font=serial_label_font, foreground=serial_label_color, background="#282424", justify = 'center')
        serial_label1.grid(row=1, column = 0, columnspan =3)
        #Forza(N)
        alt_label2 = ttk.Label(window, text="Force:", font=alt_label_font, foreground=crimson, background="#282424", justify = 'center')
        alt_label2.grid(row=0, column = 3, columnspan = 3)
        serial_label2 = ttk.Label(window, text="5 Data...", font=serial_label_font, foreground=serial_label_color, background="#282424", justify = 'center')
        serial_label2.grid(row=1, column = 3, columnspan = 3)
        
        #Graph
        canvas = tk.Canvas(window, width=300, height=200, bg="white")
        rectangle = canvas.create_rectangle(50, 50, 150, 100, fill="white")
        canvas.grid(row = 2, column = 0, columnspan = 6, rowspan = 2, pady = 25)


        #button
        button = tk.Button(window, text="Activate", font=("Helvetica", 50, "bold"), bg=gray, foreground='white', relief='raised', bd=20, command=Ignite_Motor)
        button.grid(row=4, column = 0, columnspan =4)
        Ignite_Motor = ttk.Label(window, text="Waiting for Activation...", font=('Helvetica', 40), foreground=gray, background="#282424")
        Ignite_Motor.grid(row=5, column = 0, columnspan =4)

        maxfLabel = ttk.Label(window, text="Max Force: 0.00 N", font=('Helvetica', 30, "bold"), foreground="#D89216", background="#282424")
        maxfLabel.grid(row = 4, column = 4, columnspan = 2)
        impulseLabel = ttk.Label(window, text="Impulse: 0.00 N*s", font=('Helvetica', 30, "bold"), foreground="#D89216", background="#282424")
        impulseLabel.grid(row = 5, column = 4, columnspan = 2)

        # Function to read serial data and update the label
        def read_serial():
            while True:
                global maxf
                data = ser.readline().decode().strip()
                serial_label.configure(text=data)
                if(data[0].isnumeric()):
                    res = ''
                    for i in range(0, len(data)):
                        if data[i]!=" ":
                            res = res + data[i]
                        else:
                            break
                    if(float(res)>maxf):
                        maxf=float(res)
                        maxfLabel.configure(text="Max Height: "+str(maxf)+" m")

        
        
        # Start reading serial data in a separate thread
        t = threading.Thread(target=read_serial)
        t.start()

        window.mainloop()

    except serial.SerialException as e:
        # Display error message in a messagebox
        messagebox.showerror("Error", str(e))

def parachute():
    global stop


def stopIgnite_Motor():
    global stop


# Create the main Tkinter window
root = tk.Tk()
root.title("Configurazione Seriale Zanas")  # Add title to the window
root.configure(bg="#282424")

# Configure the window size
root.geometry("600x300")

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (600 / 2))
y = int((screen_height / 2) - (300 / 2))
root.geometry(f"600x300+{x}+{y}")

# Add labels and input fields to the window with padding
port_name_label = ttk.Label(root, text="Serial Port Name:",font=("Helvetica", 17), background="#282424", foreground="#DDDDDD")
port_name_label.grid(row=0, column=0, padx=10, pady=10)  # Add port_name_label to the window with padding

port_name_entry = ttk.Entry(root, font=("Helvetica", 20))
port_name_entry.grid(row=0, column=1, padx=10, pady=10)  # Add port_name_entry to the window with padding
port_name_entry.insert(0, "COM");

baud_rate_label = ttk.Label(root, text="Baud Rate:",font=("Helvetica", 20), background="#282424", foreground="#DDDDDD")
baud_rate_label.grid(row=1, column=0, padx=10, pady=10)  # Add baud_rate_label to the window with padding

baud_rate_entry = ttk.Entry(root, font=("Helvetica", 20))
baud_rate_entry.insert(0, "9600");
baud_rate_entry.grid(row=1, column=1, padx=10, pady=10)  # Add baud_rate_entry to the window with padding

# Add a button to the window with padding
open_button = tk.Button(root, text="Avvia Monitor Zanas", font=("Helvetica", 25), command=open_serial_port)
open_button.grid(row=2, column=0, columnspan=2, pady=40)  # Add open_button to the window

# Run the Tkinter event loop
root.mainloop()
