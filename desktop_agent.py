import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from agent import OfflineAgent

class DesktopAgentGUI:
    def __init__(self):
        self.agent = OfflineAgent()
        self.setup_gui()

    def setup_gui(self):
        self.window = tk.Tk()
        self.window.title("🤖 Offline AI Agent")
        self.window.geometry("800x600")
        self.window.configure(bg="#f0f0f0")

        # Create main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="🤖 Offline AI Agent", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            width=70, 
            height=20,
            font=("Helvetica", 20),
            bg="white",
            fg="black"
        )
        self.chat_display.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)

        # Message input
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(
            input_frame, 
            textvariable=self.message_var, 
            font=("Helvetica", 13)
        )
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = ttk.Button(
            input_frame, 
            text="Send", 
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1)

        # Clear button
        clear_button = ttk.Button(
            input_frame, 
            text="Clear", 
            command=self.clear_chat
        )
        clear_button.grid(row=0, column=2, padx=(10, 0))

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, font=("Arial", 8))
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        # Welcome message
        self.add_message("Agent", "Hello! I'm your offline AI assistant. How can I help you today?")

        # Focus on input
        self.message_entry.focus()

    def add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        message = self.message_var.get().strip()
        if not message:
            return

        # Add user message
        self.add_message("You", message)
        self.message_var.set("")

        # Disable send button and show status
        self.send_button.config(state=tk.DISABLED)
        self.status_var.set("Thinking...")

        # Send to agent in separate thread
        thread = threading.Thread(target=self.get_agent_response, args=(message,))
        thread.daemon = True
        thread.start()

    def get_agent_response(self, message):
        try:
            response = self.agent.chat(message)
            # Update GUI in main thread
            self.window.after(0, self.display_agent_response, response)
        except Exception as e:
            self.window.after(0, self.display_agent_response, f"Error: {str(e)}")

    def display_agent_response(self, response):
        self.add_message("Agent", response)
        self.send_button.config(state=tk.NORMAL)
        self.status_var.set("Ready")
        self.message_entry.focus()

    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.agent.conversation_history = []
        self.add_message("Agent", "Chat cleared! How can I help you Michal?")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = DesktopAgentGUI()
    app.run()