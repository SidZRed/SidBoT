import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime


class ChatAIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ChatAI")
        self.master.geometry("500x400")
        self.master.configure(bg="#CCCCCC")  # Set background color

        self.user_name = ""
        self.knowledge_base = self.load_knowledge_base(
            r"C:\Users\rolla\OneDrive\Desktop\Programming\ChatAI\knowledge_base.json")

        self.create_widgets()

    def create_widgets(self):
        self.chat_text = scrolledtext.ScrolledText(
            self.master, wrap=tk.WORD, width=40, height=15, bg="black", fg="white")  # Set background and text color
        self.chat_text.pack(pady=10)

        self.user_input_entry = tk.Entry(self.master, width=30)
        self.user_input_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Add initial text to the entry widget
        self.user_input_entry.insert(0, "Ask right away")
        self.user_input_entry.bind("<FocusIn>", self.clear_initial_text)

        self.send_button = tk.Button(
            self.master, text="Send", command=self.process_user_input)
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.quit_button = tk.Button(
            self.master, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        # Configure tags for colored text
        self.chat_text.tag_configure("bot_tag", foreground="blue")
        self.chat_text.tag_configure("user_tag", foreground="green")

    def clear_initial_text(self, event):
        # Clear the initial text when the user clicks on the entry
        if self.user_input_entry.get() == "Ask right away":
            self.user_input_entry.delete(0, tk.END)

    def process_user_input(self):
        user_input = self.user_input_entry.get()
        self.user_input_entry.delete(0, tk.END)

        if user_input.lower() == "exit" or user_input.lower() == "quit":
            self.master.destroy()

        best_match = self.find_best_match(
            user_input, [q["question"] for q in self.knowledge_base["questions"]])

        if best_match:
            answer = self.get_answer(best_match, self.knowledge_base)
            self.display_message("SidBOT: " + answer, "bot_tag")
        else:
            response = messagebox.askquestion(
                "Unknown Input", "I'm sorry I haven't been trained on this yet.\nWould you like to provide me with that knowledge?")
            if response == 'yes':
                new_answer = messagebox.askstring(
                    "Provide Knowledge", "Enter your answer:")
                if new_answer:
                    self.knowledge_base["questions"].append(
                        {"question": user_input, "answer": new_answer})
                    self.save_knowledge_base(
                        r"C:\Users\rolla\OneDrive\Desktop\Programming\ChatAI\knowledge_base.json", self.knowledge_base)
                    self.display_message(
                        f"SidBOT: Thanks for the knowledge, {self.user_name}!", "bot_tag")
                else:
                    self.display_message(
                        "SidBOT: Knowledge input canceled.", "bot_tag")
            else:
                self.display_message(
                    "SidBOT: You chose not to provide knowledge.", "bot_tag")

    def display_message(self, message, tag):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.chat_text.insert(tk.END, formatted_message, tag)

    def load_knowledge_base(self, file_path: str) -> dict:
        try:
            with open(file_path, "r") as file:
                data: dict = json.load(file)
            return data
        except FileNotFoundError:
            messagebox.showerror("Error", "Knowledge base file not found.")
            self.master.destroy()

    def save_knowledge_base(self, file_path: str, data: dict) -> None:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    def find_best_match(self, user_question: str, questions: list[str]) -> str | None:
        matches: list = get_close_matches(
            user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_answer(self, question: str, knowledge_base: dict) -> str | None:
        for q in knowledge_base["questions"]:
            if q["question"] == question:
                return q["answer"]


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatAIApp(root)
    root.mainloop()
