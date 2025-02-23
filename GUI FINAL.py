import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def load_image():
    global img_path
    img_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if img_path:
        image_label.config(text=f"Image Loaded: {img_path.split('/')[-1]}")
        
def encrypt_message():
    msg = msg_entry.get()
    password = passcode_entry.get()

    if not msg or not password:
        messagebox.showwarning("Input Error", "Please enter a message and passcode!")
        return

    try:
        img = cv2.imread(img_path)
        d = {chr(i): i for i in range(255)}
        c = {i: chr(i) for i in range(255)}

        m, n, z = 0, 0, 0
        for i in range(len(msg)):
            img[n, m, z] = d[msg[i]]
            n += 1
            m += 1
            z = (z + 1) % 3

        encrypted_img_path = "encryptedImage.jpg"
        cv2.imwrite(encrypted_img_path, img)
        messagebox.showinfo("Success", "Message encrypted successfully!")
        
        os.system(f"start {encrypted_img_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error encrypting the image: {e}")

        
def decrypt_message():
    msg = msg_entry.get()
    password = passcode_entry.get()

    if not msg or not password:
        messagebox.showwarning("Input Error", "Please enter a message and passcode!")
        return

    pas = passcode_entry.get()
    if password != pas:
        messagebox.showerror("Authentication Failed", "Incorrect passcode!")
        return

    try:
        img = cv2.imread("encryptedImage.jpg")
        c = {i: chr(i) for i in range(255)}

        message = ""
        m, n, z = 0, 0, 0
        for i in range(len(msg)):
            message += c[img[n, m, z]]
            n += 1
            m += 1
            z = (z + 1) % 3

        messagebox.showinfo("Decrypted Message", f"Decrypted message: {message}")
    except Exception as e:
        messagebox.showerror("Error", f"Error decrypting the image: {e}")

root = tk.Tk()
root.title("Image Encryption & Decryption")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="Image Encryption & Decryption", font=("Helvetica", 14, "bold"), bg="#f0f0f0", fg="#4CAF50")
title_label.pack(pady=10)

image_label = tk.Label(root, text="No Image Loaded", font=("Helvetica", 10), bg="#f0f0f0", fg="#FF5722")
image_label.pack(pady=5)

load_button = tk.Button(root, text="Load Image", command=load_image, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
load_button.pack(pady=5)

msg_label = tk.Label(root, text="Enter Secret Message:", font=("Helvetica", 10), bg="#f0f0f0", fg="#2196F3")
msg_label.pack(pady=5)
msg_entry = tk.Entry(root, width=40, font=("Helvetica", 10))
msg_entry.pack(pady=5)

passcode_label = tk.Label(root, text="Enter Passcode:", font=("Helvetica", 10), bg="#f0f0f0", fg="#2196F3")
passcode_label.pack(pady=5)
passcode_entry = tk.Entry(root, width=40, font=("Helvetica", 10), show="*")
passcode_entry.pack(pady=5)

encrypt_button = tk.Button(root, text="Encrypt Message", command=encrypt_message, bg="#8BC34A", fg="white", font=("Helvetica", 10, "bold"))
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(root, text="Decrypt Message", command=decrypt_message, bg="#FF9800", fg="white", font=("Helvetica", 10, "bold"))
decrypt_button.pack(pady=10)

root.mainloop()
