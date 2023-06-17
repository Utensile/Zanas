import serial
import time
import winsound
import threading
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as cTk

k=0
def uFormat(num, dig):
    return ('{number:.{digits}f}'.format(number=num, digits=dig))

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
        app = cTk.CTk()
        cTk.set_appearance_mode("Dark")
        app.title("my app")
        w= app.winfo_screenwidth()*0.8
        h= app.winfo_screenheight()*0.9
        x= app.winfo_screenwidth()*0.05
        y= app.winfo_screenheight()*0.1
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))
        app.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        app.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)

        frame_color="#999999"
        txt_color_light="#F0F0F0"
        txt_color_dark="#212121"
        GROUPE_font = cTk.CTkFont(family="GROUPE MEDIUM", size=50)
        Nasalization_font = cTk.CTkFont(family="Nasalization Rg", size=50)
        TextFontL=cTk.CTkFont(family="Robot Lt", size=40)
        TextFontM=cTk.CTkFont(family="Robot Lt", size=30)
        TextFontS=cTk.CTkFont(family="Robot Lt", size=15)
        corn_rad=20
        butt_size=100
        butt_color="#444444"
        timeFrame_color="#212121"
        graphColorIn="#AAAAAA"
        gray=graphColorIn

        global maxf
        global incoming_data
        global ti
        global ax
        global canvas
        global impulse
        global cVariable
        cVariable=0
        impulse=0
        ti=[0.0]
        incoming_data=[0]
        maxf=0
        
        def resetData(arduino=False):
            global maxf
            global incoming_data
            global ti
            global ax
            global canvas
            global impulse
            global cVariable
            impulse=0
            if(not arduino):
                ti[-1]=cVariable
            else :
                cVariable=0
            ti=[0.0]
            incoming_data=[0]
            updateGraph()
            maxf=0
            ser.write(b'2')


        def updateGraph():
            global ti
            global ax
            global canvas
            global incoming_data 
            ax.clear()
            ax.plot(ti, incoming_data, linewidth=3, color="#FF0000",label="Force(N)")
            ax.grid()
            ax.legend()
            ax.set_title("Force(N) over Time(s)")
            ax.set_xlabel("Time(s)")
            ax.set_ylabel("Force(N)")
            ax.fill_between(ti, incoming_data, 0, color="#FF0000", alpha=0.2)
            canvas.draw()

        def Ignite_Motor():
            global stop
            stop=0
            if startButton['text']=="Activate":
                Ignite_Motor['text']='Waiting for Ignition..'
                Ignite_Motor['foreground']= gray
                startButton.configure(text="Ignite Motor")
                startButton['bg']="#91030a"
                stop=0
            else:
                if startButton['text']=="Ignite Motor":
                    for i in range(5, 0, -1):
                        if(stop!=1):
                            Ignite_Motor['text'] = 'Ignition in {}'.format(i)
                            app.update()
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
                        startButton['text']="Reset"
                        startButton['bg']=gray
                    else:
                        Ignite_Motor['text']='Waiting for Ignition...'
                        Ignite_Motor['foreground']= gray
                        startButton['text']="Ignite_Motor"
                        startButton['bg']="#91030a"
                    app.update()
                else:
                    if startButton['text']=="Reset":
                        Ignite_Motor['text']='Waiting for Activation...'
                        Ignite_Motor['foreground']= gray
                        startButton['text']='Activate'
                        startButton['bg']=gray
        def export():
            print("export")
        # Make the new window fullscreen
        
        #TitleFrame
        titleFrame=cTk.CTkFrame(app, corner_radius=corn_rad/2,fg_color=frame_color, height=80)
        titleFrame.grid(row=0, column=0, rowspan=1, columnspan=7, sticky="ew", padx=10, pady=10)

        zanasLabel=cTk.CTkLabel(titleFrame, text="ZANAS", text_color=txt_color_light, font=Nasalization_font)
        zanasLabel.grid(row=0, column=0, padx=20, pady=15)
        titleLabel=cTk.CTkLabel(titleFrame, text="LoaD-CEll Monitor", text_color=txt_color_light, font=GROUPE_font)
        titleLabel.grid(row=0, column=1, padx=20, pady=15)

        #ButtonFrame
        buttonFrame=cTk.CTkFrame(app, corner_radius=corn_rad, fg_color=frame_color)
        buttonFrame.grid(row=1, column=0, rowspan=9, columnspan=4, sticky="nsew", padx=10, pady=10)

        buttonFrame.grid_rowconfigure((0, 1, 2), weight=1)
        buttonFrame.grid_columnconfigure(0, weight=1)
        timeFrame=cTk.CTkFrame(buttonFrame, corner_radius=corn_rad*1.5, fg_color=timeFrame_color)
        timeFrame.grid(row=0, column=0, padx=20, pady=15)
        dateLabel=cTk.CTkLabel(timeFrame, text="16/01/2023 9:00", text_color=txt_color_light, font=TextFontL)
        dateLabel.pack(padx=10, pady=10)
        startButton=cTk.CTkButton(buttonFrame, text="Start Test", text_color=txt_color_light, font=TextFontL, command=Ignite_Motor, width=butt_size, height=butt_size*4*0.25, fg_color=butt_color, corner_radius=corn_rad*1.5)
        startButton.grid(row=1, column=0, padx=20, pady=8)
        exportButton=cTk.CTkButton(buttonFrame, text="Export Data", text_color=txt_color_light, font=TextFontS, command=export, width=butt_size*4*0.35, height=butt_size*4*0.35*0.4, fg_color=butt_color)
        exportButton.grid(row=2, column=0, padx=20, pady=15)

        #WeatherFrame
        weatherFrame=cTk.CTkFrame(app, corner_radius=corn_rad, fg_color=frame_color)
        weatherFrame.grid(row=10, column=0, rowspan=1, columnspan=3, sticky="nsew", padx=10, pady=10)

        weatherFrame.grid_rowconfigure((0, 1, 2), weight=1)
        weatherFrame.grid_columnconfigure((0, 1), weight=1)
        humidityLabel=cTk.CTkLabel(weatherFrame, text="Humidity: ", text_color=txt_color_dark, font=TextFontM)
        humidityLabel.grid(row=0, column=0, padx=20, pady=15)
        temperatureLabel=cTk.CTkLabel(weatherFrame, text="Temperature: ", text_color=txt_color_dark, font=TextFontM)
        temperatureLabel.grid(row=1, column=0, padx=20, pady=15)
        pressureLabel=cTk.CTkLabel(weatherFrame, text="Pressure: ", text_color=txt_color_dark, font=TextFontM)
        pressureLabel.grid(row=2, column=0, padx=20, pady=15)
        hValueLabel=cTk.CTkLabel(weatherFrame, text="0.00%", text_color=txt_color_dark, font=TextFontM)
        hValueLabel.grid(row=0, column=1, padx=20, pady=15)
        TValueLabel=cTk.CTkLabel(weatherFrame, text="0.00 °C", text_color=txt_color_dark, font=TextFontM)
        TValueLabel.grid(row=1, column=1, padx=20, pady=15)
        pValueLabel=cTk.CTkLabel(weatherFrame, text="000 Pa", text_color=txt_color_dark, font=TextFontM)
        pValueLabel.grid(row=2, column=1, padx=20, pady=15)

        #GraphFrame
        graphFrame=cTk.CTkFrame(app, corner_radius=corn_rad, fg_color=frame_color)
        graphFrame.grid(row=1, column=4, rowspan=8, columnspan=3, sticky="nsew", padx=10, pady=10)

        graphFrame.grid_rowconfigure(0, weight=1)
        graphFrame.grid_columnconfigure(0, weight=1)

        fig = plt.Figure()
        fig.patch.set_facecolor(frame_color)
        ax = fig.add_subplot(111)
        ax.patch.set_facecolor(graphColorIn)
        #ax.figure.set_figheight(3.8)
        #ax.figure.set_figwidth(6.5)
        canvas = FigureCanvasTkAgg(fig, master=graphFrame)
        canvas.get_tk_widget().grid(row = 0, column=0, padx=2, pady=2)
        ax.plot(ti, incoming_data, linewidth=3, color="#FF0000",label="Force(N)")  
        ax.grid()
        ax.legend()
        ax.set_title("Force(N) over Time(s)")
        ax.set_xlabel("Time(s)")
        ax.set_ylabel("Force(N)")
        ax.fill_between(ti, incoming_data, 0, color="#FF0000", alpha=0.2)
        canvas.draw()

        #DataFrame
        dataFrame=cTk.CTkFrame(app, corner_radius=corn_rad, fg_color=frame_color)
        dataFrame.grid(row=10, column=4, rowspan=3, columnspan=3, sticky="nsew", padx=10, pady=10)

        dataFrame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        dataFrame.grid_columnconfigure((0, 1), weight=1)
        gramLabel=cTk.CTkLabel(dataFrame, text="Force(g): ", text_color=txt_color_light, font=TextFontM)
        gramLabel.grid(row=0, column=0, padx=20, pady=15)
        NewtonLabel=cTk.CTkLabel(dataFrame, text="Force(N): ", text_color=txt_color_light, font=TextFontM)
        NewtonLabel.grid(row=1, column=0, padx=20, pady=15)
        maxForceLabel=cTk.CTkLabel(dataFrame, text="Max Force(N): ", text_color=txt_color_light, font=TextFontM)
        maxForceLabel.grid(row=2, column=0, padx=20, pady=15)
        impulseLabel=cTk.CTkLabel(dataFrame, text="Impulse: ", text_color=txt_color_light, font=TextFontM)
        impulseLabel.grid(row=3, column=0, padx=20, pady=15)
        timeLabel=cTk.CTkLabel(dataFrame, text="Time: ", text_color=txt_color_light, font=TextFontM)
        timeLabel.grid(row=4, column=0, padx=20, pady=15)
        gLabel=cTk.CTkLabel(dataFrame, text="0.00 g", text_color=txt_color_light, font=TextFontM)
        gLabel.grid(row=0, column=1, padx=20, pady=15)
        NLabel=cTk.CTkLabel(dataFrame, text="0.000 N", text_color=txt_color_light, font=TextFontM)
        NLabel.grid(row=1, column=1, padx=20, pady=15)
        maxfLabel=cTk.CTkLabel(dataFrame, text="0.000 N", text_color=txt_color_light, font=TextFontM)
        maxfLabel.grid(row=2, column=1, padx=20, pady=15)
        iLabel=cTk.CTkLabel(dataFrame, text="0.000 N*s", text_color=txt_color_light, font=TextFontM)
        iLabel.grid(row=3, column=1, padx=20, pady=15)
        tLabel=cTk.CTkLabel(dataFrame, text="0.000 s", text_color=txt_color_light, font=TextFontM)
        tLabel.grid(row=4, column=1, padx=20, pady=15)
        # Function to read serial data and update the label
        def read_serial():
            while True:
                global maxf
                global incoming_data
                global impulse
                global k
                try:
                    data = str(ser.readline().strip())[2:-1]
                    print(data)
                except serial.SerialException as e:
                    print("Error", str(e))
                else:
                    if(data[0].isnumeric()):
                        force = ''
                        temp= ''
                        for i in range(0, len(data)):
                            if data[i]!=" ":
                                force = force + data[i]
                            else:
                                for j in range((i+1), len(data), 1):
                                    temp=temp + data[j]
                                break
                        try:
                            force=float(force)
                        except ValueError:
                            print("Error: " + str(force))
                        incoming_data.append(round(force*0.009806652, 3))
                        temp=float(temp)/1000
                        if(temp<ti[-1]):
                            resetData()
                        else:
                            ti.append(temp)
                            if(force>maxf):
                                maxf=force
                                maxfLabel.configure(text=str(uFormat(round(maxf*0.009806652, 4), 3)+" N"))
                            impulse+=float(incoming_data[-1])*(ti[-1]-ti[-2])
                            iLabel.configure(text=str(uFormat(impulse, 3)) +  "N*s")
                            gLabel.configure(text=str(uFormat(force, 2))+" g")
                            NLabel.configure(text=str(uFormat(round(force*0.009806652, 4), 3)+ " N"))
                            tLabel.configure(text=str(ti[-1])+" s")
                            if(k%3==0):
                                updateGraph()
                            k+=1

        
        
        # Start reading serial data in a separate thread
        t = threading.Thread(target=read_serial)
        t.start()

        app.mainloop()

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
port_name_entry.insert(0, "COM")

baud_rate_label = ttk.Label(root, text="Baud Rate:",font=("Helvetica", 20), background="#282424", foreground="#DDDDDD")
baud_rate_label.grid(row=1, column=0, padx=10, pady=10)  # Add baud_rate_label to the window with padding

baud_rate_entry = ttk.Entry(root, font=("Helvetica", 20))
baud_rate_entry.insert(0, "9600")
baud_rate_entry.grid(row=1, column=1, padx=10, pady=10)  # Add baud_rate_entry to the window with padding

# Add a button to the window with padding
open_button = tk.Button(root, text="Avvia Monitor Zanas", font=("Helvetica", 25), command=open_serial_port)
open_button.grid(row=2, column=0, columnspan=2, pady=40)  # Add open_button to the window

# Run the Tkinter event loop
root.mainloop()
