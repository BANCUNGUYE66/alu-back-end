#!/usr/bin/python3
"""
A script that, for a given employee ID, returns information
about his/her TODO list progress.
"""

import json
import sys
import urllib.request

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) == 2:
        # Get the employee ID from the command-line argument
        employee_id = sys.argv[1]
        
        # Define the base URL for the API
        base_url = "https://jsonplaceholder.typicode.com"
        
        try:
            # --- 1. Get User Information ---
            # Construct the URL for user data
            user_url = "{}/users/{}".format(base_url, employee_id)
            
            # Send the request using urllib
            with urllib.request.urlopen(user_url) as response:
                # Read the response and decode it as UTF-8
                user_data_bytes = response.read()
                user_data_str = user_data_bytes.decode('utf-8')
                # Parse the JSON string
                user_data = json.loads(user_data_str)
            
            # Safely get the employee name
            employee_name = user_data.get("name")

            # --- 2. Get TODO List Information ---
            # Construct the URL for the user's TODO list
            todos_url = "{}/todos?userId={}".format(base_url, employee_id)
            
            # Send the request using urllib
            with urllib.request.urlopen(todos_url) as response:
                # Read the response and decode it
                todos_data_bytes = response.read()
                todos_data_str = todos_data_bytes.decode('utf-8')
                # Parse the JSON string
                todos_data = json.loads(todos_data_str)

            # --- 3. Process the Data ---
            total_tasks = 0
            done_tasks = 0
            completed_task_titles = []

            for task in todos_data:
                total_tasks += 1
                # Check if the task is completed
                if task.get("completed"):
                    done_tasks += 1
                    # Add the title to our list
                    completed_task_titles.append(task.get("title"))

            # --- 4. Display the Formatted Output ---
            if employee_name:
                # Print the summary line
                print("Employee {} is done with tasks({}/{}):".format(
                    employee_name, done_tasks, total_tasks))
                
                # Print each completed task title
                for title in completed_task_titles:
                    # Format with 1 tab and 1 space
                    print("\t {}".format(title))

        except (urllib.error.URLError,
                urllib.error.HTTPError,
                ValueError,
                KeyError) as e:
            # Handle potential network, HTTP, JSON, or key errors
            pass


