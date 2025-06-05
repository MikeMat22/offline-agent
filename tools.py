import os
import datetime
import json
from typing import Dict, Any

class Tools:
    @staticmethod
    def get_current_time() -> str:
        """Get current date and time"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def read_file(filepath: str) -> str:
        """Read contents of a file - checks if file exists first"""
        try:
            if not os.path.exists(filepath):
                return f"File '{filepath}' does not exist. Available files: {', '.join(os.listdir('.'))}"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:1000] + "..." if len(content) > 1000 else content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    @staticmethod
    def write_file(filepath: str, content: str) -> str:
        """Write content to a file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    @staticmethod
    def list_directory(path: str = ".") -> str:
        """List contents of a directory"""
        try:
            items = os.listdir(path)
            if not items:
                return "Directory is empty"
            return "Files and folders:\n" + "\n".join(f"- {item}" for item in sorted(items))
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    @staticmethod
    def file_exists(filepath: str) -> str:
        """Check if a file exists"""
        return f"File '{filepath}' {'exists' if os.path.exists(filepath) else 'does not exist'}"
    
    @staticmethod
    def calculate(expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Only allow safe operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Only basic math operations allowed"
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error calculating: {str(e)}"

# Updated tool registry
AVAILABLE_TOOLS = {
    "get_current_time": Tools.get_current_time,
    "read_file": Tools.read_file,
    "write_file": Tools.write_file,
    "list_directory": Tools.list_directory,
    "file_exists": Tools.file_exists,
    "calculate": Tools.calculate,
}

def get_tools_description() -> str:
    """Return description of available tools"""
    return """
Available tools:
1. get_current_time() - Get current date and time
2. read_file(filepath) - Read contents of a file (checks if exists first)
3. write_file(filepath, content) - Write content to a file
4. list_directory(path) - List directory contents
5. file_exists(filepath) - Check if a file exists
6. calculate(expression) - Perform basic math calculations

IMPORTANT: Always check if files exist before trying to read them!
To use a tool, format your response as: TOOL: tool_name(parameters)
"""