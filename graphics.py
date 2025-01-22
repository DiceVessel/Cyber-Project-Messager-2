import tkinter as tk
from tkinter import ttk
#import ttkbootstrap as ttk
import oop
                                                                                    #pack: down each other

def create_window(title, size):
    window = tk.Tk()
    window.title(title)
    window.geometry(size)
    
    return window
    
def current_text_in_field(entry):
    return str(entry.get("1.0", tk.END))

'''def add_graphics_message(message_text, message_time, scrollable_frame, canvas): #self is a bool that determines whether the message was sent by the user to who it's displayed
    label = tk.Label(scrollable_frame, text=message_text, bg="lightblue", pady=5)
    label.pack(fill="x", padx=10, pady=5)

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

'''
def add_graphics_message(message_text, message_time, scrollable_frame, canvas, sent_by_user=False):
    message_frame = tk.Frame(scrollable_frame, padx=10, pady=5)
    
    bg_color = "lightgreen" if sent_by_user else "lightblue"
    anchor = "e" if sent_by_user else "w"

    message_label = tk.Label(message_frame, text=message_text, bg=bg_color, anchor=anchor, justify="left", wraplength=400)
    message_label.pack(fill="both", expand=True, padx=(10, 50) if sent_by_user else (50, 10))

    time_label = tk.Label(message_frame, text=message_time, font=("Arial", 8), anchor=anchor)
    time_label.pack(fill="x", padx=(10, 50) if sent_by_user else (50, 10))

    message_frame.pack(fill="x", pady=5, anchor=anchor)

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1.0)  # Scroll to bottom
    