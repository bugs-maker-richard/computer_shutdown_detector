import threading
import time
import tkinter as tk
import webbrowser
from tkinter import ttk


OFFICIAL_WEBSITE_URL = "https://bugs-maker-richard.github.io/computer_shutdown_detector/"
COPYRIGHT_TEXT = "Copyright © 2026 Richard Lin. All rights reserved."


TRANSLATIONS = {
    "zh": {
        "language": "语言",
        "title": "电脑关机检测器",
        "waiting": "等待检测...",
        "start": "立即检测",
        "website": "打开官网",
        "thinking": "AI大模型深度思考中...",
        "finished": "检测完成",
        "report_title": "检测报告",
        "result": "检测结果：\n\n经 AI 深度分析：\n您的电脑目前【未关机】！",
        "close": "我知道了",
    },
    "en": {
        "language": "Language",
        "title": "Computer Shutdown Detector",
        "waiting": "Waiting...",
        "start": "Start",
        "website": "Open offical Website",
        "thinking": "AI is thinking deeply...",
        "finished": "Finish",
        "report_title": "Test Report",
        "result": (
            "Detection result:\n\n"
            "After AI deep analysis:\n"
            "Your computer is currently [not shut down]!"
        ),
        "close": "OK",
    },
}


class ShutdownDetectorApp:
    def __init__(self, root):
        self.root = root
        self.language = tk.StringVar(value="zh")
        self.is_running = False

        window_width = 430
        window_height = 345
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f4")

        self.top_frame = tk.Frame(root, bg="#f4f4f4")
        self.top_frame.pack(fill=tk.X, padx=18, pady=(14, 0))

        self.website_btn = tk.Button(
            self.top_frame,
            font=("Microsoft YaHei", 9, "underline"),
            bg="#f4f4f4",
            fg="#555555",
            activebackground="#f4f4f4",
            activeforeground="#333333",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.open_website,
        )
        self.website_btn.pack(side=tk.LEFT)

        self.language_frame = tk.Frame(self.top_frame, bg="#f4f4f4")
        self.language_frame.pack(side=tk.RIGHT)

        self.language_label = tk.Label(
            self.language_frame,
            font=("Microsoft YaHei", 9),
            bg="#f4f4f4",
            fg="#555555",
        )
        self.language_label.pack(side=tk.LEFT, padx=(0, 8))

        self.language_box = ttk.Combobox(
            self.language_frame,
            textvariable=self.language,
            values=("zh", "en"),
            state="readonly",
            width=8,
        )
        self.language_box.pack(side=tk.LEFT)
        self.language_box.bind("<<ComboboxSelected>>", self.change_language)

        self.title_label = tk.Label(
            root,
            font=("Microsoft YaHei", 20, "bold"),
            bg="#f4f4f4",
            fg="#333333",
        )
        self.title_label.pack(pady=(32, 10))

        self.status_label = tk.Label(
            root,
            font=("Microsoft YaHei", 10, "italic"),
            bg="#f4f4f4",
            fg="#888888",
        )
        self.status_label.pack(pady=5)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=20,
            troughcolor="#f0f0f0",
            background="#a1c4fd",
        )

        self.progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length=280,
            mode="determinate",
            style="Custom.Horizontal.TProgressbar",
        )
        self.progress.pack(pady=10)

        self.btn = tk.Button(
            root,
            font=("Microsoft YaHei", 12),
            bg="#ffffff",
            fg="#333333",
            relief="groove",
            width=12,
            command=self.start_detection,
        )
        self.btn.pack(pady=(15, 0))

        self.footer_label = tk.Label(
            root,
            text=COPYRIGHT_TEXT,
            font=("Microsoft YaHei", 8),
            bg="#f4f4f4",
            fg="#777777",
            wraplength=390,
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=(0, 10))

        self.apply_language()

    def text(self, key):
        return TRANSLATIONS[self.language.get()][key]

    def apply_language(self):
        self.root.title(self.text("title"))
        self.language_label.config(text=self.text("language"))
        self.title_label.config(text=self.text("title"))
        self.btn.config(text=self.text("start"))
        self.website_btn.config(text=self.text("website"))

        if not self.is_running:
            self.status_label.config(text=self.text("waiting"), fg="#888888")

    def change_language(self, _event=None):
        self.apply_language()

    def open_website(self):
        webbrowser.open(OFFICIAL_WEBSITE_URL, new=2)

    def start_detection(self):
        self.is_running = True
        self.btn.config(state=tk.DISABLED)
        self.language_box.config(state=tk.DISABLED)
        threading.Thread(target=self.run_detection_animation, daemon=True).start()

    def run_detection_animation(self):
        self.status_label.config(text=self.text("thinking"), fg="#888888")
        self.progress["value"] = 0

        for i in range(1, 101):
            time.sleep(0.03)
            self.progress["value"] = i
            if i in [35, 65, 88]:
                time.sleep(0.4)
            self.root.update_idletasks()

        self.status_label.config(text=self.text("finished"), fg="#2ecc71")
        time.sleep(0.2)
        self.show_result_popup()

    def reset_ui(self, popup):
        popup.destroy()
        self.is_running = False
        self.btn.config(state=tk.NORMAL)
        self.language_box.config(state="readonly")
        self.status_label.config(text=self.text("waiting"), fg="#888888")
        self.progress.config(value=0)

    def show_result_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title(self.text("report_title"))
        popup.geometry("340x170")
        popup.configure(bg="#ffffff")
        popup.geometry(f"+{self.root.winfo_x() + 45}+{self.root.winfo_y() + 75}")
        popup.resizable(False, False)

        msg = tk.Label(
            popup,
            text=self.text("result"),
            font=("Microsoft YaHei", 11, "bold"),
            bg="#ffffff",
            fg="#e74c3c",
            justify=tk.CENTER,
        )
        msg.pack(pady=(22, 12))

        close_btn = tk.Button(
            popup,
            text=self.text("close"),
            font=("Microsoft YaHei", 10),
            command=lambda: self.reset_ui(popup),
        )
        close_btn.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownDetectorApp(root)
    root.mainloop()
