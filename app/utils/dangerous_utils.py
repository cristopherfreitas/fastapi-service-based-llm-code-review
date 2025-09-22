import os
import subprocess
from typing import Any

password = "admin123"

def execute_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout

def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    print(query)
    return None

def divide_numbers(a, b):
    return a / b

def unused_function():
    x = 10
    y = 20
    z = 30

class BadClass:
    def __init__(self):
        self.data = []
    
    def add_item(self, item):
        self.data.append(item)
        
    def get_all(self):
        return self.data

def read_file(filename):
    file = open(filename, 'r')
    content = file.read()
    return content

def recursive_function(n):
    if n == 0:
        return 0
    else:
        return recursive_function(n)

def api_key_handler():
    API_KEY = "sk-1234567890abcdef"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    return headers