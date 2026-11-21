# DNS Recon Console
# Coded by RUDRA SINGH
# only scan domains you have permission to test

import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
import dns.resolver

AUTHOR = "RUDRA SINGH"
TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

BG = "#0a0e14"
GREEN = "#00ff9c"
CYAN = "#4cc9f0"
RED = "#ff4d6d"


def lookup(domain, rtype):
    # returns a list of records, empty list if nothing found
    try:
        answers = dns.resolver.resolve(domain, rtype, lifetime=5)
        return [a.to_text() for a in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []
    except Exception as e:
        return ["error: %s" % e]


def scan():
    domain = entry.get().strip()
    if not domain:
        return
    output.delete("1.0", "end")
    output.insert("end", ">> scanning %s ...\n\n" % domain, "head")
    status.config(text="scanning...")
    # thread so the window doesn't freeze
    threading.Thread(target=worker, args=(domain,), daemon=True).start()


def worker(domain):
    results = {}
    for t in TYPES:
        if checks[t].get():
            results[t] = lookup(domain, t)
    root.after(0, show, results)


def show(results):
    for rtype, values in results.items():
        if not values:
            output.insert("end", "[-] %-6s none\n" % rtype, "bad")
        for v in values:
            output.insert("end", "[+] %-6s %s\n" % (rtype, v), "ok")
    output.insert("end", "\n-- coded by %s --\n" % AUTHOR, "head")
    status.config(text="done")


root = tk.Tk()
root.title("DNS Recon Console | by " + AUTHOR)
root.geometry("700x500")
root.configure(bg=BG)
root.bind("<Return>", lambda e: scan())

tk.Label(root, text="DNS RECON CONSOLE", bg=BG, fg=GREEN,
         font=("Consolas", 18, "bold")).pack(pady=(10, 0))
tk.Label(root, text="coded by " + AUTHOR, bg=BG, fg=CYAN,
         font=("Consolas", 10)).pack()

# input row
top = tk.Frame(root, bg=BG)
top.pack(pady=8)
entry = ttk.Entry(top, width=35)
entry.pack(side="left", padx=5)
ttk.Button(top, text="SCAN", command=scan).pack(side="left")
ttk.Button(top, text="CLEAR", command=lambda: output.delete("1.0", "end")).pack(side="left", padx=5)

# record type checkboxes
box = tk.Frame(root, bg=BG)
box.pack()
checks = {}
for t in TYPES:
    checks[t] = tk.BooleanVar(value=True)
    tk.Checkbutton(box, text=t, variable=checks[t], bg=BG, fg=GREEN,
                   selectcolor=BG, activebackground=BG).pack(side="left")

output = scrolledtext.ScrolledText(root, bg="#121923", fg=GREEN, font=("Consolas", 10), bd=0)
output.pack(fill="both", expand=True, padx=10, pady=8)
output.tag_config("ok", foreground=GREEN)
output.tag_config("bad", foreground=RED)
output.tag_config("head", foreground=CYAN)

status = tk.Label(root, text="ready", bg=BG, fg=CYAN, anchor="w")
status.pack(fill="x", padx=10)

root.mainloop()