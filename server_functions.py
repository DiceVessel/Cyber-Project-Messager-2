from oop import *
from random import randrange
import networking


def provide_user_id(list_of_users):
    same = True
    while same:
        proposal_id = randrange(1000000)
        same = False
        for user in list_of_users:
            if user.user_id == proposal_id:
                same = True
    return str(proposal_id)

def provide_group_id(list_of_groups):
    same = True
    while same:
        proposal_id = randrange(1000000,10000000)
        same = False
        for group in list_of_groups:
            if group.group_id == proposal_id:
                same = True
    return str(proposal_id)

def send_object_to_id(list_of_users, user_id, object_to_send): #sends a message to a user based on id, return True is message was sent
    for user in list_of_users:
        if user.user_id == user_id:
            networking.send_object(user.user_socket ,object_to_send)
            return True
    print('Error, message was not sent')
    return False

def handle_message(msg_object, list_of_users): #return true is message was sent, false if an error occured
    requested_dst_id = msg_object.destination_id
    send_object_to_id(list_of_users, msg_object.source_id, msg_object)
    return send_object_to_id(list_of_users, requested_dst_id, msg_object)

def dest_user_not_found(message_object, list_of_users):
    server_message_object = Server_Message(0)
    send_object_to_id(list_of_users, message_object.source_id, server_message_object)

def remove_user_by_socket(list_of_users, socket_to_remove):
    for user in list_of_users:
        if user.user_socket == socket_to_remove:
            list_of_users.remove(user)
            return list_of_users
    return list_of_users

def find_user_by_id(id, list_of_users):
    for user in list_of_users:
        if user.user_id == id:
            return user
    return list_of_users[0] #if error occured and user was not found in the list

def find_group_by_id(id, list_of_groups):
    for group in list_of_groups:
        if group.group_id == id:
            return group
    return list_of_groups[0] #if error occured and group was not found in the list

def create_group(build_message, list_of_users, list_of_groups):
    group_name = build_message.content
    group_id = provide_group_id(list_of_groups)
    list_of_participants = []
    list_of_ids = build_message.destination_id
    list_of_ids.append(build_message.source_id)
    for id in list_of_ids:
        matching_user = find_user_by_id(id,list_of_users)
        list_of_participants.append(matching_user)
    return Group(group_name, group_id, list_of_participants)

def notify_created_group_users(group_object):
    group_participants = group_object.list_of_participants
    group_ids = []
    for user in group_participants:
        group_ids.append(user.user_id)
    server_message = Server_Message(1, [group_object.group_id, group_ids])
    for user in group_participants:
        networking.send_object(user.user_socket, server_message)
    
def handle_group_message(message_object, list_of_groups):
    group_object = find_group_by_id(message_object.destination_id, list_of_groups)
    group_users = group_object.list_of_participants
    for user in group_users:
        networking.send_object(user.user_socket, message_object)
    return True
