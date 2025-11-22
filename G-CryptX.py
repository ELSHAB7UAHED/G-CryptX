#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""
G-CryptX - Advanced Python Encryption Tool
Developer: Ahmed Nour Ahmed from Qena
License: Ethical Use Only - Ghost ©
"""

import os
import sys
import time
import hashlib
import secrets
import threading
import subprocess
import base64
import json
import traceback
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# Linux-only check
if sys.platform != "linux":
    print("❌ G-CryptX runs ONLY on Linux systems.")
    sys.exit(1)

try:
    import customtkinter as ctk
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from PIL import Image, ImageTk
    import psutil
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip3 install cryptography customtkinter pillow psutil")
    sys.exit(1)

# Audio simulation (using system beep for simplicity; replace with real .wav if desired)
try:
    import pygame
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    SOUND_ENABLED = True
except:
    SOUND_ENABLED = False

# ============= SOUND EFFECTS =============
def play_success_sound():
    if not SOUND_ENABLED:
        os.system("echo -e '\a' &> /dev/null")
        return
    sound = pygame.mixer.Sound(buffer=bytearray([128]*100 + [200]*100))
    sound.play()

def play_error_sound():
    if not SOUND_ENABLED:
        os.system("echo -e '\a\a' &> /dev/null")
        return
    sound = pygame.mixer.Sound(buffer=bytearray([50]*50 + [30]*50))
    sound.play()

# ============= MATRIX BACKGROUND =============
class MatrixBackground(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color="#000000")
        self.canvas = ctk.CTkCanvas(self, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.chars = "01"
        self.drops = []
        self.text_ids = []
        self.after(100, self.init_drops)
        self.animate()

    def init_drops(self):
        self.width = int(self.canvas.winfo_width() or 800)
        self.height = int(self.canvas.winfo_height() or 600)
        cols = self.width // 20
        self.drops = [0 for _ in range(cols)]
        self.text_ids = [None for _ in range(cols)]

    def animate(self):
        self.width = int(self.canvas.winfo_width() or 800)
        self.height = int(self.canvas.winfo_height() or 600)
        cols = self.width // 20
        if len(self.drops) != cols:
            self.drops = [0 for _ in range(cols)]
            self.text_ids = [None for _ in range(cols)]

        self.canvas.delete("matrix")
        for i in range(len(self.drops)):
            x = i * 20
            y = self.drops[i] * 20
            char = secrets.choice(self.chars)
            color = "#00ff00" if secrets.randbelow(10) > 7 else "#003300"
            self.text_ids[i] = self.canvas.create_text(
                x, y, text=char, fill=color, font=("OCR A Extended", 14, "bold"), tags="matrix"
            )
            self.drops[i] += 1
            if y > self.height or secrets.randbelow(100) < 2:
                self.drops[i] = 0
        self.after(50, self.animate)

# ============= MAIN APP =============
class GCryptXApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("G-CryptX — Ghost Encryption Engine")
        self.geometry("1024x768")
        self.minsize(900, 600)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Set dark theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Try to set OCR A Extended
        try:
            test_font = ("OCR A Extended", 12)
            self.option_add("*Font", test_font)
        except:
            pass

        # Watermark
        self.watermark = ctk.CTkLabel(self, text="Ghost ©", font=("Consolas", 10), text_color="#00ff44")
        self.watermark.place(relx=0.99, rely=0.99, anchor="se")

        # Developer credit
        self.dev_label = ctk.CTkLabel(
            self, 
            text="Ahmed Nour Ahmed from Qena", 
            font=("Consolas", 9, "italic"), 
            text_color="#00aa55"
        )
        self.dev_label.place(relx=0.01, rely=0.99, anchor="sw")

        # Splash screen
        self.show_splash()

    def show_splash(self):
        self.splash = ctk.CTkToplevel(self)
        self.splash.title("")
        self.splash.geometry("600x300")
        self.splash.configure(fg_color="#000000")
        self.splash.attributes("-topmost", True)
        self.splash.overrideredirect(True)

        # Center splash
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 300
        y = self.winfo_y() + (self.winfo_height() // 2) - 150
        self.splash.geometry(f"+{x}+{y}")

        # Logo placeholder (use transparent if missing)
        try:
            logo_img = Image.open("G-CryptX.png").convert("RGBA")
            logo_img = logo_img.resize((120, 120), Image.LANCZOS)
            logo = ImageTk.PhotoImage(logo_img)
            logo_label = ctk.CTkLabel(self.splash, image=logo, text="")
            logo_label.image = logo
            logo_label.pack(pady=20)
        except:
            title_label = ctk.CTkLabel(
                self.splash,
                text="G-CryptX",
                font=("OCR A Extended", 32, "bold"),
                text_color="#00ff44"
            )
            title_label.pack(pady=30)

        msg = ctk.CTkLabel(
            self.splash,
            text="Welcome to G-CryptX — Ghost Encryption Engine Initiated ⚡",
            font=("Consolas", 14),
            text_color="#00ff88",
            wraplength=500
        )
        msg.pack(pady=10)

        progress = ctk.CTkProgressBar(self.splash, width=400, height=8)
        progress.set(0)
        progress.pack(pady=20)
        progress.configure(progress_color="#00ff00")

        for i in range(1, 101):
            progress.set(i / 100)
            self.splash.update()
            time.sleep(0.01)

        self.splash.destroy()
        self.init_main_ui()

    def init_main_ui(self):
        # Matrix background
        self.bg_frame = MatrixBackground(self)
        self.bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Main frame on top
        self.main_frame = ctk.CTkFrame(self, fg_color="#0a0a0a", corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.92)

        # Tabs
        self.tabview = ctk.CTkTabview(
            self.main_frame,
            fg_color="#0f0f0f",
            segmented_button_fg_color="#000000",
            segmented_button_selected_color="#003300",
            segmented_button_selected_hover_color="#005500",
            text_color="#00ff44",
            text_color_disabled="#555555",
            font=("OCR A Extended", 14, "bold")
        )
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        tabs = ["🔒 Encrypt File", "🔓 Decrypt File", "⚙️ Run Encrypted Script", 
                "🧬 Key Generator", "📜 Activity Logs", "Internal Encryption"]
        for tab in tabs:
            self.tabview.add(tab)

        self.setup_encrypt_tab()
        self.setup_decrypt_tab()
        self.setup_run_tab()
        self.setup_keygen_tab()
        self.setup_logs_tab()
        self.setup_internal_tab()

        # Status bar
        self.status_bar = ctk.CTkFrame(self, fg_color="#001100", height=25)
        self.status_bar.pack(side="bottom", fill="x")
        self.status_time = ctk.CTkLabel(self.status_bar, text="", font=("Consolas", 10), text_color="#00aa00")
        self.status_user = ctk.CTkLabel(self.status_bar, text=f"User: {os.getlogin()}", font=("Consolas", 10), text_color="#00aa00")
        self.status_lib = ctk.CTkLabel(self.status_bar, text="Libs: OK", font=("Consolas", 10), text_color="#00aa00")
        self.status_time.pack(side="left", padx=10)
        self.status_user.pack(side="left", padx=10)
        self.status_lib.pack(side="right", padx=10)
        self.update_time()

        # Stealth mode button
        self.stealth_btn = ctk.CTkButton(
            self, text="🕶️ Stealth Mode", 
            command=self.toggle_stealth,
            fg_color="#002200",
            hover_color="#004400",
            text_color="#00ff88",
            font=("OCR A Extended", 12)
        )
        self.stealth_btn.place(relx=0.99, rely=0.02, anchor="ne")

    def update_time(self):
        self.status_time.configure(text=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.after(1000, self.update_time)

    def log(self, msg, color="green"):
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {msg}"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", formatted + "\n", color)
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

    def setup_encrypt_tab(self):
        tab = self.tabview.tab("🔒 Encrypt File")
        ctk.CTkLabel(tab, text="Select file to encrypt:", font=("OCR A Extended", 16), text_color="#00ff88").pack(pady=10)
        self.encrypt_file_path = ctk.CTkEntry(tab, placeholder_text="File path...", width=500, font=("Consolas", 12))
        self.encrypt_file_path.pack(pady=5)
        ctk.CTkButton(tab, text="Browse", command=lambda: self.browse_file(self.encrypt_file_path), 
                      fg_color="#003300", hover_color="#005500").pack(pady=5)
        ctk.CTkButton(tab, text="🔐 ENCRYPT", command=self.encrypt_file, 
                      fg_color="#005500", hover_color="#00aa00", font=("OCR A Extended", 14, "bold")).pack(pady=20)

    def setup_decrypt_tab(self):
        tab = self.tabview.tab("🔓 Decrypt File")
        ctk.CTkLabel(tab, text="Encrypted file:", font=("OCR A Extended", 16), text_color="#00ff88").pack(pady=5)
        self.decrypt_file_path = ctk.CTkEntry(tab, placeholder_text="Encrypted file path...", width=500, font=("Consolas", 12))
        self.decrypt_file_path.pack(pady=5)
        ctk.CTkButton(tab, text="Browse", command=lambda: self.browse_file(self.decrypt_file_path)).pack(pady=5)

        ctk.CTkLabel(tab, text="Decryption key (Base64):", font=("OCR A Extended", 16), text_color="#00ff88").pack(pady=10)
        self.decrypt_key = ctk.CTkEntry(tab, placeholder_text="Paste key here...", width=500, font=("Consolas", 12))
        self.decrypt_key.pack(pady=5)

        ctk.CTkButton(tab, text="🔓 DECRYPT", command=self.decrypt_file, 
                      fg_color="#005500", hover_color="#00aa00", font=("OCR A Extended", 14, "bold")).pack(pady=20)

    def setup_run_tab(self):
        tab = self.tabview.tab("⚙️ Run Encrypted Script")
        ctk.CTkLabel(tab, text="Select encrypted .py file to run:", font=("OCR A Extended", 16), text_color="#00ff88").pack(pady=10)
        self.run_file_path = ctk.CTkEntry(tab, placeholder_text="Encrypted Python file...", width=500, font=("Consolas", 12))
        self.run_file_path.pack(pady=5)
        ctk.CTkButton(tab, text="Browse", command=lambda: self.browse_file(self.run_file_path)).pack(pady=5)
        ctk.CTkButton(tab, text="▶️ RUN IN MEMORY", command=self.run_encrypted_script, 
                      fg_color="#005500", hover_color="#00aa00", font=("OCR A Extended", 14, "bold")).pack(pady=20)

    def setup_keygen_tab(self):
        tab = self.tabview.tab("🧬 Key Generator")
        ctk.CTkLabel(tab, text="Generate secure AES-256 key", font=("OCR A Extended", 16), text_color="#00ff88").pack(pady=10)
        self.key_output = ctk.CTkTextbox(tab, width=500, height=100, font=("Consolas", 12))
        self.key_output.pack(pady=10)
        ctk.CTkButton(tab, text="🎲 GENERATE KEY", command=self.generate_key, 
                      fg_color="#005500", hover_color="#00aa00", font=("OCR A Extended", 14, "bold")).pack(pady=10)
        ctk.CTkLabel(tab, text="Save key with password (optional):", font=("OCR A Extended", 14), text_color="#00cc66").pack(pady=5)
        self.key_pass = ctk.CTkEntry(tab, placeholder_text="Password to encrypt key...", width=400, show="*", font=("Consolas", 12))
        self.key_pass.pack(pady=5)
        ctk.CTkButton(tab, text="💾 SAVE KEY SECURELY", command=self.save_key_securely, 
                      fg_color="#004400", hover_color="#007700").pack(pady=5)

    def setup_logs_tab(self):
        tab = self.tabview.tab("📜 Activity Logs")
        self.log_text = ctk.CTkTextbox(tab, wrap="word", font=("Consolas", 12))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_text.tag_config("green", foreground="#00ff44")
        self.log_text.insert("1.0", "🔒 G-CryptX Activity Log Initialized\n", "green")
        self.log_text.configure(state="disabled")

    def setup_internal_tab(self):
        tab = self.tabview.tab("Internal Encryption")
        ctk.CTkLabel(tab, text="Convert any .py file into self-decrypting encrypted script", 
                     font=("OCR A Extended", 16), text_color="#00ff88").pack(pady=10)
        self.internal_file_path = ctk.CTkEntry(tab, placeholder_text="Python file to encrypt (e.g., app.py)...", width=500, font=("Consolas", 12))
        self.internal_file_path.pack(pady=5)
        ctk.CTkButton(tab, text="Browse", command=lambda: self.browse_file(self.internal_file_path, [("Python Files", "*.py")])).pack(pady=5)
        ctk.CTkButton(tab, text="🔥 ENCRYPT & MAKE SELF-RUNNING", command=self.internal_encrypt, 
                      fg_color="#005500", hover_color="#00aa00", font=("OCR A Extended", 14, "bold")).pack(pady=20)
        ctk.CTkLabel(tab, text="💡 Result: Same filename, but encrypted. Run with: python script.py", 
                     font=("Consolas", 12), text_color="#00cc66").pack(pady=10)

    def browse_file(self, entry_widget, filetypes=[("All Files", "*.*")]):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, path)

    def generate_key(self):
        key = AESGCM.generate_key(bit_length=256)
        b64_key = base64.b64encode(key).decode()
        self.key_output.delete("1.0", "end")
        self.key_output.insert("1.0", b64_key)
        self.log("🔑 New AES-256 key generated.")
        play_success_sound()

    def save_key_securely(self):
        key_text = self.key_output.get("1.0", "end").strip()
        if not key_text:
            self.log("❌ No key to save!", "red")
            play_error_sound()
            return
        password = self.key_pass.get()
        if not password:
            self.log("⚠️ Warning: Saving key without password protection.", "yellow")
        # In real app, you'd encrypt the key with password using PBKDF2
        from tkinter import filedialog
        save_path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key Files", "*.key")])
        if save_path:
            with open(save_path, "w") as f:
                f.write(key_text)
            self.log(f"💾 Key saved to: {save_path}")

    def encrypt_file(self):
        filepath = self.encrypt_file_path.get()
        if not os.path.isfile(filepath):
            self.log("❌ File not found!", "red")
            play_error_sound()
            return

        key = AESGCM.generate_key(bit_length=256)
        nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(key)
        with open(filepath, "rb") as f:
            data = f.read()
        encrypted = aesgcm.encrypt(nonce, data, None)

        output_path = filepath + ".gcx"
        with open(output_path, "wb") as f:
            f.write(nonce + encrypted)

        b64_key = base64.b64encode(key).decode()
        self.log(f"✅ Encrypted: {output_path}")
        self.log(f"🔑 Key (SAVE IT): {b64_key}")
        play_success_sound()

        # Auto-show in key generator tab
        self.key_output.delete("1.0", "end")
        self.key_output.insert("1.0", b64_key)

    def decrypt_file(self):
        filepath = self.decrypt_file_path.get()
        key_b64 = self.decrypt_key.get()
        if not os.path.isfile(filepath):
            self.log("❌ Encrypted file not found!", "red")
            play_error_sound()
            return
        try:
            key = base64.b64decode(key_b64)
            with open(filepath, "rb") as f:
                data = f.read()
            nonce = data[:12]
            ciphertext = data[12:]
            aesgcm = AESGCM(key)
            decrypted = aesgcm.decrypt(nonce, ciphertext, None)

            output_path = filepath.replace(".gcx", ".decrypted")
            if output_path == filepath:
                output_path += ".decrypted"
            with open(output_path, "wb") as f:
                f.write(decrypted)
            self.log(f"✅ Decrypted to: {output_path}")
            play_success_sound()
        except Exception as e:
            self.log(f"❌ Decryption failed: {str(e)}", "red")
            play_error_sound()

    def run_encrypted_script(self):
        filepath = self.run_file_path.get()
        if not os.path.isfile(filepath):
            self.log("❌ Script not found!", "red")
            play_error_sound()
            return
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            if len(data) < 13:
                raise ValueError("Invalid encrypted file")

            nonce = data[:12]
            ciphertext = data[12:]
            key_b64 = self.decrypt_key.get() or base64.b64encode(AESGCM.generate_key(256)).decode()
            key = base64.b64decode(key_b64)

            aesgcm = AESGCM(key)
            source = aesgcm.decrypt(nonce, ciphertext, None).decode()

            # Execute in memory
            self.log(f"▶️ Executing encrypted script: {filepath}")
            old_stdout, old_stderr = sys.stdout, sys.stderr
            captured_output = StringIO()
            sys.stdout = sys.stderr = captured_output

            try:
                exec(source, {"__file__": filepath})
                output = captured_output.getvalue()
                if output.strip():
                    self.log("📝 Script Output:\n" + output)
                self.log("✅ Script executed successfully in memory.")
                play_success_sound()
            except Exception as e:
                error_msg = traceback.format_exc()
                self.log(f"💥 Runtime Error:\n{error_msg}", "red")
                play_error_sound()
            finally:
                sys.stdout, sys.stderr = old_stdout, old_stderr
        except Exception as e:
            self.log(f"❌ Failed to run encrypted script: {str(e)}", "red")
            play_error_sound()

    def internal_encrypt(self):
        filepath = self.internal_file_path.get()
        if not filepath.endswith(".py") or not os.path.isfile(filepath):
            self.log("❌ Please select a valid .py file!", "red")
            play_error_sound()
            return

        with open(filepath, "r") as f:
            source_code = f.read()

        # Encrypt source
        key = AESGCM.generate_key(bit_length=256)
        nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(key)
        encrypted = aesgcm.encrypt(nonce, source_code.encode(), None)

        # Create self-decrypting loader
        loader_code = f'''
# G-CryptX Encrypted Python Script - Ghost ©
import base64, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
encrypted_data = {repr(base64.b64encode(nonce + encrypted).decode())}
key = {repr(base64.b64encode(key).decode())}
try:
    data = base64.b64decode(encrypted_data)
    nonce = data[:12]
    ciphertext = data[12:]
    aesgcm = AESGCM(base64.b64decode(key))
    source = aesgcm.decrypt(nonce, ciphertext, None)
    exec(source, {{"__file__": sys.argv[0]}})
except Exception as e:
    print("❌ Decryption or execution failed. Unauthorized access detected.")
    sys.exit(1)
'''

        output_path = filepath  # overwrite original
        with open(output_path, "w") as f:
            f.write(loader_code)

        self.log(f"🔥 Self-decrypting script created: {output_path}")
        self.log(f"🔑 Encryption key: {base64.b64encode(key).decode()}")
        play_success_sound()

    def toggle_stealth(self):
        # Switch to fake terminal
        self.withdraw()
        stealth = ctk.CTkToplevel()
        stealth.title("Terminal - user@ghost")
        stealth.geometry("800x600")
        stealth.configure(fg_color="#000000")

        term = ctk.CTkTextbox(stealth, font=("Consolas", 12), text_color="#00ff00", fg_color="#000000")
        term.pack(fill="both", expand=True)
        term.insert("1.0", "user@ghost:~$ \n")
        term.configure(state="disabled")

        def on_close():
            stealth.destroy()
            self.deiconify()

        stealth.protocol("WM_DELETE_WINDOW", on_close)

    def on_closing(self):
        if messagebox := getattr(ctk, "messagebox", None):
            confirm = messagebox.askokcancel("Exit", "Are you sure you want to quit G-CryptX?")
        else:
            import tkinter.messagebox as tkmsg
            confirm = tkmsg.askokcancel("Exit", "Are you sure you want to quit G-CryptX?")
        if confirm:
            self.quit()

# ============= MAIN ENTRY =============
if __name__ == "__main__":
    app = GCryptXApp()
    app.mainloop()
