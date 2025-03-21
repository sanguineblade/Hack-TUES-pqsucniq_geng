from gpiozero import DistanceSensor 
import tkinter as tk 
from tkinter import font  
from time import sleep  

sensor_1 = DistanceSensor(echo=23, trigger=24, max_distance=10)
sensor_2 = DistanceSensor(echo=17, trigger=27, max_distance=10)
distanceBound = 5

window = tk.Tk()
window.title("Distance Measurement")
custom_font = font.Font(size=30) 
window.geometry("800x400") 

distance_label_1 = tk.Label(window, text="Distance: ", anchor='center', font=custom_font)
distance_label_2 = tk.Label(window, text="Distance: ", anchor='center', font=custom_font)
distance_label_3 = tk.Label(window, text="Posture: ", anchor='center', font=custom_font)

distance_label_1.pack()
distance_label_2.pack() 
distance_label_3.pack()

def isPostureCorrect(distance_1, distance_2):
    return abs(distance_1 - distance_2) < distanceBound

def measure_distance():

    distance_1 = int(sensor_1.distance * 100)
    distance_2 = int(sensor_2.distance * 100) 
    
    distance_label_1.config(fg="red", text="Distance: {} cm\nHi!".format(distance_1))
    distance_label_2.config(fg="red", text="Distance: {} cm\nHi!".format(distance_2))
    distance_label_3.config(fg="red", text="Posture: {} ".format(isPostureCorrect(distance_1, distance_2)))
    window.after(100, measure_distance)  

measure_distance()

window.mainloop()