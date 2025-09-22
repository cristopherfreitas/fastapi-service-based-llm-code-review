"""
This file contains intentionally problematic code for testing Claude Code review.
DO NOT USE IN PRODUCTION - TEST PURPOSES ONLY
"""
import os
import subprocess
from typing import Any

# Security Issue: Hardcoded credentials
PASSWORD = "admin123"
API_KEY = "sk-prod-1234567890abcdef"

def sql_injection_vulnerable(user_id: str):
    """Security Issue: SQL Injection vulnerability"""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    # This is vulnerable to SQL injection
    return query

def command_injection(filename: str):
    """Security Issue: Command injection via subprocess"""
    cmd = f"cat {filename}"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout

def divide_by_zero(x: int, y: int):
    """Bug: No zero division check"""
    return x / y

def resource_leak():
    """Resource leak: File not closed"""
    f = open("data.txt", "r")
    content = f.read()
    # Missing f.close()
    return content

def infinite_recursion(n: int):
    """Bug: Infinite recursion"""
    if n == 0:
        return 0
    return infinite_recursion(n)  # Never decrements n

class BadCode:
    """Poor code quality example"""
    
    def __init__(self):
        self.data = []
    
    def process(self, item):
        """Bad practice: Bare except clause"""
        try:
            self.data.append(item)
            result = 10 / item
        except:  # Bad: bare except
            pass  # Bad: silently ignoring errors
        
    def unused_method(self):
        """Code smell: Unused method"""
        x = 10
        y = 20
        # Variables defined but never used
        pass

def eval_user_input(user_input: str):
    """CRITICAL Security Issue: Using eval on user input"""
    try:
        result = eval(user_input)
        return result
    except Exception as e:
        return f"Error: {e}"

# Performance issue: Inefficient algorithm
def find_duplicates(items: list):
    """O(n²) complexity when it could be O(n)"""
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates