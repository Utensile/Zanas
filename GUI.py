import customtkinter as cTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def temp_event():
    print("button pressed")

app = cTk.CTk()
cTk.set_appearance_mode("Dark")
app.title("my app")
w= app.winfo_screenwidth()
h= app.winfo_screenheight()
x=-10
y=0
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
timeLabel=cTk.CTkLabel(timeFrame, text="16/01/2023 9:00", text_color=txt_color_light, font=TextFontL)
timeLabel.pack(padx=10, pady=10)
startButton=cTk.CTkButton(buttonFrame, text="Start Test", text_color=txt_color_light, font=TextFontL, command=temp_event, width=butt_size, height=butt_size*4*0.25, fg_color=butt_color, corner_radius=corn_rad*1.5)
startButton.grid(row=1, column=0, padx=20, pady=8)
exportButton=cTk.CTkButton(buttonFrame, text="Export Data", text_color=txt_color_light, font=TextFontS, command=temp_event, width=butt_size*4*0.35, height=butt_size*4*0.35*0.4, fg_color=butt_color)
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
ax.figure.set_figheight(3.8)
ax.figure.set_figwidth(6.5)
canvas = FigureCanvasTkAgg(fig, master=graphFrame)
canvas.get_tk_widget().grid(row = 0, column=0, padx=2, pady=2)
ax.plot([0, 1 ,4, 9, 16, 25, 36, 49], [0, 1, 2, 3, 4, 5, 6, 7], linewidth=3, color="#FF0000",label="Force(N)")  
ax.grid()
ax.legend()
ax.set_title("Force(N) over Time(s)")
ax.set_xlabel("Time(s)")
ax.set_ylabel("Force(N)")
ax.fill_between([0, 1 ,4, 9, 16, 25, 36, 49], [0, 1, 2, 3, 4, 5, 6, 7], 0, color="#FF0000", alpha=0.2)
canvas.draw()

#DataFrame
dataFrame=cTk.CTkFrame(app, corner_radius=corn_rad, fg_color=frame_color)
dataFrame.grid(row=10, column=4, rowspan=3, columnspan=3, sticky="nsew", padx=10, pady=10)

dataFrame.grid_rowconfigure((0, 1, 2, 3), weight=1)
dataFrame.grid_columnconfigure((0, 1), weight=1)
gramLabel=cTk.CTkLabel(dataFrame, text="Force(g): ", text_color=txt_color_light, font=TextFontL)
gramLabel.grid(row=0, column=0, padx=20, pady=15)
NewtonLabel=cTk.CTkLabel(dataFrame, text="Force(N): ", text_color=txt_color_light, font=TextFontL)
NewtonLabel.grid(row=1, column=0, padx=20, pady=15)
maxForceLabel=cTk.CTkLabel(dataFrame, text="Max Force(N): ", text_color=txt_color_light, font=TextFontL)
maxForceLabel.grid(row=2, column=0, padx=20, pady=15)
impulseLabel=cTk.CTkLabel(dataFrame, text="Impulse: ", text_color=txt_color_light, font=TextFontL)
impulseLabel.grid(row=3, column=0, padx=20, pady=15)
gLabel=cTk.CTkLabel(dataFrame, text="000.00 g", text_color=txt_color_light, font=TextFontL)
gLabel.grid(row=0, column=1, padx=20, pady=15)
NLabel=cTk.CTkLabel(dataFrame, text="000.00 N", text_color=txt_color_light, font=TextFontL)
NLabel.grid(row=1, column=1, padx=20, pady=15)
maxfLabel=cTk.CTkLabel(dataFrame, text="000.00 N", text_color=txt_color_light, font=TextFontL)
maxfLabel.grid(row=2, column=1, padx=20, pady=15)
iLabel=cTk.CTkLabel(dataFrame, text="000.00 N*s", text_color=txt_color_light, font=TextFontL)
iLabel.grid(row=3, column=1, padx=20, pady=15)

'''
#SHOW GRID
for rows in range(12):
    for cols in range(7):
        frame = cTk.CTkFrame(app)
        frame.grid(row=rows, column=cols, sticky="nsew")
        label=cTk.CTkLabel(frame, text="row: "+str(rows)+" col:"+str(cols))
        label.pack()
'''
app.mainloop()