import json
from datetime import datetime, timedelta
file_path='message.json'
current_time = datetime.now()







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





def load_messages(student_id,file_path):
    """ this function fetch the message corresponding to the student id from the message.json source file also deleted 12 hrs older messages       """
    delete_message(file_path) 
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
        









""" 
todo1: first fetch the time when message was send 
todo2: add 12 hrs to fetched time 
todo3: check whether present time is matched with added 12 hr time 
todo4: if matched then delete the message automatically 

"""





    

# Step 2: Get the current datetime
# Step 3: Define a function to parse and filter messages
def is_within_12_hours(message):
    try:
        # Combine date and time from the message
        message_time = datetime.strptime(
            f"{message['date']} {message['time']}",
            "%d-%m-%Y %H:%M:%S"
        )
        # Check if the message is within 12 hours
        return current_time - message_time <= timedelta(hours=12)
    except KeyError:
        # If date or time is missing, keep the message
        return True
    
def delete_message(filepath):
    # Step 1: Load JSON data from file
    with open(filepath, 'r') as file:
        data = json.load(file)

    # Step 4: Filter messages that are within 12 hours
    data['users'] = [user for user in data['users'] if is_within_12_hours(user)]

    # Step 5: Write the updated data back to the file
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

    print("Old messages have been deleted successfully!")




def dump_community_message(message,file_name):
    message = message 
    new_message = {"message":message, "date":now.strftime("%d-%m-%Y"),"time":now.strftime("%H:%M:%S")}

    # Path to the JSON file
    file_path = file_name

    # Read existing data
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {"messages": []}  # Initialize if file doesn't exist

    # Add new data
    data["messages"].append(new_message)

    # Write updated data back to the file
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)



# dump_community_message("hello from community","community_message.json")


def load_community_messages(file_path):
      delete_community_messages(file_path)
      with open(file_path, "r") as json_file:
        data = json.load(json_file)
        list_messages = data['messages']

        # Collect all messages for the given student_id
        found_messages = [messages['message'] for messages in list_messages ]

        # Print all messages or a message if no messages were found
        if found_messages:
            # print(f"Messages from student {student_id}:")
            # for message in found_messages:
            #     print(message)
            return found_messages
        else:
            # print(f"Student with ID {student_id} not found.")
            message = f"No messages Yet!."
            return message
  

def delete_community_messages(filepath):
  # Step 1: Load JSON data from file
    with open(filepath, 'r') as file:
        data = json.load(file)

    # Step 4: Filter messages that are within 12 hours
    data['messages'] = [user for user in data['messages'] if is_within_12_hours(user)]

    # Step 5: Write the updated data back to the file
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

    print("Old messages have been deleted successfully!")
