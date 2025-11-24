#!/usr/bin/python3
"""
Returns information about an employee's TODO list progress
using a REST API.
"""
import requests
import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    # The ID passed as a command-line argument
    employee_id = sys.argv[1]

    # Base URL for the JSONPlaceholder API
    base_url = "https://jsonplaceholder.typicode.com"

    # 1. Fetch User Information (to get the name)
    user_url = "{}/users/{}".format(base_url, employee_id)
    user_response = requests.get(user_url)
    
    # Check if user exists
    if user_response.status_code != 200:
        print("User not found")
        sys.exit(1)
        
    user_data = user_response.json()
    employee_name = user_data.get("name")

    # 2. Fetch User's TODO list
    todos_url = "{}/todos".format(base_url)
    params = {"userId": employee_id}
    todos_response = requests.get(todos_url, params=params)
    todos = todos_response.json()

    # 3. Calculate progress
    total_tasks = len(todos)
    done_tasks = [task for task in todos if task.get("completed") is True]
    number_of_done_tasks = len(done_tasks)

    # 4. Display the formatted output
    # First line: Employee EMPLOYEE_NAME is done with tasks(DONE/TOTAL):
    print("Employee {} is done with tasks({}/{}):".format(
        employee_name, number_of_done_tasks, total_tasks))

    # Subsequent lines: Titles of completed tasks (with tab and space)
    for task in done_tasks:
        print("\t {}".format(task.get("title")))
