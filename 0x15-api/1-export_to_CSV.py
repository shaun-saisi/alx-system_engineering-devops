#!/usr/bin/python3
"""Exports to-do list information for a given employee ID to CSV format."""
import csv
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    user_id = sys.argv[1]
    url = "https://jsonplaceholder.typicode.com/"
    
    try:
        user = requests.get(url + "users/{}".format(user_id)).json()
        username = user.get("username")
        todos = requests.get(url + "todos", params={"userId": user_id}).json()
    except requests.RequestException as e:
        print("Error fetching data: {}".format(e))
        sys.exit(1)

    with open("{}.csv".format(user_id), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for todo in todos:
            writer.writerow([user_id, username, todo.get("completed"), todo.get("title")])

