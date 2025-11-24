#!/usr/bin/python3
"""
Exports to-do list information of all employees to JSON format.
"""
import json
import requests

if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/"

    # Fetch all users
    users = requests.get(url + "users").json()

    # Fetch all todos
    todos = requests.get(url + "todos").json()

    # Prepare the dictionary
    todo_all = {}

    for user in users:
        user_id = user.get("id")
        username = user.get("username")
        
        # Filter tasks for this user
        user_tasks = [task for task in todos if task.get("userId") == user_id]
        
        # Format the tasks list
        formatted_tasks = []
        for task in user_tasks:
            formatted_tasks.append({
                "username": username,
                "task": task.get("title"),
                "completed": task.get("completed")
            })
            
        # Add to main dictionary (key must be string for JSON)
        todo_all[str(user_id)] = formatted_tasks

    # Write to JSON file
    with open("todo_all_employees.json", "w") as jsonfile:
        json.dump(todo_all, jsonfile)
