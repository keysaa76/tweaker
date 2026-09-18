
import os
import sys
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox

try:
    import customtkinter as ctk
except ImportError:
    raise SystemExit("Install terlebih dahulu: pip install customtkinter")

APP_NAME = "LEVSCLOADES"
COPYRIGHT = "Copyright © 2026 LEVSCLOADES — All Rights Reserved."

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def is_admin():
    if os.name != "nt":
        return False
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def detect_gpu():
    """Deteksi GPU melalui PowerShell. Tidak mengubah sistem."""
    if os.name != "nt":
        return ["Non-Windows system"]
    try:
        cmd = [
            "powershell", "-NoProfile", "-Command",
            "Get-CimInstance Win32_VideoController | "
            "Select-Object -ExpandProperty Name"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        gpus = [x.strip() for x in result.stdout.splitlines() if x.strip()]
        return gpus or ["GPU tidak terdeteksi"]
    except Exception as e:
        return [f"Deteksi gagal: {e}"]


class LevscLoader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1100x680")
        self.minsize(900, 580)

        self.show_splash()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_splash(self):
        self.clear()
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=80, pady=70)

        ctk.CTkLabel(
            frame, text="LEVSCLOADES",
            font=ctk.CTkFont(size=42, weight="bold")
        ).pack(pady=(60, 5))

        ctk.CTkLabel(
            frame, text="WINDOWS DEBLOATER & OPTIMIZER",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)

        ctk.CTkLabel(
            frame,
            text=(
                "Welcome to LEVSCLOADES\n\n"
                "A Windows optimization utility for configurable\n"
                "debloating, system and GPU tweaks.\n\n"
                "IMPORTANT\n"
                "Create a System Restore Point before applying\n"
                "system modifications."
            ),
            justify="center",
            font=ctk.CTkFont(size=14)
        ).pack(pady=25)

        ctk.CTkLabel(
            frame,
            text=(
                "This software may not be resold, repackaged,\n"
                "or redistributed as another paid product without permission.\n\n"
                + COPYRIGHT
            ),
            justify="center",
            font=ctk.CTkFont(size=12)
        ).pack(pady=10)

        ctk.CTkButton(
            frame, text="CONTINUE", width=220, height=42,
            command=self.show_main
        ).pack(pady=25)

    def show_main(self):
        self.clear()

        header = ctk.CTkFrame(self, height=75)
        header.pack(fill="x", padx=15, pady=(15, 8))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="LEVSCLOADES",
            font=ctk.CTkFont(size=27, weight="bold")
        ).pack(side="left", padx=20)

        status = "ADMINISTRATOR" if is_admin() else "STANDARD USER"
        ctk.CTkLabel(header, text=status).pack(side="right", padx=20)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15, pady=5)

        self.make_category(body, "DEBLOATERS", [
            ("Windows Privacy", self.not_ready),
            ("Windows Debloat", self.not_ready),
            ("Apps", self.not_ready),
        ], 0)

        self.make_category(body, "TWEAK PACK", [
            ("Power Plans", self.not_ready),
            ("GPU OPTIMIZATIONS", self.show_gpu),
            ("OS Optimizations", self.not_ready),
            ("Useful Tools", self.not_ready),
        ], 1)

        self.make_category(body, "NETWORK OPTIMIZER", [
            ("Network Adapter", self.not_ready),
            ("TCP Settings", self.not_ready),
            ("Network Info", self.show_network_info),
        ], 2)

        footer = ctk.CTkLabel(
            self, text=COPYRIGHT,
            font=ctk.CTkFont(size=11)
        )
        footer.pack(pady=(3, 10))

    def make_category(self, parent, title, buttons, column):
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, sticky="nsew", padx=7)
        parent.grid_columnconfigure(column, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))

        for text, command in buttons:
            ctk.CTkButton(
                card, text=text, height=42,
                command=command
            ).pack(fill="x", padx=20, pady=7)

    def not_ready(self):
        messagebox.showinfo(
            APP_NAME,
            "Modul ini masih dalam tahap pengembangan.\n"
            "Belum ada perubahan sistem yang dilakukan."
        )

    def show_gpu(self):
        self.clear()

        top = ctk.CTkFrame(self, height=70)
        top.pack(fill="x", padx=15, pady=(15, 8))
        top.pack_propagate(False)

        ctk.CTkButton(
            top, text="← BACK", width=100,
            command=self.show_main
        ).pack(side="left", padx=15, pady=15)

        ctk.CTkLabel(
            top, text="GPU OPTIMIZATIONS",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20)

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=15)

        gpus = detect_gpu()
        gpu_text = "\n".join(gpus)

        info = ctk.CTkFrame(content)
        info.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            info, text="DETECTED GPU",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            info, text=gpu_text, justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))

        grid = ctk.CTkFrame(content, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        self.gpu_card(grid, "NVIDIA GPU", 0)
        self.gpu_card(grid, "AMD iGPU", 1)
        self.gpu_card(grid, "AMD Radeon RX", 2)

        ctk.CTkLabel(
            content,
            text="Detection only in this demo — no GPU settings are changed.",
            font=ctk.CTkFont(size=11)
        ).pack(pady=10)

    def gpu_card(self, parent, title, col):
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=col, sticky="nsew", padx=6)

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(pady=(20, 15))

        for item in [
            "Hardware scheduling",
            "Shader cache",
            "Graphics preference",
            "Game Mode",
        ]:
            ctk.CTkCheckBox(card, text=item).pack(
                anchor="w", padx=20, pady=7
            )

        ctk.CTkButton(
            card, text="APPLY SELECTED",
            command=lambda: messagebox.showinfo(
                APP_NAME,
                "Demo: belum menerapkan perubahan sistem."
            )
        ).pack(fill="x", padx=20, pady=20)

    def show_network_info(self):
        messagebox.showinfo(
            APP_NAME,
            f"OS: {platform.platform()}\n"
            f"Computer: {platform.node()}\n\n"
            "Network optimizer akan ditambahkan pada modul berikutnya."
        )


if __name__ == "__main__":
    app = LevscLoader()
    app.mainloop()
