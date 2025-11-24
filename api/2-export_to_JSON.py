#!/usr/bin/python3
"""
Exports to-do list information for a given employee ID to JSON format.
"""
import json
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./2-export_to_JSON.py <employee_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    url = "https://jsonplaceholder.typicode.com/"

    # Fetch user data to get the username
    user = requests.get(url + "users/{}".format(user_id)).json()
    username = user.get("username")

    # Fetch todos for the specific user
    todos = requests.get(url + "todos", params={"userId": user_id}).json()

    # Create the dictionary structure
    dictionary = {user_id: []}
    for task in todos:
        dictionary[user_id].append({
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": username
        })

    # Write to JSON file
    with open("{}.json".format(user_id), "w") as jsonfile:
        json.dump(dictionary, jsonfile)
