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
from datetime import datetime

state=0
l=0
def uFormat(num, dig):
    return ('{number:.{digits}f}'.format(number=num, digits=dig))

def open_serial_port():
    # Get the serial port name and baud rate from the input fields
    port_name = port_name_entry.get()
    baud_rate = baud_rate_entry.get()
    global pressure
    global hum
    global temp
    pressure=pressure_entry.get()

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
        x= app.winfo_screenwidth()*0.1
        y= 0
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

        global state
        global maxf
        global incoming_data
        global ti
        global ax
        global canvas
        global impulse
        global cVariable
        global resetImpulse
        resetImpulse=True
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
            global avgf
            global impulseTime
            global cVariable
            global resetImpulse
            resetImpulse=True
            impulse=0
            if(not arduino):
                cVariable+=ti[-1]
            else:
                cVariable=0
            ti=[]
            incoming_data=[]
            maxf=0
            ser.write(b'2')
            ser.read_all


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
            global state
            stop=0
            if(state==0):
                infoLabel.configure(text='Waiting for Ignition..')
                infoLabel.configure(fg_color=gray)
                startButton.configure(text="Ignite Motor")
                startButton.configure(fg_color="#91030a")
                state=1
            elif(state==1):
                for i in range(5, 0, -1):
                    infoLabel.configure(text='Ignition in {}'.format(i))
                    app.update()
                    winsound.Beep(800, 300)
                    time.sleep(0.7)
                ser.read_all()
                ser.write(b'1')
                infoLabel.configure(text="Motor Ignited!!!")
                state=2
                winsound.Beep(1000, 1000)
                infoLabel.configure(text="Motor Ignited")
                infoLabel.configure(fg_color='#DDDDDD')
                startButton.configure(text="Reset")
                startButton.configure(bg_color=gray)
            elif(state==2):
                infoLabel.configure(text='Waiting for Activation...')
                infoLabel.configure(fg_color=gray)
                startButton.configure(text='Start Test')
                startButton.configure(bg_color=gray)
                state=0
        def export():
            global incoming_data
            global ti
            global pressure
            global hum
            global temp
            global impulse
            global avgf
            global impulseTime
            global maxf
            with open(datetime.now().strftime("DATA-%Y-%m-%d_%H-%M-%S.txt"), "w") as file:
                file.write("ZANAS load cell data test\n"+datetime.now().strftime("%d/%m/%Y\n%H:%M:%S")+"\n"+"Humidity: "+str(hum)+"%"+" - "+"Temperature: "+ str(temp)+" °C"+" - "+ "Pressure: "+str(pressure)+" Pa\nImpulse: "+str(round(impulse, 3))+" N*s - Impulse Time: "+str(impulseTime)+" s - Avg. Force:"+str(round(avgf,3))+ " N - Max Force: "+str(round(maxf*0.009806652, 3))+ "N\nForce(N): - Time(s)\n")
                for i in range(len(incoming_data)):
                    file.write(str(incoming_data[i])+ " - "+str(ti[i])+"\n")

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

        buttonFrame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        buttonFrame.grid_columnconfigure((0, 1), weight=1)
        timeFrame=cTk.CTkFrame(buttonFrame, corner_radius=corn_rad*1.5, fg_color=timeFrame_color)
        timeFrame.grid(row=0, column=0, columnspan=2, padx=20, pady=15)
        dateLabel=cTk.CTkLabel(timeFrame, text="16/01/2023 9:00", text_color=txt_color_light, font=TextFontM)
        dateLabel.pack(padx=10, pady=10)
        startButton=cTk.CTkButton(buttonFrame, text="Start Test", text_color=txt_color_light, font=TextFontL, command=Ignite_Motor, width=butt_size, height=butt_size*4*0.25, fg_color=butt_color, corner_radius=corn_rad*1.5)
        startButton.grid(row=1, column=0, columnspan=2, padx=20, pady=8)
        infoLabel=cTk.CTkLabel(buttonFrame, text="Waiting for Activation", text_color=txt_color_light, font=TextFontM)
        infoLabel.grid(row=2, column=0, columnspan=2, padx=20, pady=8)
        exportButton=cTk.CTkButton(buttonFrame, text="Export Data", text_color=txt_color_light, font=TextFontS, command=export, width=butt_size*4*0.35, height=butt_size*4*0.35*0.4, fg_color=butt_color)
        exportButton.grid(row=3, column=0, padx=20, pady=10)
        tareButton=cTk.CTkButton(buttonFrame, text="Tare Load Cell", text_color=txt_color_light, font=TextFontS, command=resetData, width=butt_size*4*0.35, height=butt_size*4*0.35*0.4, fg_color=butt_color)
        tareButton.grid(row=3, column=1, padx=20, pady=10)

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
        pValueLabel=cTk.CTkLabel(weatherFrame, text=str(pressure)+"  Pa", text_color=txt_color_dark, font=TextFontM)
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

        dataFrame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        dataFrame.grid_columnconfigure((0, 1), weight=1)
        gramLabel=cTk.CTkLabel(dataFrame, text="Force: ", text_color=txt_color_light, font=TextFontM)
        gramLabel.grid(row=0, column=0, padx=20, pady=8)
        NewtonLabel=cTk.CTkLabel(dataFrame, text="Force: ", text_color=txt_color_light, font=TextFontM)
        NewtonLabel.grid(row=1, column=0, padx=20, pady=8)
        maxForceLabel=cTk.CTkLabel(dataFrame, text="Max Force: ", text_color=txt_color_light, font=TextFontM)
        maxForceLabel.grid(row=2, column=0, padx=20, pady=8)
        impulseLabel=cTk.CTkLabel(dataFrame, text="Impulse: ", text_color=txt_color_light, font=TextFontM)
        impulseLabel.grid(row=3, column=0, padx=20, pady=8)
        avgForceLabel=cTk.CTkLabel(dataFrame, text="Avg. Force: ", text_color=txt_color_light, font=TextFontM)
        avgForceLabel.grid(row=4, column=0, padx=20, pady=8)
        impulseTimeLabel=cTk.CTkLabel(dataFrame, text="Impulse Time: ", text_color=txt_color_light, font=TextFontM)
        impulseTimeLabel.grid(row=5, column=0, padx=20, pady=15)
        gLabel=cTk.CTkLabel(dataFrame, text="0.00 g", text_color=txt_color_light, font=TextFontM)
        gLabel.grid(row=0, column=1, padx=20, pady=8)
        NLabel=cTk.CTkLabel(dataFrame, text="0.000 N", text_color=txt_color_light, font=TextFontM)
        NLabel.grid(row=1, column=1, padx=20, pady=8)
        maxfLabel=cTk.CTkLabel(dataFrame, text="0.000 N", text_color=txt_color_light, font=TextFontM)
        maxfLabel.grid(row=2, column=1, padx=20, pady=8)
        iLabel=cTk.CTkLabel(dataFrame, text="0.000 N*s", text_color=txt_color_light, font=TextFontM)
        iLabel.grid(row=3, column=1, padx=20, pady=8)
        avgfLabel=cTk.CTkLabel(dataFrame, text="0.000 N", text_color=txt_color_light, font=TextFontM)
        avgfLabel.grid(row=4, column=1, padx=20, pady=8)
        itLabel=cTk.CTkLabel(dataFrame, text="0.000 s", text_color=txt_color_light, font=TextFontM)
        itLabel.grid(row=5, column=1, padx=20, pady=8)
        # Function to read serial data and update the label
        def read_serial():
            while True:
                global maxf
                global incoming_data
                global impulse
                global l
                global resetImpulse
                global hum
                global temp
                global avgf
                global impulseTime
                try:
                    data = str(ser.readline().strip())[2:-1]
                    #print(data)
                except serial.SerialException as e:
                    #print("Error", str(e))
                    
                    ser.close()
                    for i in range(20):
                        infoLabel.configure(text="Attempting Reconnect in "+str(round(2-i/10, 1))+"s...")
                        time.sleep(0.1)
                    try:
                        ser.open()
                    except:
                        infoLabel.configure(text="Failed to open port!")
                        time.sleep(0.75)
                    else:
                        infoLabel.configure(text="Waiting for Activation...")
                        resetData(True)
                else:
                    if(data[0].isnumeric()):
                        force = ''
                        tim=''
                        tim2=''
                        hum=''
                        temp= ''
                        for i in range(0, len(data)):
                            if data[i]!=" ":
                                force = force + data[i]
                            else:
                                for j in range((i+1), len(data), 1):
                                    if data[j]!=" ":
                                        tim=tim + data[j]
                                    else:
                                        for k in range((j+1), len(data), 1):
                                            if data[k]!=" ":
                                                hum=hum + data[k]
                                            else:
                                                for h in range((k+1), len(data), 1):
                                                    if data[h]!=" ":
                                                        temp=temp + data[h]
                                                    else:
                                                        for p in range((h+1), len(data), 1):
                                                            if data[p]!=" ":
                                                                tim2=tim2 + data[p]
                                                            else:
                                                                break 
                                                        break  
                                                    
                                                break
                                        break
                                break
                        try:
                            force=float(force)
                            tim=float(tim)/1000
                            hum=float(hum)
                            temp=float(temp)
                            tim2=float(tim2)/1000
                        except ValueError:
                            print("Error: ")
                            print("force: "+str(force))
                            print("tim: "+str(tim))
                            print("hum: "+str(hum))
                            print("temp: "+str(temp))
                            print("tim2: "+str(tim2))
                        else:
                            incoming_data.append(round(force*0.009806652, 3))
                            
                            if(len(ti)!=0 and tim<ti[-1]):
                                resetData(True)
                            else:
                                ti.append(round(tim-cVariable, 3))
                                if(force>maxf):
                                    maxf=force
                                    maxfLabel.configure(text=str(uFormat(round(maxf*0.009806652, 4), 3)+" N"))
                                if(len(ti)>1 and force>20):
                                    if(resetImpulse):
                                        impulse=0
                                        resetImpulse=False
                                    impulse+=float(incoming_data[-1])*(ti[-1]-ti[-2])
                                else:
                                    resetImpulse=True
                                iLabel.configure(text=str(uFormat(impulse, 3)) +  "N*s")
                                gLabel.configure(text=str(uFormat(force, 2))+" g")
                                NLabel.configure(text=str(uFormat(round(force*0.009806652, 4), 3)+ " N"))
                                hValueLabel.configure(text=str(uFormat(hum, 2))+"%")
                                TValueLabel.configure(text=str(uFormat(temp, 2))+"°C")
                                impulseTime=tim2
                                itLabel.configure(text=str(uFormat(tim2, 3))+" s")
                                dateLabel.configure(text=datetime.now().strftime("%d/%m/%Y\n%H:%M:%S"))
                                if(tim2!=0):
                                    avgf=impulse/tim2
                                    avgfLabel.configure(text=str(uFormat(avgf, 3))+" N")
                                else:
                                    avgfLabel.configure(text="0.000 N")
                                if(l%5==0):
                                    updateGraph()
                                l+=1

        
        
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

pressure_label = ttk.Label(root, text="Pressure(Pa):",font=("Helvetica", 20), background="#282424", foreground="#DDDDDD")
pressure_label.grid(row=2, column=0, padx=10, pady=10) 

pressure_entry = ttk.Entry(root, font=("Helvetica", 20))
pressure_entry.insert(0, "101325")
pressure_entry.grid(row=2, column=1, padx=10, pady=10) 
# Add a button to the window with padding
open_button = tk.Button(root, text="Avvia Monitor Zanas", font=("Helvetica", 25), command=open_serial_port)
open_button.grid(row=3, column=0, columnspan=2, pady=40)  # Add open_button to the window

# Run the Tkinter event loop
root.mainloop()
