import tkinter as tk
import serial
import vispy.scene
import numpy as np

# Create a Tkinter window
window = tk.Tk()
window.title("Serial Data Graph")
window.geometry("800x600")

# Create a VisPy canvas
canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()

# Create a line plot
line = vispy.scene.visuals.Line(pos=np.array([[0, 0]]), color='r', width=2.0)
view.add(line)

# Open the serial port
ser = serial.Serial('COM1', 9600)  # Replace 'COM1' with the appropriate port and baud rate

def update_graph():
    # Read data from the serial port
    data = ser.readline().decode().strip()
    
    try:
        value = float(data)  # Convert the data to a floating-point value
        line.pos = np.vstack([line.pos, [line.pos[-1, 0] + 1, value]])  # Update the line plot data
    except ValueError:
        pass
    
    canvas.update()

# Create a function to periodically update the graph
def animate():
    update_graph()
    window.after(10, animate)  # Update every 10 milliseconds

# Start the animation loop
animate()

# Start the Tkinter event loop
window.mainloop()
