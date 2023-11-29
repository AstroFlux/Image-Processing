import tkinter as tk
from tkinter import filedialog, Scrollbar
import cv2
from PIL import Image, ImageTk, ImageChops
import numpy as np
import os
import time

def open_file_dialog():
	file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg;*.jpe;*.jfif"), ("All Files", "*.*")])
	if file_path:
		process_file(file_path)

def process_file(file_path):
	try:
		place_file(file_path)
	except Exception as e:
		error_label.config(text=f"Error: {str(e)}")

def place_file(file_path):
	error_label.config(text="Processing")

	inputImageCV2 = cv2.imread(file_path, 0)
	inputImage = Image.fromarray(inputImageCV2)
	width, height = inputImage.size
	newwidth = int(float(width)/(float(height)/200))
	inputImage = inputImage.resize((newwidth, 200))
	labelInputImage = ImageTk.PhotoImage(inputImage)
	imageLabelInput.config(image=labelInputImage)
	imageLabelInput.image = labelInputImage
	textLabelInput.place(x=0, y=30)
	imageLabelInput.place(x=0, y=50)

	avgFilter(inputImageCV2, newwidth)
	error_label.config(text="No Error")

def avgFilter(inputImageCV2, newwidth):
	filter = np.array([
		[1, 1, 1],
		[1, 1, 1],
		[1, 1, 1],
	])/9
	smoothedImage = cv2.filter2D(inputImageCV2, -1, filter)
	avgFilterImage = Image.fromarray(smoothedImage)
	avgFilterImage = avgFilterImage.resize((newwidth, 200))
	labelAvgFilterImage = ImageTk.PhotoImage(avgFilterImage)
	imageLabelOutputAvgFilter.config(image=labelAvgFilterImage)
	imageLabelOutputAvgFilter.image = labelAvgFilterImage
	textLabelOutputAvgFilter.place(x=0, y=260)
	imageLabelOutputAvgFilter.place(x=0, y=280)

root = tk.Tk()
root.state('zoomed')
root.title("Image Smoothing/Blurring")

open_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_button.place(x=0, y=0)

error_label = tk.Label(root)
error_label.place(x=65, y=2)

textLabelInput = tk.Label(root, text="Input Image")
imageLabelInput = tk.Label(root)

textLabelOutputAvgFilter = tk.Label(root, text="Average Filter")
imageLabelOutputAvgFilter = tk.Label(root)

root.mainloop()