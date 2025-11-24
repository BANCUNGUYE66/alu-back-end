#!/usr/bin/python3
"""
A script that fetches all TODO list data for all employees
and exports it to a JSON file in a specific format.
"""

import json
import sys
import urllib.request

if __name__ == "__main__":
    # Define the base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"
    # Define the output filename
    filename = "todo_all_employees.json"

    try:
        # --- 1. Get All Users ---
        # Construct the URL for all users
        users_url = "{}/users".format(base_url)

        with urllib.request.urlopen(users_url) as response:
            users_data_bytes = response.read()
            users_data_str = users_data_bytes.decode('utf-8')
            users_data = json.loads(users_data_str)

        # --- 2. Get All TODOs ---
        # Construct the URL for all TODOs
        todos_url = "{}/todos".format(base_url)

        with urllib.request.urlopen(todos_url) as response:
            todos_data_bytes = response.read()
            todos_data_str = todos_data_bytes.decode('utf-8')
            todos_data = json.loads(todos_data_str)

        # --- 3. Create a Map of User ID to Username ---
        # This is efficient so we don't have to loop users_data
        # inside the main loop.
        user_map = {}
        for user in users_data:
            user_map[user.get("id")] = user.get("username")

        # --- 4. Build the Required Data Structure ---
        # The structure is a dictionary where keys are user IDs
        # and values are lists of task dictionaries.
        all_tasks_by_user = {}

        for todo in todos_data:
            user_id = todo.get("userId")
            username = user_map.get(user_id)

            # Check if the user ID from the todo exists in our map
            if username:
                # If this is the first task for this user, create an empty list
                if user_id not in all_tasks_by_user:
                    all_tasks_by_user[user_id] = []

                # Build the task dictionary in the required format
                task_dict = {
                    "username": username,
                    "task": todo.get("title"),
                    "completed": todo.get("completed")
                }

                # Add this task to the list for this user
                all_tasks_by_user[user_id].append(task_dict)

        # --- 5. Write Data to JSON File ---
        with open(filename, mode='w') as json_file:
            # Dump the final dictionary into the JSON file
            json.dump(all_tasks_by_user, json_file)

    except (urllib.error.URLError,
            urllib.error.HTTPError,
            ValueError,
            KeyError) as e:
        # Handle potential network, HTTP, JSON, or key errors
        pass

