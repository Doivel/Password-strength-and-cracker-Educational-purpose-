import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import re
import itertools
import string
import threading

# --- CORE LOGIC (ACCUMULATIVE SCORING) ---

COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "12345678", "dragon",
    "p@ssw0rd", "passw0rd", "admin", "guest", "iloveyou"
]

def calculate_strength(password):
    score = 0
    suggestions = []
    length = len(password)
    
    # 1. LENGTH SCORE (Max 40 points)
    score += min(40, length * 4)
    
    # 2. DIVERSITY SCORE (Max 60 points)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[^A-Za-z0-9]', password))

    char_types = sum([has_upper, has_lower, has_digit, has_symbol])
    score += (char_types * 15)

    # 3. BONUSES & PENALTIES
    if length < 8:
        score -= 20
        suggestions.append("❌ LENGTH WARNING: Aim for 8+ characters (10+ is optimal).")
    
    if char_types < 3:
        score -= 15
        suggestions.append("⚠️ WEAK MIX: Use Uppercase, Numbers & Symbols for diversity.")
        
    if not (has_digit and has_symbol):
        score -= 10
        suggestions.append("⚠️ VULNERABLE: Include both a number and a symbol.")

    if any(p in password.lower() for p in COMMON_PASSWORDS):
        score -= 50
        suggestions.append("❌ CRITICAL: Found in common dictionary database.")
    
    if re.search(r'(.)\1\1', password):
        score -= 20
        suggestions.append("⚠️ PATTERN: Repeated characters detected (e.g., 'aaa').")
    
    if re.search(r'0123|1234|abc|bcd', password.lower()):
        score -= 20
        suggestions.append("⚠️ PATTERN: Sequential characters detected (e.g., '123').")

    return max(0, min(100, score)), suggestions

# --- GLORIFIED GUI CLASS (ACADEMIC EDITION) ---

class AcademicPasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADVANCED CYBER SECURITY AUDITOR v3.0")
        self.root.geometry("850x700") # Slightly larger window
        self.root.configure(bg="#0d0d0d") # Near-black background

        # --- STYLE CONFIGURATION ---
        style = ttk.Style()
        style.theme_use('clam')

        PRIMARY_DARK = "#0d0d0d"
        SECONDARY_DARK = "#1a1a1a"
        AZURE_ACCENT = "#00aaff" # Deep Azure Blue

        # General Styles
        style.configure("TFrame", background=SECONDARY_DARK)
        style.configure("TLabel", background=SECONDARY_DARK, foreground="#e0e0e0", font=("Segoe UI", 11))
        
        # Labelframe (used for containers)
        style.configure("TLabelframe", background=SECONDARY_DARK, foreground=AZURE_ACCENT, bordercolor=AZURE_ACCENT, relief="solid")
        style.configure("TLabelframe.Label", background=SECONDARY_DARK, foreground=AZURE_ACCENT, font=("Segoe UI", 12, "bold"))
        
        # Notebook (Tabs) Styling
        style.configure("TNotebook", background=PRIMARY_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background="#333333", foreground="white", padding=[20, 7], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", AZURE_ACCENT)], foreground=[("selected", PRIMARY_DARK)])

        # Progress Bars (Thick and highly visible)
        style.configure("Red.Horizontal.TProgressbar", background='#ff4444', thickness=30, troughcolor='#333333', bordercolor="#1e1e1e")
        style.configure("Orange.Horizontal.TProgressbar", background='#ffbb00', thickness=30, troughcolor='#333333', bordercolor="#1e1e1e")
        style.configure("Green.Horizontal.TProgressbar", background='#00e676', thickness=30, troughcolor='#333333', bordercolor="#1e1e1e")

        # --- HEADER ---
        header_frame = tk.Frame(root, bg="#050505", height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="🛡️ ADVANCED PASSWORD ENTROPY ANALYZER", bg="#050505", fg=AZURE_ACCENT, 
                 font=("Impact", 24)).pack(side="left", padx=20, pady=10)

        # --- TABS ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_strength = ttk.Frame(self.notebook)
        self.tab_cracker = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_strength, text="  🔐 STRENGTH AUDIT  ")
        self.notebook.add(self.tab_cracker, text="  🎯 PASSWORD CRACK SIMULATION  ")

        self.setup_strength_tab(AZURE_ACCENT)
        self.setup_cracker_tab(AZURE_ACCENT)

        self.stop_event = threading.Event()

    # ================= TAB 1: STRENGTH =================
    def setup_strength_tab(self, AZURE_ACCENT):
        center_frame = ttk.Frame(self.tab_strength)
        center_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # ⚙️ Input Section
        ttk.Label(center_frame, text="⚙️ ENTER CREDENTIALS FOR REAL-TIME SCAN", foreground="#aaaaaa").pack(anchor="w", pady=(0, 5))

        input_frame = tk.Frame(center_frame, bg="#1a1a1a", relief="solid", bd=2, highlightbackground=AZURE_ACCENT, highlightthickness=1)
        input_frame.pack(fill="x", pady=(5, 20))
        
        # Input Field (prominent)
        self.ent_pass = tk.Entry(input_frame, show="•", bg="#2c2c2c", fg="white", 
                                 insertbackground=AZURE_ACCENT, font=("Consolas", 18), relief="flat", bd=15)
        self.ent_pass.pack(side="left", fill="x", expand=True)
        self.ent_pass.bind("<KeyRelease>", self.run_strength_test)

        # Toggle Button
        self.var_show = tk.BooleanVar()
        self.btn_show = tk.Checkbutton(input_frame, text="👁", variable=self.var_show, 
                                       bg="#1a1a1a", fg=AZURE_ACCENT, selectcolor="#444444",
                                       activebackground="#1a1a1a", activeforeground="white",
                                       command=self.toggle_password_visibility, font=("Segoe UI", 16, "bold"), padx=10)
        self.btn_show.pack(side="left", fill="y")

        # 📈 Visuals Frame
        visual_frame = ttk.LabelFrame(center_frame, text=" 📈 ENTROPY RATING ")
        visual_frame.pack(fill="x", pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(visual_frame, variable=self.progress_var, maximum=100, length=400, mode='determinate', style="Red.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", padx=30, pady=(25, 15))

        # Score Display (Oversized for impact)
        self.lbl_score = tk.Label(visual_frame, text="0 / 100", bg="#1a1a1a", fg="#555555", font=("Impact", 40, "bold"))
        self.lbl_score.pack(pady=(0, 25))

        # 📝 Feedback Terminal
        ttk.Label(center_frame, text="📝 SECURITY REPORT & VULNERABILITIES", foreground="#aaaaaa").pack(anchor="w", pady=(20, 5))
        
        self.txt_suggestions = tk.Text(center_frame, height=8, bg="#050505", fg="#00e676", 
                                       font=("Courier New", 12), relief="flat", bd=5, insertbackground="#00e676")
        self.txt_suggestions.pack(fill="both", expand=True)
        self.txt_suggestions.insert("1.0", f"[{time.strftime('%H:%M:%S')}] > SYSTEM INITIALIZED. AWAITING INPUT...\n")
        self.txt_suggestions.bind("<Key>", lambda e: "break")

    def toggle_password_visibility(self):
        if self.var_show.get():
            self.ent_pass.config(show="")
        else:
            self.ent_pass.config(show="•")

    def run_strength_test(self, event=None):
        pwd = self.ent_pass.get()
        self.txt_suggestions.delete(1.0, tk.END)
        
        if not pwd:
            self.progress_var.set(0)
            self.lbl_score.config(text="0 / 100", fg="#555555")
            self.txt_suggestions.insert("1.0", f"[{time.strftime('%H:%M:%S')}] > WAITING FOR INPUT...\n")
            return
        
        score, suggestions = calculate_strength(pwd)
        self.progress_var.set(score)

        # Dynamic Styling
        bar_style = "Red.Horizontal.TProgressbar"
        color = "#ff4444"
        verdict = "VULNERABLE"

        if score >= 50:
            bar_style = "Orange.Horizontal.TProgressbar"
            color = "#ffbb00"
            verdict = "MODERATE"
        if score >= 85:
            bar_style = "Green.Horizontal.TProgressbar"
            color = "#00e676"
            verdict = "SECURE"
        
        self.progress_bar.configure(style=bar_style)
        self.lbl_score.config(text=f"{score} / 100  [{verdict}]", fg=color)
        
        if suggestions:
            for s in suggestions:
                self.txt_suggestions.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] > {s}\n")
        else:
            self.txt_suggestions.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] > STATUS: GREEN\n")
            self.txt_suggestions.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] > ENTROPY RATING: MAX\n")
            self.txt_suggestions.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] > NO CRITICAL VULNERABILITIES DETECTED.")

    # ================= TAB 2: CRACKER =================
    def setup_cracker_tab(self, AZURE_ACCENT):
        center_frame = ttk.Frame(self.tab_cracker)
        center_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # ⚙️ Configuration Area
        config_frame = ttk.LabelFrame(center_frame, text=" ⚙️ ATTACK PARAMETERS ")
        config_frame.pack(fill="x", pady=10)

        grid_frame = tk.Frame(config_frame, bg="#1a1a1a", padx=15, pady=15)
        grid_frame.pack(fill="x")

        tk.Label(grid_frame, text="TARGET CREDENTIAL:", bg="#1a1a1a", fg="#e0e0e0", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_target = tk.Entry(grid_frame, bg="#333333", fg="white", font=("Consolas", 14), relief="flat", bd=8, insertbackground="white")
        self.ent_target.grid(row=0, column=1, padx=15, sticky="ew")
        grid_frame.columnconfigure(1, weight=1)

        tk.Label(grid_frame, text="CRACKING METHOD:", bg="#1a1a1a", fg="#e0e0e0", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", pady=10)
        
        self.attack_type = tk.StringVar(value="dict")
        radio_frame = tk.Frame(grid_frame, bg="#1a1a1a")
        radio_frame.grid(row=1, column=1, sticky="w", padx=15)

        modes = [("Dictionary", "dict"), ("Brute Force (5)", "5"), ("Brute Force (6)", "6"), ("Brute Force (8)", "8")]
        for text, val in modes:
            tk.Radiobutton(radio_frame, text=text, variable=self.attack_type, value=val,
                           bg="#1a1a1a", fg=AZURE_ACCENT, selectcolor="#333333", activebackground="#1a1a1a", activeforeground="white", font=("Segoe UI", 10)).pack(side="left", padx=10)

        # Buttons (Custom "Flat" Look)
        btn_frame = tk.Frame(center_frame, bg="#0d0d0d")
        btn_frame.pack(pady=20)

        self.btn_start = tk.Button(btn_frame, text="▶ INITIATE ATTACK", command=self.start_attack_thread,
                                   bg="#00aaff", fg="black", font=("Segoe UI", 12, "bold"), relief="raised", bd=3, padx=30, pady=8)
        self.btn_start.pack(side="left", padx=15)

        self.btn_stop = tk.Button(btn_frame, text="⏹ TERMINATE", command=self.stop_attack,
                                  bg="#aa3333", fg="white", font=("Segoe UI", 12, "bold"), relief="flat", bd=3, padx=30, pady=8, state="disabled")
        self.btn_stop.pack(side="left", padx=15)

        # 🖥️ Monitor
        monitor_frame = ttk.LabelFrame(center_frame, text=" 🖥️ LIVE EXECUTION LOG ")
        monitor_frame.pack(fill="both", expand=True, pady=10)

        self.lbl_status = tk.Label(monitor_frame, text="[SYSTEM IDLE]", bg="#1a1a1a", fg="#555555", font=("Consolas", 14, "bold"))
        self.lbl_status.pack(anchor="w", padx=15, pady=10)

        self.log_area = scrolledtext.ScrolledText(monitor_frame, height=8, state='disabled', 
                                                  bg="#050505", fg="#00ff00", font=("Courier New", 11), relief="flat")
        self.log_area.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def stop_attack(self):
        self.stop_event.set()
        self.log(f"[{time.strftime('%H:%M:%S')}] >>> PROCESS TERMINATED BY USER")
        self.btn_start.config(state="normal", bg="#00aaff")
        self.btn_stop.config(state="disabled", bg="#552222")

    def start_attack_thread(self):
        target = self.ent_target.get()
        attack_mode = self.attack_type.get()
        
        if not target:
            messagebox.showwarning("INPUT ERROR", "Please define a target password.")
            return

        # --- LENGTH VALIDATION ---
        if attack_mode in ('5', '6', '8'):
            required_length = int(attack_mode)
            if len(target) != required_length:
                messagebox.showwarning("LENGTH MISMATCH", 
                    f"Selected Brute Force ({required_length} Char) requires a target of exactly {required_length} characters. You entered {len(target)}.")
                return
        # --- END VALIDATION ---

        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        
        self.stop_event.clear()
        self.btn_start.config(state="disabled", bg="#225588")
        self.btn_stop.config(state="normal", bg="#aa3333")

        t = threading.Thread(target=self.run_attack_logic, args=(target, attack_mode))
        t.daemon = True
        t.start()

    def run_attack_logic(self, target, mode):
        start_time = time.time()
        found = False
        password_found = ""

        if mode == "dict":
            self.log(f"[{time.strftime('%H:%M:%S')}] [*] LOADING DICTIONARY MODULE...")
            for guess in COMMON_PASSWORDS:
                if self.stop_event.is_set(): return
                self.lbl_status.config(text=f"DICTIONARY TEST: {guess}", fg="#00aaff")
                if guess.lower() == target.lower():
                    password_found = guess; found = True; break
                time.sleep(0.05)
        else:
            max_len = int(mode)
            self.log(f"[{time.strftime('%H:%M:%S')}] [*] INITIALIZING BRUTE FORCE ENGINE (LEN {max_len})...")
            char_set = string.ascii_lowercase + string.digits + string.ascii_uppercase
            
            for length in range(max_len, max_len + 1):
                if found or self.stop_event.is_set(): break
                self.log(f"[{time.strftime('%H:%M:%S')}] [*] CHECKING {length}-CHARACTER SPACE...")
                
                last_update = time.time()
                for guess_tuple in itertools.product(char_set, repeat=length):
                    if self.stop_event.is_set(): return
                    guess = "".join(guess_tuple)

                    if time.time() - last_update > 0.2:
                        self.lbl_status.config(text=f"HASHING: {guess}", fg="#00aaff")
                        last_update = time.time()

                    if guess == target.lower():
                        password_found = guess; found = True; break

        elapsed = time.time() - start_time
        
        if found:
            self.lbl_status.config(text=">>> ACCESS GRANTED: CRACK SUCCESS <<<", fg="#00ff00")
            self.log(f"\n[{time.strftime('%H:%M:%S')}] [+] MATCH FOUND: '{password_found}'")
            self.log(f"[{time.strftime('%H:%M:%S')}] [+] TIME ELAPSED: {elapsed:.4f}s")
            messagebox.showinfo("SUCCESS", f"PASSWORD CRACKED\n\nKey: {password_found}\nTime: {elapsed:.4f}s")
        else:
            if not self.stop_event.is_set():
                self.lbl_status.config(text=">>> FAILED: SEARCH SPACE EXHAUSTED <<<", fg="#ff4444")
                self.log(f"\n[{time.strftime('%H:%M:%S')}] [-] PASSWORD NOT FOUND.")
                messagebox.showerror("FAILURE", "Password not found within search limits.")

        self.btn_start.config(state="normal", bg="#00aaff")
        self.btn_stop.config(state="disabled", bg="#552222")

if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicPasswordApp(root)
    root.mainloop()