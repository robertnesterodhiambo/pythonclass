import fitz  # PyMuPDF
import tkinter as tk
from PIL import Image, ImageTk

# Load PDF and render first page as an image
pdf_path = "Template.pdf"
doc = fitz.open(pdf_path)
page = doc[0]  # first page

# Render page to a pixmap (image)
zoom = 2  # zoom factor to make image clearer
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)
img_data = pix.tobytes("ppm")

# Use PIL to open image from bytes
from io import BytesIO
img = Image.open(BytesIO(img_data))

# PDF page size
pdf_width = page.rect.width
pdf_height = page.rect.height

# Tkinter window setup
root = tk.Tk()
root.title("Click to get PDF coordinates")

# Convert PIL image to ImageTk for tkinter
tk_img = ImageTk.PhotoImage(img)

canvas = tk.Canvas(root, width=tk_img.width(), height=tk_img.height())
canvas.pack()
canvas_img = canvas.create_image(0, 0, anchor="nw", image=tk_img)

def on_click(event):
    # event.x, event.y are coordinates in the displayed image pixels
    # Need to convert back to PDF coordinates

    # Calculate ratio between PDF coords and image pixels
    x_ratio = pdf_width / tk_img.width()
    y_ratio = pdf_height / tk_img.height()

    pdf_x = event.x * x_ratio
    pdf_y = event.y * y_ratio

    print(f"Clicked at image coords: ({event.x}, {event.y})")
    print(f"Corresponding PDF coords: ({pdf_x:.2f}, {pdf_y:.2f})")

canvas.bind("<Button-1>", on_click)

root.mainloop()
