import requests
import json
import re
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from config import Config
from tools import AVAILABLE_TOOLS, get_tools_description

class OfflineAgent:
    def __init__(self, model: str = None):
        self.console = Console()
        self.model = model or Config.DEFAULT_MODEL
        self.conversation_history = []
        self.system_prompt = f"""You are a helpful AI assistant running offline. You have access to several tools to help users.

{get_tools_description()}

IMPORTANT RULES:
1. NEVER assume files exist - always check first with file_exists() or list_directory()
2. Only use tools when specifically needed - don't make up file operations
3. For general knowledge questions (like "tell me about the universe"), use your built-in knowledge
4. Only use file tools when the user specifically asks about files or wants to create/read files
5. Be direct and helpful without unnecessary tool calls

When you want to use a tool, include it in your response using the format: TOOL: tool_name(parameters)

Be helpful, concise, and always explain what you're doing."""

    def call_ollama(self, prompt: str) -> str:
        """Make API call to Ollama"""
        try:
            response = requests.post(
                f"{Config.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": Config.TEMPERATURE,
                        "num_predict": Config.MAX_TOKENS
                    }
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except json.JSONDecodeError:
            return "Error: Invalid response from Ollama"

    def execute_tool(self, tool_call: str) -> str:
        """Execute a tool call"""
        try:
            # Parse tool call: TOOL: tool_name(parameters)
            match = re.match(r'TOOL:\s*(\w+)\((.*?)\)', tool_call.strip())
            if not match:
                return "Error: Invalid tool call format"
            
            tool_name = match.group(1)
            params_str = match.group(2)
            
            if tool_name not in AVAILABLE_TOOLS:
                return f"Error: Tool '{tool_name}' not found"
            
            tool_func = AVAILABLE_TOOLS[tool_name]
            
            # Parse parameters
            if params_str.strip():
                # Simple parameter parsing (you might want to improve this)
                if ',' in params_str:
                    params = [p.strip().strip('"\'') for p in params_str.split(',')]
                    result = tool_func(*params)
                else:
                    param = params_str.strip().strip('"\'')
                    result = tool_func(param)
            else:
                result = tool_func()
            
            return str(result)
        except Exception as e:
            return f"Error executing tool: {str(e)}"

    def process_response(self, response: str) -> str:
        """Process agent response and execute any tool calls"""
        lines = response.split('\n')
        processed_lines = []
        
        for line in lines:
            if line.strip().startswith('TOOL:'):
                tool_result = self.execute_tool(line)
                processed_lines.append(f"[Tool Result] {tool_result}")
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)

    def chat(self, user_input: str) -> str:
        """Main chat method"""
        # Build conversation context
        conversation = f"System: {self.system_prompt}\n\n"
        
        # Add conversation history
        for exchange in self.conversation_history[-5:]:  # Keep last 5 exchanges
            conversation += f"Human: {exchange['user']}\nAssistant: {exchange['assistant']}\n\n"
        
        # Add current input
        conversation += f"Human: {user_input}\nAssistant: "
        
        # Get response from Ollama
        response = self.call_ollama(conversation)
        
        # Process response (execute tools if needed)
        processed_response = self.process_response(response)
        
        # Save to history
        self.conversation_history.append({
            "user": user_input,
            "assistant": processed_response
        })
        
        return processed_response

    def run_interactive(self):
        """Run interactive chat loop"""
        self.console.print(Panel("🤖 Offline Agent Started", style="bold green"))
        self.console.print(f"Using model: {self.model}")
        self.console.print("Type 'quit' or 'exit' to stop\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                self.console.print("\n🤖 Agent:", style="bold blue")
                response = self.chat(user_input)
                self.console.print(response)
                self.console.print()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.console.print(f"Error: {str(e)}", style="bold red")
        
        self.console.print("\n👋 Goodbye!", style="bold green")

if __name__ == "__main__":
    # You can specify a different model here
    agent = OfflineAgent()  # or OfflineAgent("your-model-name")
    agent.run_interactive()