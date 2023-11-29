import tkinter as tk
from tkinter import filedialog, Scrollbar
import cv2
from PIL import Image, ImageTk, ImageChops
import numpy as np

def open_file_dialog():
	file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg;*.jpe;*.jfif"), ("All Files", "*.*")])
	if file_path:
		process_file(file_path)

def process_file(file_path):
	try:
		place_file(file_path)
		error_label.config(text=f"No Error")
	except Exception as e:
		error_label.config(text=f"Error: {str(e)}")

def place_file(file_path):
	inputImageCV2 = cv2.imread(file_path, 0)
	inputImage = Image.fromarray(inputImageCV2)
	width, height = inputImage.size
	newwidth = int(float(width)/(float(height)/200))
	inputImage = inputImage.resize((newwidth, 200))
	labelInputImage = ImageTk.PhotoImage(inputImage)
	imageLabelInput.config(image=labelInputImage)
	imageLabelInput.image = labelInputImage

	invert_file(inputImageCV2, newwidth)
	threshold_file(inputImageCV2, newwidth)
	log_transform_file(inputImageCV2, newwidth)
	exp_transform_file(inputImageCV2, newwidth)

def invert_file(inputImageCV2, newwidth):
	invertedImageCV2 = np.invert(inputImageCV2)
	inverted_image = Image.fromarray(invertedImageCV2)
	inverted_image = inverted_image.resize((newwidth, 200))
	labelInvertedImage = ImageTk.PhotoImage(inverted_image)
	imageLabelOutputInverted.config(image=labelInvertedImage)
	imageLabelOutputInverted.image = labelInvertedImage

def threshold_file(inputImageCV2, newwidth):
	thresholder = lambda t: 0 if t<128 else 255
	vfunc = np.vectorize(thresholder)
	thresholdImageCV2 = vfunc(inputImageCV2)
	thresholdImage = Image.fromarray(thresholdImageCV2)
	thresholdImage = thresholdImage.resize((newwidth, 200))
	labelThresholdImage = ImageTk.PhotoImage(thresholdImage)
	imageLabelOutputThreshold.config(image=labelThresholdImage)
	imageLabelOutputThreshold.image = labelThresholdImage

def log_transform_file(inputImageCV2, newwidth):
	c = 255 / np.log(1 + np.max(inputImageCV2))
	logger = lambda t: c * (np.log(t + 1))
	vfunc = np.vectorize(logger)
	logarithmicImageCV2 = vfunc(inputImageCV2)
	logarithmicImage = Image.fromarray(logarithmicImageCV2)
	logarithmicImage = logarithmicImage.resize((newwidth, 200))
	labelLogarithmicImage = ImageTk.PhotoImage(logarithmicImage)
	imageLabelOutputLogarithmic.config(image=labelLogarithmicImage)
	imageLabelOutputLogarithmic.image = labelLogarithmicImage

def exp_transform_file(inputImageCV2, newwidth):
	expper = lambda t: 255 * ((t/255) ** 2)
	vfunc = np.vectorize(expper)
	exponentialImageCV2 = vfunc(inputImageCV2)
	exponentialImage = Image.fromarray(exponentialImageCV2)
	exponentialImage = exponentialImage.resize((newwidth, 200))
	labelExponentialImage = ImageTk.PhotoImage(exponentialImage)
	imageLabelOutputExponential.config(image=labelExponentialImage)
	imageLabelOutputExponential.image = labelExponentialImage

root = tk.Tk()
root.state('zoomed')
root.title("Image Enhancing")

open_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_button.place(x=0, y=0)

error_label = tk.Label(root)
error_label.place(x=65, y=2)

selected_file_label = tk.Label(root, text="Input Image")
selected_file_label.place(x=0, y=30)

imageLabelInput = tk.Label(root)
imageLabelInput.place(x=0, y=50)

output_file_label_inverted = tk.Label(root, text="Inverting")
output_file_label_inverted.place(x=0, y=260)

imageLabelOutputInverted = tk.Label(root)
imageLabelOutputInverted.place(x=0, y=280)

output_file_label_threshold = tk.Label(root, text="Thresholding (t = 128)")
output_file_label_threshold.place(x=400, y=30)

imageLabelOutputThreshold = tk.Label(root)
imageLabelOutputThreshold.place(x=400, y=50)

output_file_label_logarithmic = tk.Label(root, text="Logarithmic")
output_file_label_logarithmic.place(x=400, y=260)

imageLabelOutputLogarithmic = tk.Label(root)
imageLabelOutputLogarithmic.place(x=400, y=280)

output_file_label_exponential = tk.Label(root, text="Exponential (γ = 2)")
output_file_label_exponential.place(x=800, y=30)

imageLabelOutputExponential = tk.Label(root)
imageLabelOutputExponential.place(x=800, y=50)

root.mainloop()
