import cv2
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)
    return thresh

def detect_answers(thresh_image):
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bubbles = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if 0.8 < aspect_ratio < 1.2 and 15 < w < 50:
            bubbles.append((x, y, w, h))
    
    bubbles = sorted(bubbles, key=lambda b: (b[1], b[0]))
    return bubbles

def extract_answers(thresh_image, bubbles):
    responses = []
    for i in range(0, len(bubbles), 4):
        row = bubbles[i:i+4]
        row = sorted(row, key=lambda b: b[0])
        filled = [np.sum(thresh_image[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]) for b in row]
        marked = np.argmin(filled)
        responses.append(chr(65 + marked))
    return responses

def save_results(index_number, answers, output_file="results.csv"):
    df = pd.DataFrame([[index_number] + answers], columns=["Index"] + [f"Q{i+1}" for i in range(len(answers))])
    df.to_csv(output_file, index=False, mode='a', header=False)

def process_omr():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if not image_path:
        return
    
    index_number = index_entry.get()
    if not index_number.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid index number.")
        return
    
    thresh = preprocess_image(image_path)
    bubbles = detect_answers(thresh)
    answers = extract_answers(thresh, bubbles)
    save_results(index_number, answers)
    
    messagebox.showinfo("Success", "Results saved successfully.")

# GUI Setup
root = tk.Tk()
root.title("OMR Scanner")
root.geometry("400x200")

tk.Label(root, text="Enter Index Number:").pack()
index_entry = tk.Entry(root)
index_entry.pack()

tk.Button(root, text="Select OMR Image", command=process_omr).pack()

root.mainloop()
