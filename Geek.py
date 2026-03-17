import tkinter as tk
from tkinter import scrolledtext, messagebox
from groq import Groq

# CONFIG

API_KEY = "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"
MODEL_NAME = "llama-3.1-8b-instant"


# GROQ CLIENT

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    print("Error creating Groq client:", e)
    raise

# Conversation memory
messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful, friendly AI chatbot. "
            "Keep answers clear, simple, and useful."
        )
    }
]


# FUNCTIONS

def add_to_chat(sender, text):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"{sender}: {text}\n\n")
    chat_box.config(state="disabled")
    chat_box.yview(tk.END)

def send_message(event=None):
    user_text = entry_box.get().strip()

    if not user_text:
        return

    # show user message
    add_to_chat("You", user_text)
    entry_box.delete(0, tk.END)

    # special commands
    if user_text.lower() == "/clear":
        clear_chat()
        return

    if user_text.lower() == "/exit":
        root.destroy()
        return

    # store user message in memory
    messages.append({"role": "user", "content": user_text})


    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        bot_reply = response.choices[0].message.content.strip()

        # store bot reply in memory
        messages.append({"role": "assistant", "content": bot_reply})

        add_to_chat("Geek", bot_reply)

    except Exception as e:
        add_to_chat("Error", str(e))

    finally:
        status_label.config(text="Ready")

def clear_chat():
    global messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, friendly AI chatbot. "
                "Keep answers clear, simple, and useful."
            )
        }
    ]

    chat_box.config(state="normal")
    chat_box.delete("1.0", tk.END)
    chat_box.config(state="disabled")

    add_to_chat("Geek", "Memory cleared. Starting fresh.")

# =========================
# GUI
# =========================
root = tk.Tk()
root.title("GEEK AI CHATBOT")
root.geometry("700x550")
root.configure(bg="#1e1e1e")

title_label = tk.Label(
    root,
    text="Geek Chatbot",
    font=("Arial", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title_label.pack(pady=10)

chat_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 12),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white",
    state="disabled"
)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

bottom_frame = tk.Frame(root, bg="#1e1e1e")
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

entry_box = tk.Entry(
    bottom_frame,
    font=("Arial", 12),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white"
)
entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry_box.bind("<Return>", send_message)

send_button = tk.Button(
    bottom_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    command=send_message,
    bg="#4CAF50",
    fg="white",
    padx=15
)
send_button.pack(side=tk.RIGHT)

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="lightgreen"
)
status_label.pack(pady=(0, 8))

add_to_chat("Geek", "Hello 👋 I’m ready. Type your message.")
add_to_chat("Geek", "Commands: /clear to reset memory, /exit to close.")

entry_box.focus()
root.mainloop()