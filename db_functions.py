import sqlite3

DB_NAME = "text_messaging_app.db"

def create_tables():
    """Creates the necessary tables in the database."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
    """)

    # contacts table - not using currently
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        contact_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (contact_id) REFERENCES users (user_id)
    )
    """)

    # messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        message_text TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES users (user_id),
        FOREIGN KEY (receiver_id) REFERENCES users (user_id)
    )
    """)

    # groups table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        group_name TEXT
    )
    """)

    # group members table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS group_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (group_id) REFERENCES groups (group_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)

    connection.commit()
    connection.close()

def add_user(user_id):
    """Adds a new user with a specific user_id to the users table."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO users (user_id)
    VALUES (?)
    """, (user_id,))

    connection.commit()
    connection.close()

def add_contact(user_id, contact_id):
    """Adds a contact to a user's contact list."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO contacts (user_id, contact_id)
    VALUES (?, ?)
    """, (user_id, contact_id))

    connection.commit()
    connection.close()

def add_message(sender_id, receiver_id, message_text):
    """Adds a message from a sender to a receiver."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO messages (sender_id, receiver_id, message_text)
    VALUES (?, ?, ?)
    """, (sender_id, receiver_id, message_text))

    connection.commit()
    connection.close()

def create_group(group_id, group_name=None):
    """Creates a new group with a specific group_id."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO groups (group_id, group_name)
    VALUES (?, ?)
    """, (group_id, group_name))

    connection.commit()
    connection.close()

def add_user_to_group(group_id, user_id):
    """Adds a user to a group."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO group_members (group_id, user_id)
    VALUES (?, ?)
    """, (group_id, user_id))

    connection.commit()
    connection.close()

def get_group_members(group_id):
    """Retrieves all members of a group."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT user_id FROM group_members
    WHERE group_id = ?
    """, (group_id,))

    members = cursor.fetchall()
    connection.close()
    return [member[0] for member in members]
