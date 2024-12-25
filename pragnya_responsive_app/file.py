import json
from datetime import datetime
now = datetime.now()
def dump_messages(student_id,student_message,file_name,):
    """ this function fetch the message from the admin and store it to the message.json file      """
    count = 1
    # New user data to add
    new_user = {"id": student_id , "message": student_message, "date":now.strftime("%d-%m-%Y"),"time":now.strftime("%H:%M:%S")}

    # Path to the JSON file
    file_path = file_name

    # Read existing data
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {"users": []}  # Initialize if file doesn't exist

    # Add new data
    data["users"].append(new_user)

    # Write updated data back to the file
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


student_id = 3 

file_path='messages.json'


def load_messages(student_id,file_path):
    """ this function fetch the message corresponding to the student id from the message.json source file      """
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        list_messages = data['users']

        # Collect all messages for the given student_id
        found_messages = [user['message'] for user in list_messages if user['id'] == student_id]

        # Print all messages or a message if no messages were found
        if found_messages:
            # print(f"Messages from student {student_id}:")
            # for message in found_messages:
            #     print(message)
            return found_messages
        else:
            # print(f"Student with ID {student_id} not found.")
            message = f"Student with ID {student_id} not found."
            return message