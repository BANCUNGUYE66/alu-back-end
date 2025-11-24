#!/usr/bin/python3
"""
Exports to-do list information for a given employee ID to CSV format.
"""
import csv
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./1-export_to_CSV.py <employee_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    url = "https://jsonplaceholder.typicode.com/"

    # Fetch user data to get the username
    user = requests.get(url + "users/{}".format(user_id)).json()
    username = user.get("username")

    # Fetch todos for the specific user
    todos = requests.get(url + "todos", params={"userId": user_id}).json()

    # Write to CSV
    with open("{}.csv".format(user_id), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for task in todos:
            writer.writerow([user_id, username, str(task.get("completed")),
                             task.get("title")])
