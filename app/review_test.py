"""
Test file with intentional issues for code review
"""
import os
import subprocess

# ISSUE: Hardcoded sensitive credentials
DATABASE_PASSWORD = "admin123"
API_SECRET = "sk-live-production-key-12345"

def process_user_input(user_data):
    # ISSUE: SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE name = '{user_data}'"
    print(f"Executing: {query}")
    return query

def run_system_command(file_path):
    # ISSUE: Command injection vulnerability
    cmd = f"cat {file_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout

def calculate_average(numbers):
    # ISSUE: No error handling for empty list or zero division
    total = sum(numbers)
    return total / len(numbers)

def load_config():
    # ISSUE: Resource leak - file not closed
    file = open("config.json", "r")
    data = file.read()
    # Missing: file.close()
    return data

def dangerous_eval(expression):
    # CRITICAL: Using eval on user input
    try:
        result = eval(expression)
        return result
    except:  # ISSUE: Bare except clause
        pass  # ISSUE: Silently ignoring errors

class DataProcessor:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        # ISSUE: No validation or error handling
        self.items.append(item)
    
    def find_duplicates(self):
        # ISSUE: Inefficient O(n²) algorithm
        duplicates = []
        for i in range(len(self.items)):
            for j in range(i + 1, len(self.items)):
                if self.items[i] == self.items[j]:
                    if self.items[i] not in duplicates:
                        duplicates.append(self.items[i])
        return duplicates

def recursive_function(n):
    # ISSUE: Infinite recursion - n is never decremented
    if n == 0:
        return 0
    return recursive_function(n)

# ISSUE: Unused function
def unused_helper():
    x = 10
    y = 20
    z = x + y
    # z is calculated but never returned or used