import tkinter as tk

def add_label():
    """Add a new label to the scrollable frame dynamically."""
    global label_count
    label = tk.Label(scrollable_frame, text=f"Label {label_count}", bg="lightblue", pady=5)
    label.pack(fill="x", padx=10, pady=5)
    label_count += 1
    # Update the scroll region to include the new label
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Create the main window
root = tk.Tk()
root.title("Scrollable Area Example")

# Set up a canvas with a scrollbar
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

canvas = tk.Canvas(frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas for content
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Add a button to add labels dynamically
button = tk.Button(root, text="Add Label", command=add_label)
button.pack(pady=10)

# Configure scrolling behavior
def configure_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_canvas)

# Initialize label counter
label_count = 1

# Start the Tkinter event loop
root.mainloop()
