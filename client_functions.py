import socket
import networking
import pickle
import oop
import graphics
import tkinter as tk
from tkinter import ttk

def display_message(message_object, scrollable_frame, canvas):
    print("Message from server", message_object)
    graphics.add_graphics_message(message_object.content, message_object.time, scrollable_frame, canvas)

def handle_server_message(message_object):
    message_code = message_object.message_code
    if message_code == 0:
        print('Error, previous message was not sent') ######### Expand later on
    elif message_code == 1:
        print(f"New group created! Group id: {message_object.description[0]}, participants: {message_object.description[1]}")
    else:
        print("Message from server not recognized")

def listen_to_server(sock,scrollable_frame, canvas):
    while True:
        try:
            message = networking.receive_object(sock)
            if not message:
                print("Server connection closed.")
                break
            if type(message) == oop.Server_Message:
                handle_server_message(message)
            else:
                display_message(message,scrollable_frame, canvas)
        except Exception as e:
            print(f"Error: {e}")
            break

def send_user_input(sock, src_id, dst_ids_list, id_dropdown, id_entry, message_entry):
    """
     sending messages from client to server.
    """
    
    dst_id = id_dropdown.get() or id_entry.get().strip()  # get dest id ( dropdown or entry)

    if not dst_id:
        print("Please enter or select a destination ID.")
        return

    if dst_id not in dst_ids_list:
        dst_ids_list.append(dst_id)
        id_dropdown['values'] = dst_ids_list  

    message_text = message_entry.get("1.0", tk.END).strip()
    if not message_text:
        print("Cannot send an empty message.")
        return

    message_object = oop.Text_Message(src_id, dst_id, message_text)

    try:
        networking.send_object(sock, message_object)
        print(f"Message sent to {dst_id}: {message_text}")
    except Exception as e:
        print(f"Error sending message: {e}")
        return

    id_entry.delete(0, tk.END)
    message_entry.delete("1.0", tk.END)
