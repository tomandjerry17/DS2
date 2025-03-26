import tkinter as tk
from PIL import Image, ImageTk  # Pillow is needed for JPG support

# Convert JPG to PNG (only runs once to create 'logo.png')
image = Image.open("logo.jpg")
image.save("logo.png")  # Save as PNG

# Create main window
root = tk.Tk()
root.title("Custom Icon Example")

# Load and set window icon using PNG
icon_path = "logo.png"  # Use the new PNG file
root.iconphoto(False, tk.PhotoImage(file=icon_path))

# Create a simple label
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
label.pack(pady=20)

root.mainloop()
