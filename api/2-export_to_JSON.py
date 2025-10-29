"""
A script that, for a given employee ID, fetches TODO list data
and exports it in JSON format.
"""

import json
import sys
import urllib.request

if __name__ == "__main__":
    # Check if exactly one argument (employee ID) is provided
    if len(sys.argv) == 2:

        # Get the employee ID from the command-line argument
        employee_id = sys.argv[1]

        # Define the base URL for the API
        base_url = "https://jsonplaceholder.typicode.com"

        try:
            # --- 1. Get User Information (Employee Name) ---
            # Construct the URL for user data
            user_url = "{}/users/{}".format(base_url, employee_id)

            with urllib.request.urlopen(user_url) as response:
                user_data_bytes = response.read()
                user_data_str = user_data_bytes.decode('utf-8')
                user_data = json.loads(user_data_str)

            # Safely get the employee's username
            username = user_data.get("username")

            # --- 2. Get TODO List Information ---
            # Construct the URL for the user's TODO list
            todos_url = "{}/todos?userId={}".format(base_url, employee_id)

            with urllib.request.urlopen(todos_url) as response:
                todos_data_bytes = response.read()
                todos_data_str = todos_data_bytes.decode('utf-8')
                todos_data = json.loads(todos_data_str)

            # --- 3. Prepare Data for JSON Structure ---
            tasks_list = []
            for task in todos_data:
                # Build the dictionary for this task
                task_dict = {
                    "task": task.get("title"),
                    "completed": task.get("completed"),
                    "username": username
                }
                # Add the task dictionary to our list
                tasks_list.append(task_dict)

            # Create the final dictionary with the USER_ID as the key
            json_output = {employee_id: tasks_list}

            # --- 4. Write Data to JSON File ---
            # The filename is the user ID .json
            filename = "{}.json".format(employee_id)

            # Open the file for writing
            with open(filename, mode='w') as json_file:
                # Dump the dictionary into the file
                json.dump(json_output, json_file)

        except (urllib.error.URLError,
                urllib.error.HTTPError,
                ValueError,
                KeyError) as e:
            # Handle potential network, HTTP, JSON, or key errors
            pass
