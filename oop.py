import networking
import server_functions

class Text_Message:
    def __init__(self, source_id, destination_id, content, time=0):
        self.source_id = source_id
        self.destination_id = destination_id
        self.content = content
        self.time = time

    def __str__(self):
        '''return (
            f"Source ID: {self.source_id}\n"
            f"Destination ID: {self.destination_id}\n"
            f"Content: {self.content}\n"
            f"Time: {self.time}"
        )'''
        return (f"[{self.source_id}] to [{self.destination_id}]: {self.content}")


class User:
    def __init__(self, user_id, user_socket):
        self.user_id = user_id
        self.user_socket = user_socket


class Group:
    def __init__(self, name, group_id, list_of_participants):
        self.name = name
        self.group_id = group_id
        self.list_of_participants = list_of_participants
    
    def send_message(self, message_object, server_list_of_users):
        for user in self.list_of_participants:
            message_object_for_user = Text_Message(message_object.source_id, user.user_id, message_object.content)
            server_functions.handle_message(message_object_for_user, server_list_of_users)


class Server_Message:
    def __init__(self, message_code, description='0'):
        message_code_list = ['DESTINATION USER NOT FOUND', 'NEW GROUP CREATED']
        self.message_code = message_code
        if description == '0':
            self.description = message_code_list[self.message_code]
        else:
            self.description = description

class Chat:
    def __init__(self, title, last_message):
        self.title = title
        self.last_message = last_message