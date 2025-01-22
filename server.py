from server_functions import *
import oop
import socket
import select
import pickle
import networking
import db_functions as db

db.create_tables()


list_of_users = []
list_of_groups = []

HOST = '0.0.0.0'
PORT = 100

messages_objects = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# A list to keep track of sockets
sockets_list = [server_socket]

print(f"Server started on {HOST}:{PORT}")

try:
    ################################################################# HANDLE MESSAGE RECEIVING #############################
    while True:
        # Use select to wait for I/O events
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                # New connection
                client_socket, client_address = server_socket.accept()

                new_user_id = provide_user_id(list_of_users)
                #notified_socket.sendall(new_user_id.encode())
                networking.send_text(client_socket,new_user_id)
                new_user_object = oop.User(new_user_id,client_socket)
                list_of_users.append(new_user_object)
                db.add_user(new_user_id)

                sockets_list.append(client_socket)
                print(f"New connection from {client_address}")
            else:
                # Receive message from a client
                try:
                    message = networking.receive_object(notified_socket)
                    if message:
                        print(f"Message received: {message}")
                        messages_objects.append(message)  # Store the message
                    else:
                        # Remove the socket if the connection is closed
                        print(f"Connection closed by {notified_socket.getpeername()}")
                        sockets_list.remove(notified_socket)
                        list_of_users = remove_user_by_socket(list_of_users, notified_socket)
                        notified_socket.close()
                except ConnectionResetError:
                    # Handle client abrupt disconnection
                    print("Client disconnected abruptly")
                    sockets_list.remove(notified_socket)
                    notified_socket.close()
        
        ################################################################# HANDLE MESSAGE RECEIVING ######################
        
        for msg in messages_objects:
            if type(msg.destination_id) == list:
                new_group = create_group(msg, list_of_users, list_of_groups)
                db.create_group(new_group.name, new_group.group_id)
                for member in list_of_users:
                    db.add_user_to_group(new_group.group_id, member.user_id)

                list_of_groups.append(new_group)
                notify_created_group_users(new_group)
                was_message_sent = True
                continue
            elif len(msg.destination_id) >= 7:
                was_message_sent = handle_group_message(msg, list_of_groups)
                db.add_message(msg.source_id,msg.destination_id,msg.content)
            else:
                was_message_sent = handle_message(msg, list_of_users)
                db.add_message(msg.source_id,msg.destination_id,msg.content)
            if not was_message_sent: #message was not sent
                dest_user_not_found(msg, list_of_users)
        messages_objects = []




finally:
    # Clean up sockets on exit
    for sock in sockets_list:
        sock.close()