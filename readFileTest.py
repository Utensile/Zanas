import datetime


now = datetime.datetime.now()

# Create the filename based on the date and time
filename = now.strftime("DATA%Y-%m-%d_%H-%M-%S.txt")

# Write "Hello world" into the file
with open(filename, "w") as file:
    file.write("Hello world")