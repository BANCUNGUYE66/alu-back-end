#!/usr/bin/python3
"""
A script that, for a given employee ID, fetches TODO list data
and exports it in CSV format.
"""

import csv
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

            # --- 3. Write Data to CSV File ---
            # The filename is the user ID
            filename = "{}.csv".format(employee_id)
            
            # Open the file for writing
            # newline='' is the standard way to write CSVs in Python
            with open(filename, mode='w', newline='') as csv_file:
                # Create a CSV writer
                # We use quoting=csv.QUOTE_ALL to put quotes around every field
                writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                
                # Loop through all tasks and write them to the file
                for task in todos_data:
                    # Get the required data for each row
                    user_id = employee_id
                    task_completed = task.get("completed")
                    task_title = task.get("title")
                    
                    # Write the row in the specified format
                    writer.writerow([user_id,
                                     username,
                                     task_completed,
                                     task_title])

        except (urllib.error.URLError,
                urllib.error.HTTPError,
                ValueError,
                KeyError) as e:
            # Handle potential network, HTTP, JSON, or key errors
            pass


