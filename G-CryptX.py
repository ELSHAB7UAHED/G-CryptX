#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G-CryptX — Ghost Encryption Engine
Developer: Ahmed Nour Ahmed from Qena
© Ghost © 2025 — All Rights Reserved

Powerful, Ethical, and Intense Hacking-Themed Python Encryption Tool
For Linux Only — One-File Executable with In-Memory Execution
"""

import os
import sys
import time
import threading
import hashlib
import base64
import secrets
import subprocess
import json
import logging
from pathlib import Path

# Only allow Linux
if sys.platform != "linux":
    print("⚠️ G-CryptX works ONLY on Linux systems.")
    sys.exit(1)

# --- Imports ---
try:
    import customtkinter as ctk
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from pydub import AudioSegment
    from pydub.playback import play
    import tkinter as tk
    from tkinter import filedialog, messagebox
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install customtkinter cryptography pydub")
    sys.exit(1)

# --- Constants ---
APP_NAME = "G-CryptX"
VERSION = "v2.1.0"
DEVELOPER_EN = "Ahmed Nour Ahmed from Qena"
DEVELOPER_AR = "أحمد نور أحمد من قنا"
WATERMARK = "Ghost ©"
ICON_PATH = "G-CryptX.png"
SPLASH_DURATION = 3000  # ms
NEON_GREEN = "#00ff41"
DARK_BG = "#000000"
SECONDARY_BG = "#0f0f0f"
MATRIX_CHARS = "01"

# --- Setup Logging ---
log_stream = []
class LogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        log_stream.append(msg)
        if hasattr(GCryptXApp, 'instance') and GCryptXApp.instance:
            GCryptXApp.instance.update_log_display()

logging.basicConfig(level=logging.INFO, handlers=[LogHandler()], format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("G-CryptX")

# --- Audio Alerts ---
def play_sound(success=True):
    def _play():
        try:
            if success:
                sound = AudioSegment.silent(duration=100) + AudioSegment.from_file(
                    io.BytesIO(base64.b64decode(
                        b'UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBRRSf7GfbUI2L0+Iu8B8Py0wWZO7t59sRTUxU4y8wXczKzJimL+5l2E9NDBSh7W8mF44LzNXjbu7l145MDJYkLq3k1sxLzVfkrq1jVQvLzRdjrWxh08tLjJfj7Gse0YoKzJijKuodD8nKTBli6mmbTkoJzBjh6OjZjQmJy9gf52ZaDQmJy5ceJWWYzEkJS1YdpKMXy8kJCtTb46LWiwjIyhNao2KVSwiIiZIY4iGTiohISEeS2F+iEknIB8fHh9DWXZ8iiUeHR0cHR8fHyAhISEgHyAhIiIiIiMkJCMkJCUmJiYmJiYnJycnJycnKCgoKCgoKCkpKSkpKSkqKioqKioqKysrKysrKywsLCwsLCwsLS0tLS0tLS4uLi4uLi4vLy8vLy8vMDAwMDAwMDExMTExMTExMjIyMjIyMjMzMzMzMzM0NDQ0NDQ0NTU1NTU1NTY2NjY2NjY3Nzc3Nzc3ODg4ODg4ODk5OTk5OTk6Ojo6Ojo6Ozs7Ozs7Oz09PT09PT0+Pj4+Pj4+Pz8/Pz8/P0BAQEBAQEBAQUFBQUFBQUJCQkJCQkJDQ0NDQ0NDQ0REREQ='
                    )), format="wav")
            else:
                sound = AudioSegment.silent(duration=50) + AudioSegment.from_file(
                    io.BytesIO(base64.b64decode(
                        b'UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBRRSf7GfbUI2L0+Iu8B8Py0wWZO7t59sRTUxU4y8wXczKzJimL+5l2E9NDBSh7W8mF44LzNXjbu7l145MDJYkLq3k1sxLzRfjrWxh08tLjJfj7Gse0YoKzJijKuodD8nKTBli6mmbTkoJzBjh6OjZjQmJy9gf52ZaDQmJy5ceJWWYzEkJS1YdpKMXy8kJCtTb46LWiwjIyhNao2KVSwiIiZIY4iGTiohISEeS2F+iEknIB8fHh9DWXZ8iiUeHR0cHR8fHyAhISEgHyAhIiIiIiMkJCMkJCUmJiYmJiYnJycnJycnKCgoKCgoKCkpKSkpKSkqKioqKioqKysrKysrKywsLCwsLCwsLS0tLS0tLS4uLi4uLi4vLy8vLy8vMDAwMDAwMDExMTExMTExMjIyMjIyMjMzMzMzMzM0NDQ0NDQ0NTU1NTU1NTY2NjY2NjY3Nzc3Nzc3ODg4ODg4ODk5OTk5OTk6Ojo6Ojo6Ozs7Ozs7Oz09PT09PT0+Pj4+Pj4+Pz8/Pz8/P0BAQEBAQEBAQUFBQUFBQUJCQkJCQkJDQ0NDQ0NDQ0REREQ='
                    )), format="wav")
                sound = sound.reverse()
            play(sound)
        except Exception:
            pass  # Fail silently if audio fails
    threading.Thread(target=_play, daemon=True).start()

# --- Matrix Background Canvas ---
class MatrixBackground(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color=DARK_BG)
        self.canvas = tk.Canvas(self, bg=DARK_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.columns = []
        self.delay = 50
        self.after(100, self.start_matrix)

    def start_matrix(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        if self.width < 10 or self.height < 10:
            self.after(100, self.start_matrix)
            return
        col_count = self.width // 15
        for _ in range(col_count):
            self.columns.append({
                'x': len(self.columns) * 15,
                'y': -20,
                'speed': secrets.randbelow(5) + 2,
                'length': secrets.randbelow(20) + 5
            })
        self.animate()

    def animate(self):
        self.canvas.delete("all")
        for col in self.columns:
            col['y'] += col['speed']
            if col['y'] - col['length'] * 15 > self.height:
                col['y'] = -20
                col['length'] = secrets.randbelow(20) + 5
            for i in range(col['length']):
                y_pos = col['y'] - i * 15
                if 0 <= y_pos < self.height:
                    char = secrets.choice(MATRIX_CHARS)
                    color = NEON_GREEN if i == 0 else "#005500"
                    self.canvas.create_text(
                        col['x'], y_pos,
                        text=char, fill=color,
                        font=("Consolas", 12, "bold")
                    )
        self.after(self.delay, self.animate)

# --- Splash Screen ---
class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("")
        self.geometry("500x300")
        self.configure(fg_color=DARK_BG)
        self.overrideredirect(True)
        self.transient(parent)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (500 / 2))
        y = int((screen_height / 2) - (300 / 2))
        self.geometry(f"500x300+{x}+{y}")

        try:
            img = tk.PhotoImage(file=ICON_PATH)
            label_img = ctk.CTkLabel(self, image=img, text="")
            label_img.image = img
            label_img.pack(pady=20)
        except:
            label_title = ctk.CTkLabel(
                self, text=APP_NAME,
                font=("OCR A Extended", 32, "bold"),
                text_color=NEON_GREEN
            )
            label_title.pack(pady=20)

        self.label = ctk.CTkLabel(
            self, text="Welcome to G-CryptX — Ghost Encryption Engine Initiated ⚡",
            font=("Consolas", 14), text_color=NEON_GREEN
        )
        self.label.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=400, height=8)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.loading_thread = threading.Thread(target=self.simulate_loading, daemon=True)
        self.loading_thread.start()

    def simulate_loading(self):
        for i in range(101):
            time.sleep(0.03)
            self.progress.set(i / 100)
            self.update_idletasks()
        self.destroy()

# --- Main App ---
class GCryptXApp(ctk.CTk):
    instance = None

    def __init__(self):
        super().__init__()
        GCryptXApp.instance = self

        # Window setup
        self.title(f"{APP_NAME} {VERSION}")
        self.geometry("900x650")
        self.minsize(800, 600)
        self.configure(fg_color=DARK_BG)

        try:
            self.iconphoto(False, tk.PhotoImage(file=ICON_PATH))
        except:
            pass

        # Splash
        splash = SplashScreen(self)
        self.withdraw()
        splash.mainloop()
        self.deiconify()

        # UI
        self.create_widgets()
        self.status_bar = ctk.CTkLabel(
            self, text=f"User: {os.getenv('USER')} | Time: {time.strftime('%H:%M')} | Libraries: ✅",
            fg_color=SECONDARY_BG, text_color="#aaaaaa", height=25, font=("Consolas", 10)
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.after(1000, self.update_status_time)

        # Watermark
        self.watermark = ctk.CTkLabel(self, text=WATERMARK, text_color="#333333", font=("Consolas", 10))
        self.watermark.place(relx=0.99, rely=0.99, anchor="se")

        # Stealth mode hidden terminal
        self.stealth_window = None

        logger.info("G-CryptX initialized successfully.")

    def update_status_time(self):
        self.status_bar.configure(text=f"User: {os.getenv('USER')} | Time: {time.strftime('%H:%M:%S')} | Libraries: ✅")
        self.after(1000, self.update_status_time)

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.notebook = ctk.CTkTabview(self, fg_color=SECONDARY_BG)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        tabs = ["🔒 Encrypt File", "🔓 Decrypt File", "⚙️ Run Encrypted Script", "🧬 Key Generator", "📜 Activity Logs", "Internal Encryption"]
        for t in tabs:
            self.notebook.add(t)

        # --- Encrypt Tab ---
        self.setup_encrypt_tab()
        # --- Decrypt Tab ---
        self.setup_decrypt_tab()
        # --- Run Tab ---
        self.setup_run_tab()
        # --- Key Gen Tab ---
        self.setup_keygen_tab()
        # --- Logs Tab ---
        self.setup_logs_tab()
        # --- Internal Encryption Tab ---
        self.setup_internal_tab()

        # Stealth button
        self.stealth_btn = ctk.CTkButton(
            self, text="🕶️ Stealth Mode", command=self.toggle_stealth,
            fg_color="transparent", hover_color="#222222", text_color=NEON_GREEN,
            font=("Consolas", 14, "bold")
        )
        self.stealth_btn.place(relx=0.01, rely=0.01)

    def toggle_stealth(self):
        if self.stealth_window is None or not self.stealth_window.winfo_exists():
            self.withdraw()
            self.stealth_window = ctk.CTkToplevel(self)
            self.stealth_window.title("Terminal - user@linux")
            self.stealth_window.geometry("700x500")
            self.stealth_window.configure(fg_color="#000000")
            terminal = ctk.CTkTextbox(self.stealth_window, font=("Consolas", 12), fg_color="#000000", text_color=NEON_GREEN)
            terminal.pack(fill="both", expand=True, padx=10, pady=10)
            terminal.insert("end", "user@linux:~$ ")
            terminal.configure(state="disabled")
            self.stealth_window.protocol("WM_DELETE_WINDOW", self.exit_stealth)
        else:
            self.stealth_window.focus()

    def exit_stealth(self):
        if self.stealth_window:
            self.stealth_window.destroy()
            self.stealth_window = None
        self.deiconify()

    def setup_encrypt_tab(self):
        tab = self.notebook.tab("🔒 Encrypt File")
        tab.grid_columnconfigure(0, weight=1)

        self.encrypt_file_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Select Python File to Encrypt:", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=0, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.encrypt_file_path, width=500).grid(row=1, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse", command=self.browse_encrypt_file, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=1, column=1, padx=5)

        self.encrypt_key_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Select Encryption Key (.key):", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=2, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.encrypt_key_path, width=500).grid(row=3, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse Key", command=self.browse_key_file, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=3, column=1, padx=5)

        self.encrypt_progress = ctk.CTkProgressBar(tab, width=500)
        self.encrypt_progress.set(0)
        self.encrypt_progress.grid(row=4, column=0, pady=10)

        ctk.CTkButton(tab, text="🔒 ENCRYPT", command=self.encrypt_file, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33", font=("OCR A Extended", 16, "bold")).grid(row=5, column=0, pady=20)

    def setup_decrypt_tab(self):
        tab = self.notebook.tab("🔓 Decrypt File")
        tab.grid_columnconfigure(0, weight=1)

        self.decrypt_file_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Select Encrypted File:", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=0, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.decrypt_file_path, width=500).grid(row=1, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse", command=self.browse_decrypt_file, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=1, column=1, padx=5)

        self.decrypt_key_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Select Key File:", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=2, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.decrypt_key_path, width=500).grid(row=3, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse Key", command=self.browse_key_file_decrypt, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=3, column=1, padx=5)

        ctk.CTkButton(tab, text="🔓 DECRYPT", command=self.decrypt_file, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33", font=("OCR A Extended", 16, "bold")).grid(row=4, column=0, pady=20)

    def setup_run_tab(self):
        tab = self.notebook.tab("⚙️ Run Encrypted Script")
        tab.grid_columnconfigure(0, weight=1)

        self.run_file_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Select Encrypted Python Script:", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=0, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.run_file_path, width=500).grid(row=1, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse", command=self.browse_run_file, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=1, column=1, padx=5)

        self.run_key_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Select Key File:", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=2, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.run_key_path, width=500).grid(row=3, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse Key", command=self.browse_key_file_run, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=3, column=1, padx=5)

        ctk.CTkButton(tab, text="🚀 RUN IN MEMORY", command=self.run_encrypted_script, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33", font=("OCR A Extended", 16, "bold")).grid(row=4, column=0, pady=20)

    def setup_keygen_tab(self):
        tab = self.notebook.tab("🧬 Key Generator")
        tab.grid_columnconfigure(0, weight=1)

        self.key_save_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Save Key As:", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=0, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.key_save_path, width=500).grid(row=1, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse Save Location", command=self.browse_key_save, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=1, column=1, padx=5)

        ctk.CTkButton(tab, text="🧬 GENERATE KEY", command=self.generate_key, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33", font=("OCR A Extended", 16, "bold")).grid(row=2, column=0, pady=20)

    def setup_logs_tab(self):
        tab = self.notebook.tab("📜 Activity Logs")
        self.log_text = ctk.CTkTextbox(tab, font=("Consolas", 12), text_color=NEON_GREEN, fg_color="#001100")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_text.configure(state="disabled")

    def setup_internal_tab(self):
        tab = self.notebook.tab("Internal Encryption")
        tab.grid_columnconfigure(0, weight=1)

        self.internal_file_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Select Python File for In-Place Encryption:", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=0, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.internal_file_path, width=500).grid(row=1, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse", command=self.browse_internal_file, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=1, column=1, padx=5)

        self.internal_key_path = ctk.StringVar()
        ctk.CTkLabel(tab, text="Key File (or leave empty to generate):", text_color=NEON_GREEN, font=("Consolas", 14)).grid(row=2, column=0, pady=5)
        ctk.CTkEntry(tab, textvariable=self.internal_key_path, width=500).grid(row=3, column=0, pady=5)
        ctk.CTkButton(tab, text="Browse Key", command=self.browse_internal_key, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33").grid(row=3, column=1, padx=5)

        ctk.CTkButton(tab, text="🔥 ENCRYPT IN-PLACE (Self-Executing)", command=self.encrypt_inplace, fg_color=NEON_GREEN, text_color="black", hover_color="#00cc33", font=("OCR A Extended", 16, "bold")).grid(row=4, column=0, pady=20)

    # === Utility Functions ===
    def browse_encrypt_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path: self.encrypt_file_path.set(path)

    def browse_decrypt_file(self):
        path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.py.enc"), ("All Files", "*.*")])
        if path: self.decrypt_file_path.set(path)

    def browse_run_file(self):
        path = filedialog.askopenfilename(filetypes=[("Encrypted Python", "*.py.enc")])
        if path: self.run_file_path.set(path)

    def browse_key_file(self):
        path = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
        if path: self.encrypt_key_path.set(path)

    def browse_key_file_decrypt(self):
        path = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
        if path: self.decrypt_key_path.set(path)

    def browse_key_file_run(self):
        path = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
        if path: self.run_key_path.set(path)

    def browse_key_save(self):
        path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key Files", "*.key")])
        if path: self.key_save_path.set(path)

    def browse_internal_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path: self.internal_file_path.set(path)

    def browse_internal_key(self):
        path = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
        if path: self.internal_key_path.set(path)

    def load_key(self, key_path):
        with open(key_path, "rb") as f:
            return f.read()

    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    def encrypt_file(self):
        file_path = self.encrypt_file_path.get()
        key_path = self.encrypt_key_path.get()
        if not file_path or not key_path:
            messagebox.showerror("Error", "Please select both file and key.")
            return
        try:
            key = self.load_key(key_path)
            aesgcm = AESGCM(key)
            with open(file_path, "rb") as f:
                data = f.read()
            nonce = secrets.token_bytes(12)
            encrypted = aesgcm.encrypt(nonce, data, None)
            out_path = file_path + ".enc"
            with open(out_path, "wb") as f:
                f.write(nonce + encrypted)
            logger.info(f"✅ Encrypted: {out_path}")
            play_sound(True)
            messagebox.showinfo("Success", f"File encrypted to:\n{out_path}")
        except Exception as e:
            logger.error(f"❌ Encryption failed: {e}")
            play_sound(False)
            messagebox.showerror("Error", str(e))

    def decrypt_file(self):
        file_path = self.decrypt_file_path.get()
        key_path = self.decrypt_key_path.get()
        if not file_path or not key_path:
            messagebox.showerror("Error", "Please select both file and key.")
            return
        try:
            key = self.load_key(key_path)
            aesgcm = AESGCM(key)
            with open(file_path, "rb") as f:
                data = f.read()
            nonce = data[:12]
            ciphertext = data[12:]
            decrypted = aesgcm.decrypt(nonce, ciphertext, None)
            out_path = file_path.replace(".enc", ".decrypted.py")
            with open(out_path, "wb") as f:
                f.write(decrypted)
            logger.info(f"✅ Decrypted: {out_path}")
            play_sound(True)
            messagebox.showinfo("Success", f"File decrypted to:\n{out_path}")
        except Exception as e:
            logger.error(f"❌ Decryption failed: {e}")
            play_sound(False)
            messagebox.showerror("Error", str(e))

    def run_encrypted_script(self):
        file_path = self.run_file_path.get()
        key_path = self.run_key_path.get()
        if not file_path or not key_path:
            messagebox.showerror("Error", "Please select both file and key.")
            return
        try:
            key = self.load_key(key_path)
            aesgcm = AESGCM(key)
            with open(file_path, "rb") as f:
                data = f.read()
            nonce = data[:12]
            ciphertext = data[12:]
            decrypted = aesgcm.decrypt(nonce, ciphertext, None)
            logger.info(f"🚀 Executing {file_path} in memory...")
            exec(decrypted, {"__name__": "__main__"})
            logger.info("✅ Script executed successfully.")
            play_sound(True)
        except Exception as e:
            logger.error(f"❌ Execution failed: {e}")
            play_sound(False)
            messagebox.showerror("Error", str(e))

    def generate_key(self):
        path = self.key_save_path.get()
        if not path:
            messagebox.showerror("Error", "Please specify key save path.")
            return
        try:
            key = AESGCM.generate_key(bit_length=256)
            with open(path, "wb") as f:
                f.write(key)
            logger.info(f"✅ Key generated: {path}")
            play_sound(True)
            messagebox.showinfo("Success", f"Key saved to:\n{path}")
        except Exception as e:
            logger.error(f"❌ Key generation failed: {e}")
            play_sound(False)
            messagebox.showerror("Error", str(e))

    def encrypt_inplace(self):
        file_path = self.internal_file_path.get()
        key_path = self.internal_key_path.get()
        if not file_path:
            messagebox.showerror("Error", "Select a Python file.")
            return
        try:
            if not key_path:
                key = AESGCM.generate_key(bit_length=256)
                key_path = file_path + ".auto.key"
                with open(key_path, "wb") as f:
                    f.write(key)
                logger.info(f"🔑 Auto-generated key: {key_path}")
            else:
                key = self.load_key(key_path)

            with open(file_path, "rb") as f:
                original_code = f.read()

            aesgcm = AESGCM(key)
            nonce = secrets.token_bytes(12)
            encrypted = aesgcm.encrypt(nonce, original_code, None)

            # Build loader
            loader_code = f'''
# G-CryptX In-Place Encrypted Script — DO NOT MODIFY
import sys, os, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
key_path = __file__ + ".key"
if not os.path.exists(key_path):
    print("❌ Missing key file:", key_path)
    sys.exit(1)
with open(key_path, "rb") as f: key = f.read()
with open(__file__, "rb") as f:
    data = f.read()
start_marker = b"# ENCRYPTED PAYLOAD:"
idx = data.find(start_marker)
if idx == -1:
    print("❌ Invalid encrypted file")
    sys.exit(1)
payload = base64.b64decode(data[idx+len(start_marker):].strip())
nonce = payload[:12]
ct = payload[12:]
aesgcm = AESGCM(key)
try:
    code = aesgcm.decrypt(nonce, ct, None)
    exec(code)
except Exception as e:
    print("❌ Decryption/Execution failed:", e)
'''
            encrypted_b64 = base64.b64encode(nonce + encrypted).decode()
            full_script = loader_code + "\n# ENCRYPTED PAYLOAD:" + encrypted_b64

            with open(file_path, "w") as f:
                f.write(full_script)

            # Save key
            with open(key_path, "wb") as f:
                f.write(key)

            logger.info(f"🔥 In-place encryption completed: {file_path}")
            play_sound(True)
            messagebox.showinfo("Success", f"File is now self-decrypting!\nKey: {key_path}")
        except Exception as e:
            logger.error(f"❌ In-place encryption failed: {e}")
            play_sound(False)
            messagebox.showerror("Error", str(e))

    def update_log_display(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        for line in log_stream[-500:]:
            self.log_text.insert("end", line + "\n")
        self.log_text.yview("end")
        self.log_text.configure(state="disabled")


# --- Main Entry ---
if __name__ == "__main__":
    import io  # needed for audio

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    app = GCryptXApp()
    app.mainloop()
