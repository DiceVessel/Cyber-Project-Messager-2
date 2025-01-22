import socket
import select
import pickle

def encrypt(data):
    return data

def decrypt(data):
    return data


def send_object(socket_to_send,object):
    pickled_object = pickle.dumps(object)
    encrypted_data_to_send = encrypt(pickled_object)
    socket_to_send.sendall(encrypted_data_to_send)

def receive_object(socket_to_receive):
    data = socket_to_receive.recv(1024)
    pickled_object = decrypt(data)
    object = pickle.loads(pickled_object)
    return object

def send_text(socket_to_send,text):
    encrypted_data_to_send = encrypt(text)
    socket_to_send.sendall(encrypted_data_to_send.encode())

def receive_text(socket_to_receive):
    data = socket_to_receive.recv(1024).decode()
    decrypted_data_to_return = decrypt(data)
    return decrypted_data_to_return