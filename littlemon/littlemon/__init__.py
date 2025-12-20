import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
import threading
import os

def download_video():
    url = url_entry.get().strip()
    folder = path_var.get()

    if not url or not folder:
        messagebox.showerror("Error", "URL and folder required")
        return

    download_btn.config(state=tk.DISABLED)
    status_label.config(text="Downloading...")

    def task():
        try:
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
                "quiet": True,
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_label.config(text="Done")
            messagebox.showinfo("Success", "Download completed")

        except Exception as e:
            status_label.config(text="Error")
            messagebox.showerror("Error", str(e))

        finally:
            download_btn.config(state=tk.NORMAL)

    threading.Thread(target=task).start()

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)

# ---------- UI ----------
root = tk.Tk()
root.title("YouTube Downloader (No FFmpeg)")
root.geometry("520x230")
root.resizable(False, False)

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=65)
url_entry.pack(pady=5)

tk.Label(root, text="Save to:").pack()
path_var = tk.StringVar()
path_entry = tk.Entry(root, textvariable=path_var, width=50)
path_entry.pack(side=tk.LEFT, padx=10, pady=5)

tk.Button(root, text="Browse", command=choose_folder).pack(side=tk.LEFT)

download_btn = tk.Button(root, text="Download", width=20, command=download_video)
download_btn.pack(pady=15)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
