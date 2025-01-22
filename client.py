import socket
import pickle
import oop
import threading
import tkinter as tk
from tkinter import ttk
#import ttkbootstrap as ttk
from client_functions import *
import graphics

HOST = '127.0.0.1'
PORT = 100

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
    print(f"Connected to the server at {HOST}:{PORT}")
    user_id = client_socket.recv(1024).decode()
    print("my id is: ", user_id)

    dst_ids_list = []

    ##########################################GRAPHICS########################################
    window = graphics.create_window('Messager', '1600x900')
    
    title_label = ttk.Label(master = window, text='Welcome to Messager', font = 'Calibri 16 bold')
    title_label.pack()

    input_frame = ttk.Frame(master=window)

    
    dropdown_label = ttk.Label(master=input_frame, text="Select ID:")
    dropdown_label.pack(side="left", padx=5)
    id_dropdown = ttk.Combobox(master=input_frame, values=dst_ids_list, state="readonly", width=15)
    id_dropdown.pack(side="left", padx=5)


    id_entry_label = ttk.Label(master=input_frame, text="Or enter ID:")
    id_entry_label.pack(side="left", padx=5)
    id_entry = ttk.Entry(master=input_frame, width=20)
    id_entry.pack(side="left", padx=5)




    entry = tk.Text(master = input_frame)
    button = ttk.Button(master = input_frame, text='Send', command= lambda: send_user_input(client_socket, user_id, dst_ids_list, id_dropdown, id_entry, entry))
    entry.pack(side = 'left', padx = 25)
    button.pack(side = 'right', padx = 25)
    input_frame.pack(pady = 10)
    scroll_frame = ttk.Frame(master=window)
    canvas = tk.Canvas(window)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def configure_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_canvas)

    ##########################################GRAPHICS########################################


    listen_thread = threading.Thread(target=listen_to_server, args=(client_socket,scrollable_frame, canvas,))
    listen_thread.daemon = True
    listen_thread.start()

    



    
    window.mainloop()
    
    
    #while True:
    #    dst_ids_list = send_user_input(client_socket, user_id, dst_ids_list)  

except ConnectionRefusedError:
    print("Could not connect to the server. Make sure it is running.")
except KeyboardInterrupt:
    print("\nClient interrupted. Exiting.")
finally:
    client_socket.close()
    print("Connection closed.")
