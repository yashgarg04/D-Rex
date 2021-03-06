import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision 
from torchvision import transforms

import numpy as np 
from PIL import Image

import matplotlib
import matplotlib.pyplot as plt

from helper import *
from ocr_test import *

import cv2

modelPATH = 'D:/Deep Learning Trained Models/Forms/100.pt'
PATH = "D:/Deep Learning Testing Data/DRex/Original Forms/1.jpg"
print("Initiating Trained Model... \n")
model = get_pretrained_model(modelPATH)
model.eval()

def single_pred_pass(imgPATH, shadow):
	original_image = cv2.imread(imgPATH)
	prediction_image = get_prediction_image(original_image, shadow)

	print("Making Prediction and Segmenting Image to get Boxes... \n")
	boxes = custom_predict(model, pil(original_image), pil(prediction_image), False, True)

	return boxes

def single_box_pass(imgPATH):
	boxes = single_pred_pass(PATH, False)
	if len(boxes) == 0:
		print("ACTIVATED SHADOW REMOVAL")
		boxes = single_pass(PATH, True)

	return boxes

def pipeline(imgPATH):
	boxes = single_box_pass(imgPATH)
	print("Using OCR and writing Labels and Info...\n")
	for i in range(len(boxes)):
		PATH = "./Temp/"+str(i)+".png"
		
		label = get_text(PATH, boxes[i], True)
		info = get_text(PATH, boxes[i], False)

		if info == ' ' or label == ' ':
			continue
		else:
			label, info = clean_text(label, info)

			with open("./Labels and Content/labels.txt", 'a', encoding="utf-8") as f:
				f.write(str(label))
				f.write('\n')

			with open("./Labels and Content/content.txt", 'a', encoding="utf-8") as f:
				f.write(str(info))
				f.write('\n')

pipeline(PATH)